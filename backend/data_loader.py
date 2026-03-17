import math
import os
import pandas as pd
from typing import Any

# Path: same directory as this file (backend/)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_XLSX_PATH = os.path.join(_BASE_DIR, "CP_Glide_Data_Master.xlsx")

_data: dict[str, list[dict[str, Any]]] = {
    "competitors": [],
    "products": [],
    "traceability": [],
    "market_data": [],
    "opportunities": [],
    "personas": [],
}


def _clean(val: Any) -> Any:
    """Replace NaN/Inf floats with None so JSON serialisation never fails."""
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return None
    return val


def _safe_read_sheet(xl: pd.ExcelFile, sheet_name: str) -> list[dict[str, Any]]:
    """Try to read a sheet by name (case-insensitive partial match). Return [] on failure."""
    available = xl.sheet_names
    # exact match first
    target = None
    for s in available:
        if s.strip().lower() == sheet_name.lower():
            target = s
            break
    # partial match fallback
    if target is None:
        for s in available:
            if sheet_name.lower() in s.strip().lower():
                target = s
                break
    if target is None:
        print(f"[data_loader] Sheet '{sheet_name}' not found. Available: {available}")
        return []
    try:
        df = pd.read_excel(xl, sheet_name=target)
        records = df.to_dict(orient="records")
        # Replace NaN/Inf with None for JSON serialisation
        return [{k: _clean(v) for k, v in row.items()} for row in records]
    except Exception as e:
        print(f"[data_loader] Error reading sheet '{target}': {e}")
        return []


def _map_competitors(rows: list[dict]) -> list[dict]:
    """Rename Excel columns to match frontend field names."""
    result = []
    for r in rows:
        result.append({
            "Competitor": r.get("Name"),
            "Model": r.get("Business_Model"),
            "City_Focus": r.get("City_Focus"),
            "Revenue_CNY_B": r.get("Revenue_2024_Billion_CNY"),
            "GMV_CNY_B": r.get("GMV_2024_Billion_CNY"),
            "Net_Profit_CNY_M": r.get("Net_Profit_2024_M_CNY"),
            "MAU_M": r.get("Monthly_Active_Users_M"),
            "Avg_Basket_CNY": r.get("Avg_Basket_Size_CNY"),
            "Store_Count": r.get("Stores_or_Warehouses"),
            "Key_Advantage": r.get("Strength_1"),
            "Weakness": r.get("Weakness_1"),
            "Traceability_Level": r.get("Traceability_Level"),
            "Source": r.get("Source"),
        })
    return result


def _map_products(rows: list[dict]) -> list[dict]:
    """Rename Excel columns to match frontend field names."""
    result = []
    for r in rows:
        result.append({
            "Product_ID": r.get("Product_ID"),
            "Product_Name": r.get("Name_EN"),
            "Name_CN": r.get("Name_CN"),
            "Origin": r.get("Origin"),
            "Category": r.get("Category"),
            "Sub_Category": r.get("Sub_Category"),
            "Price_CNY": r.get("Price_CNY"),
            "Original_Price_CNY": r.get("Original_Price_CNY"),
            "Discount_Pct": r.get("Discount_Pct"),
            "Quality_Score": r.get("Quality_Score"),
            "Stability_Score": r.get("Stability_Score"),
            "Freshness_Days": r.get("Freshness_Days"),
            "Certification": r.get("Certification"),
            "CP_Select": r.get("Private_Label"),
            "Description": r.get("Description"),
            "Tags": r.get("Tags"),
            "Unit": r.get("Unit"),
            "Stock_Status": r.get("Stock_Status"),
        })
    return result


def _map_market_data(rows: list[dict]) -> list[dict]:
    """Rename Excel columns and derive Is_Forecast field."""
    result = []
    for r in rows:
        year = r.get("Year")
        result.append({
            "Year": year,
            "Market_Size_CNY_B": r.get("Market_Size_Billion_CNY"),
            "YoY_Growth_Rate_Pct": r.get("YoY_Growth_Rate_Pct"),
            "Penetration_Rate": r.get("Penetration_Rate_Pct"),
            "Key_Drivers": r.get("Key_Drivers"),
            "Notable_Event": r.get("Notable_Event"),
            "Source": r.get("Source"),
            # Years > 2024 are forecast data
            "Is_Forecast": int(year) > 2024 if year is not None else False,
        })
    return result


def load_all() -> None:
    """Load all sheets from the xlsx file into the in-memory _data dict."""
    if not os.path.exists(_XLSX_PATH):
        print(f"[data_loader] WARNING: xlsx not found at {_XLSX_PATH}")
        return

    try:
        xl = pd.ExcelFile(_XLSX_PATH, engine="openpyxl")
        print(f"[data_loader] Sheets available: {xl.sheet_names}")

        raw_competitors = _safe_read_sheet(xl, "Competitors")
        _data["competitors"] = _map_competitors(raw_competitors)

        _data["products"] = _map_products(_safe_read_sheet(xl, "Products"))

        # Traceability sheet may be named differently
        trace = _safe_read_sheet(xl, "Trace_Nodes")
        if not trace:
            trace = _safe_read_sheet(xl, "Traceability")
        _data["traceability"] = trace

        raw_market = _safe_read_sheet(xl, "Market_Data")
        _data["market_data"] = _map_market_data(raw_market)

        _data["opportunities"] = _safe_read_sheet(xl, "Opportunities")
        _data["personas"] = _safe_read_sheet(xl, "Customer_Personas")

        print(
            f"[data_loader] Loaded — competitors:{len(_data['competitors'])}, "
            f"products:{len(_data['products'])}, trace:{len(_data['traceability'])}, "
            f"market:{len(_data['market_data'])}, opps:{len(_data['opportunities'])}, "
            f"personas:{len(_data['personas'])}"
        )
    except Exception as e:
        print(f"[data_loader] Fatal error loading xlsx: {e}")


def get_competitors() -> list[dict]:
    return _data["competitors"]


def get_products() -> list[dict]:
    return _data["products"]


_TRACE_DATA: dict[str, list[dict]] = {
    "P001": [  # Organic Baby Spinach
        {"Product_ID": "P001", "Step_Order": 1, "Stage": "Organic Farm",
         "Location": "Shouguang, Shandong", "Date": "2026-03-10",
         "Description": "Grown in GAP-certified organic fields with zero synthetic pesticides. Soil health and irrigation water quality verified by third-party auditors each season.",
         "Temperature": "Ambient", "Duration": "30 days", "Vehicle": None, "Certifications": "GAP Certified, Organic China"},
        {"Product_ID": "P001", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Shouguang, Shandong", "Date": "2026-03-11",
         "Description": "Hand-harvested before 6 AM for peak freshness. Leaves graded by size and colour; damaged leaves removed on-site immediately after cutting.",
         "Temperature": "12–18 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "GAP Certified"},
        {"Product_ID": "P001", "Step_Order": 3, "Stage": "Pre-Cooling",
         "Location": "Weifang, Shandong", "Date": "2026-03-11",
         "Description": "Forced-air pre-cooling tunnel reduces core temperature to ≤4 °C within 90 minutes, locking in vitamins and vibrant colour.",
         "Temperature": "0–4 °C", "Duration": "2 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P001", "Step_Order": 4, "Stage": "Cold Chain Transit",
         "Location": "Jinan, Shandong", "Date": "2026-03-12",
         "Description": "GPS-tracked refrigerated truck with continuous 0–4 °C cold chain. Temperature logs uploaded every 15 minutes to CP's traceability platform.",
         "Temperature": "0–4 °C", "Duration": "8 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P001", "Step_Order": 5, "Stage": "Distribution Center",
         "Location": "Tianjin", "Date": "2026-03-13",
         "Description": "Received at CP's regional distribution centre. Lot-level scanning, FIFO rotation, and microbiological sampling before dispatch clearance.",
         "Temperature": "2–4 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P001", "Step_Order": 6, "Stage": "Quality Inspection",
         "Location": "Tianjin", "Date": "2026-03-13",
         "Description": "Final quality pass: visual inspection, weight verification, microbiological clearance, and full cold-chain log review before consumer release.",
         "Temperature": "2–4 °C", "Duration": "3 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P001", "Step_Order": 7, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Same-day cold-chain delivery in insulated packaging with ice gel packs. Photo confirmation uploaded to order record on arrival.",
         "Temperature": "0–6 °C", "Duration": "3 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P002": [  # Heirloom Tomatoes
        {"Product_ID": "P002", "Step_Order": 1, "Stage": "Greenhouse Farm",
         "Location": "Weifang, Shandong", "Date": "2026-03-10",
         "Description": "Heirloom tomatoes cultivated in climate-controlled glasshouses via hydroponic nutrient film technique. No synthetic pesticides throughout the 60-day grow cycle.",
         "Temperature": "22–26 °C", "Duration": "60 days", "Vehicle": None, "Certifications": "GAP Certified, Green Food"},
        {"Product_ID": "P002", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Weifang, Shandong", "Date": "2026-03-11",
         "Description": "Hand-picked at peak Brix (7.5–9.0). Graded by colour uniformity, firmness, and size. Over-ripe or blemished fruit rejected at line.",
         "Temperature": "18–22 °C", "Duration": "5 hours", "Vehicle": None, "Certifications": "GAP Certified"},
        {"Product_ID": "P002", "Step_Order": 3, "Stage": "Packaging",
         "Location": "Jinan, Shandong", "Date": "2026-03-11",
         "Description": "Packed in ventilated punnets with QR-coded traceability labels. Modified-atmosphere film extends shelf life by up to 40% versus standard wrap.",
         "Temperature": "8–12 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P002", "Step_Order": 4, "Stage": "Cold Chain Transit",
         "Location": "Beijing", "Date": "2026-03-12",
         "Description": "Refrigerated truck with real-time temperature telemetry maintains 8–12 °C. Route monitored via CP logistics platform throughout the 6-hour journey.",
         "Temperature": "8–12 °C", "Duration": "6 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P002", "Step_Order": 5, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-13",
         "Description": "Received at Shanghai DC. FIFO management applied; lot allocated to same-day dispatch wave for maximum freshness guarantee.",
         "Temperature": "8–12 °C", "Duration": "18 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P002", "Step_Order": 6, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Delivered in insulated bag within 2-hour slot. Contactless drop-off with photo confirmation and digital receipt.",
         "Temperature": "8–14 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P003": [  # Sweet Corn (3-pack)
        {"Product_ID": "P003", "Step_Order": 1, "Stage": "Farm Origin",
         "Location": "Jilin, China", "Date": "2026-03-08",
         "Description": "Sweet corn cultivated on open farmland in Jilin's fertile black soil region. Non-GMO seeds under CP's supplier quality programme. No synthetic growth regulators.",
         "Temperature": "Ambient", "Duration": "75 days", "Vehicle": None, "Certifications": "GAP Certified, Green Food"},
        {"Product_ID": "P003", "Step_Order": 2, "Stage": "Harvest",
         "Location": "Jilin, China", "Date": "2026-03-10",
         "Description": "Machine-harvested at optimal sugar content (Brix ≥12). Rapid field-to-facility transfer to preserve natural sweetness before starch conversion begins.",
         "Temperature": "Ambient", "Duration": "4 hours", "Vehicle": "Field Harvester", "Certifications": "GAP Certified"},
        {"Product_ID": "P003", "Step_Order": 3, "Stage": "Processing & Packaging",
         "Location": "Changchun, Jilin", "Date": "2026-03-10",
         "Description": "Husked, cleaned, and sorted within 4 hours of harvest. Packed in 3-ear bundles with breathable wrap to maintain moisture and freshness.",
         "Temperature": "4–8 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P003", "Step_Order": 4, "Stage": "Cold Chain Transit",
         "Location": "Beijing", "Date": "2026-03-11",
         "Description": "Refrigerated long-haul truck travels overnight from Changchun to Beijing hub. Temperature maintained at 4–8 °C; route monitored via telematics.",
         "Temperature": "4–8 °C", "Duration": "12 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P003", "Step_Order": 5, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-13",
         "Description": "Consolidated at Shanghai DC. Lot scanned and assigned to same-day fulfilment wave for maximum freshness at delivery.",
         "Temperature": "4–8 °C", "Duration": "24 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P003", "Step_Order": 6, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Delivered in ventilated insulated bag within a 2-hour window. Consumer freshness guaranteed within 4 days of harvest.",
         "Temperature": "4–10 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P004": [  # Purple Asparagus
        {"Product_ID": "P004", "Step_Order": 1, "Stage": "Farm Origin",
         "Location": "Yunnan, China", "Date": "2026-03-07",
         "Description": "Purple asparagus grown at 1,900 m altitude in Yunnan's mild climate, producing spears with exceptional tenderness and high anthocyanin content.",
         "Temperature": "15–22 °C", "Duration": "45 days", "Vehicle": None, "Certifications": "GAP Certified, Organic China"},
        {"Product_ID": "P004", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Yunnan, China", "Date": "2026-03-10",
         "Description": "Hand-cut spears graded by diameter, length, and colour uniformity. Only top-grade 'Extra' class spears selected for CP's premium tier.",
         "Temperature": "15–20 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "GAP Certified"},
        {"Product_ID": "P004", "Step_Order": 3, "Stage": "Pre-Cooling",
         "Location": "Kunming, Yunnan", "Date": "2026-03-10",
         "Description": "Hydro-cooling brings core temperature to ≤4 °C within 1 hour. Preserves colour and minimises moisture loss during subsequent air transit.",
         "Temperature": "0–4 °C", "Duration": "1.5 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P004", "Step_Order": 4, "Stage": "Air Freight",
         "Location": "Kunming, Yunnan", "Date": "2026-03-11",
         "Description": "Loaded in temperature-controlled cargo containers at Kunming Changshui Airport for express flight to Shanghai — fastest route for altitude-grown specialty veg.",
         "Temperature": "0–4 °C", "Duration": "3 hours", "Vehicle": "Air Freight", "Certifications": "IATA Perishable Cargo"},
        {"Product_ID": "P004", "Step_Order": 5, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-03-11",
         "Description": "Received at Pudong cargo terminal. Plant quarantine inspection and incoming QC completed within 4 hours via CP's pre-approved priority lane.",
         "Temperature": "0–4 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P004", "Step_Order": 6, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-12",
         "Description": "Same-day delivery in insulated packaging. Asparagus bundles wrapped in damp paper to maintain turgidity during transit.",
         "Temperature": "0–6 °C", "Duration": "3 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P005": [  # Strawberries CP Select
        {"Product_ID": "P005", "Step_Order": 1, "Stage": "Farm Origin",
         "Location": "Dandong, Liaoning", "Date": "2026-03-11",
         "Description": "CP Select strawberries grown in Dandong's famous Donggang strawberry belt using drip irrigation and natural pest management under CP's certified supplier programme.",
         "Temperature": "14–20 °C", "Duration": "40 days", "Vehicle": None, "Certifications": "GAP Certified, CP Select Certified"},
        {"Product_ID": "P005", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Dandong, Liaoning", "Date": "2026-03-13",
         "Description": "Hand-picked at ≥80% red colour. Sugar content (Brix ≥9.0) verified by refractometer at field station. Damaged or under-ripe berries culled.",
         "Temperature": "12–18 °C", "Duration": "5 hours", "Vehicle": None, "Certifications": "GAP Certified"},
        {"Product_ID": "P005", "Step_Order": 3, "Stage": "Cold Storage",
         "Location": "Shenyang, Liaoning", "Date": "2026-03-13",
         "Description": "Rapid blast-chilling to 0–2 °C within 2 hours of harvest. Punnets sealed with modified-atmosphere film to extend shelf life by 3 days.",
         "Temperature": "0–2 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P005", "Step_Order": 4, "Stage": "Cold Chain Transit",
         "Location": "Beijing", "Date": "2026-03-14",
         "Description": "Refrigerated truck transports overnight; temperature logged continuously. Custom berry-spec foam packing prevents bruising on mountain and highway roads.",
         "Temperature": "0–4 °C", "Duration": "10 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P005", "Step_Order": 5, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-15",
         "Description": "Priority inbound at Shanghai DC. Assigned to earliest dispatch wave; berry lots never held more than 8 hours at the DC.",
         "Temperature": "0–4 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P005", "Step_Order": 6, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-03-15",
         "Description": "Sensory evaluation and visual grading pass. Pesticide residue multi-screen cleared before consumer release per CP Select standards.",
         "Temperature": "0–4 °C", "Duration": "2 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P005", "Step_Order": 7, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-16",
         "Description": "Delivered in strawberry-spec insulated box with gel packs. Handled manually to prevent bruising. Delivered within 2-hour slot.",
         "Temperature": "0–6 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P006": [  # Japanese Kyoho Grapes
        {"Product_ID": "P006", "Step_Order": 1, "Stage": "Vineyard Origin",
         "Location": "Yamanashi, Japan", "Date": "2026-02-10",
         "Description": "Kyoho grapes cultivated in Yamanashi Prefecture — Japan's premier table grape region. Each vine hand-tended; cluster thinning ensures supersized, uniform berries.",
         "Temperature": "18–28 °C", "Duration": "120 days", "Vehicle": None, "Certifications": "Japan GAP, JAS Organic"},
        {"Product_ID": "P006", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Yamanashi, Japan", "Date": "2026-02-18",
         "Description": "Clusters hand-snipped and inspected berry-by-berry. Only uniform clusters meeting CP's import specification (≥25 g/berry, Brix ≥18) are selected.",
         "Temperature": "20–25 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "Japan GAP"},
        {"Product_ID": "P006", "Step_Order": 3, "Stage": "Packaging & Pre-Cooling",
         "Location": "Tokyo, Japan", "Date": "2026-02-19",
         "Description": "Clusters packed in single-layer trays with cushioned inserts. Pre-cooled to 2–4 °C overnight before loading into temperature-controlled export containers.",
         "Temperature": "2–4 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P006", "Step_Order": 4, "Stage": "Air Freight",
         "Location": "Tokyo, Japan", "Date": "2026-02-20",
         "Description": "Express air freight from Narita Airport in chilled cargo hold. Approx. 3-hour flight; temperature monitored via active data logger in each pallet.",
         "Temperature": "2–4 °C", "Duration": "5 hours", "Vehicle": "Air Freight", "Certifications": "IATA Perishable Cargo"},
        {"Product_ID": "P006", "Step_Order": 5, "Stage": "Import Customs",
         "Location": "Shanghai", "Date": "2026-02-20",
         "Description": "Cleared at Pudong International Cargo Terminal. Plant quarantine, import health certificate, and pesticide MRL screen verified. GACC-registered exporter pre-approved.",
         "Temperature": "2–4 °C", "Duration": "5 hours", "Vehicle": None, "Certifications": "GACC Registered, HACCP"},
        {"Product_ID": "P006", "Step_Order": 6, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-02-21",
         "Description": "Incoming QC: Brix verification, berry uniformity check, and pesticide multi-residue screen (all results <10% MRL). Cleared for retail.",
         "Temperature": "2–4 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P006", "Step_Order": 7, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-02-22",
         "Description": "Delivered in rigid berry gift box with gel packs. White-glove handling to prevent skin damage. Priority 2-hour delivery slot.",
         "Temperature": "2–8 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P007": [  # Mango (Ataulfo)
        {"Product_ID": "P007", "Step_Order": 1, "Stage": "Farm Origin",
         "Location": "Hainan, China", "Date": "2026-03-06",
         "Description": "Ataulfo mangoes grown in Hainan's tropical climate under CP's sustainable agriculture programme. Drip-irrigated with no post-harvest wax treatment.",
         "Temperature": "28–35 °C", "Duration": "90 days", "Vehicle": None, "Certifications": "GAP Certified, Green Food"},
        {"Product_ID": "P007", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Hainan, China", "Date": "2026-03-09",
         "Description": "Hand-picked at commercial maturity (firmness index 60–80 N). Graded by size, colour, and absence of defects. Only Grade A fruit forwarded.",
         "Temperature": "30–35 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "GAP Certified"},
        {"Product_ID": "P007", "Step_Order": 3, "Stage": "Ripening Control",
         "Location": "Guangzhou", "Date": "2026-03-10",
         "Description": "Ethylene-assisted ripening room brings fruit to eating-ripe stage (Brix ≥14). Controlled at 20–22 °C for 48 hours before packaging.",
         "Temperature": "20–22 °C", "Duration": "48 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P007", "Step_Order": 4, "Stage": "Distribution Center",
         "Location": "Guangzhou", "Date": "2026-03-12",
         "Description": "Packed and lot-coded at Guangzhou DC. FIFO dispatch to Shanghai fulfilment hub initiated same day.",
         "Temperature": "13–15 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P007", "Step_Order": 5, "Stage": "Cold Chain Transit",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Refrigerated truck at 13–15 °C — critical for mango to avoid chilling injury while maintaining peak flavour and texture.",
         "Temperature": "13–15 °C", "Duration": "24 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P007", "Step_Order": 6, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-15",
         "Description": "Delivered in temperature-managed packaging. Mango at peak eating ripeness on arrival.",
         "Temperature": "13–18 °C", "Duration": "3 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P008": [  # Blueberries CP Select
        {"Product_ID": "P008", "Step_Order": 1, "Stage": "Farm Origin",
         "Location": "Guizhou, China", "Date": "2026-03-09",
         "Description": "CP Select blueberries cultivated at high altitude in Guizhou on naturally acidic soil (pH 4.5–5.5). No synthetic pesticides; drip-irrigated under CP supplier programme.",
         "Temperature": "15–22 °C", "Duration": "30 days", "Vehicle": None, "Certifications": "GAP Certified, CP Select Certified, Organic China"},
        {"Product_ID": "P008", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Guizhou, China", "Date": "2026-03-11",
         "Description": "Machine-assisted harvest followed by manual sorting. Berries graded by size (≥16 mm), colour uniformity, and Brix (≥12). Soft or damaged berries removed.",
         "Temperature": "18–24 °C", "Duration": "5 hours", "Vehicle": None, "Certifications": "GAP Certified"},
        {"Product_ID": "P008", "Step_Order": 3, "Stage": "Pre-Cooling",
         "Location": "Guiyang, Guizhou", "Date": "2026-03-11",
         "Description": "Rapid forced-air pre-cooling to 1–2 °C within 2 hours of harvest. Packed in 125 g punnets with breathable film to maintain bloom.",
         "Temperature": "1–2 °C", "Duration": "2 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P008", "Step_Order": 4, "Stage": "Cold Chain Transit",
         "Location": "Chongqing", "Date": "2026-03-12",
         "Description": "Refrigerated truck transports overnight through mountain roads. Temperature logged every 10 minutes; deviation alerts sent to CP logistics team in real time.",
         "Temperature": "0–4 °C", "Duration": "14 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P008", "Step_Order": 5, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Received at Shanghai DC. Berries checked for bloom (waxy coating) integrity as freshness indicator. Allocated to priority dispatch wave.",
         "Temperature": "0–4 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P008", "Step_Order": 6, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Final QC: Brix check, pesticide residue screen, and visual grading. CP Select standard requires ≤2% defects per punnet.",
         "Temperature": "0–4 °C", "Duration": "2 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P008", "Step_Order": 7, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-15",
         "Description": "Delivered in insulated blueberry-spec box. Bloom-intact berries arrive in perfect condition within 2-hour guaranteed slot.",
         "Temperature": "0–6 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P009": [  # Wild-Caught King Salmon Fillet
        {"Product_ID": "P009", "Step_Order": 1, "Stage": "Wild Catch",
         "Location": "New Zealand", "Date": "2026-03-03",
         "Description": "Sustainably wild-caught King (Chinook) salmon from New Zealand's pristine south island waters. MSC-certified fishery with strict daily catch quotas and observer programme.",
         "Temperature": "0–2 °C", "Duration": "12 hours", "Vehicle": "Fishing Vessel", "Certifications": "MSC Certified, Wild Catch Certified"},
        {"Product_ID": "P009", "Step_Order": 2, "Stage": "On-board Processing",
         "Location": "New Zealand", "Date": "2026-03-03",
         "Description": "Bled, gutted, and iced on-board within 30 minutes of catch. Super-chilled at -1 to 0 °C throughout the return voyage to port.",
         "Temperature": "-1–0 °C", "Duration": "6 hours", "Vehicle": "Fishing Vessel", "Certifications": "HACCP"},
        {"Product_ID": "P009", "Step_Order": 3, "Stage": "Processing Facility",
         "Location": "Auckland, New Zealand", "Date": "2026-03-04",
         "Description": "HACCP-certified shore-side facility. Filleted to ±5 g weight tolerance, pin-boned, skin-on. Batch code assigned and cold-chain timer started.",
         "Temperature": "0–2 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000, MSC Certified"},
        {"Product_ID": "P009", "Step_Order": 4, "Stage": "Air Freight",
         "Location": "Auckland, New Zealand", "Date": "2026-03-05",
         "Description": "Vacuum-packed fillets air-freighted in active-cooling containers from Auckland Airport. Transit temperature maintained at 0–2 °C throughout 11-hour flight.",
         "Temperature": "0–2 °C", "Duration": "14 hours", "Vehicle": "Air Freight", "Certifications": "IATA Perishable Cargo"},
        {"Product_ID": "P009", "Step_Order": 5, "Stage": "Import Customs",
         "Location": "Shanghai", "Date": "2026-03-06",
         "Description": "GACC-registered NZ exporter; cleared via priority green lane. Veterinary health certificate and cold-chain log verified. Temperature intact throughout.",
         "Temperature": "0–2 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "GACC Registered, ISO 22000"},
        {"Product_ID": "P009", "Step_Order": 6, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-03-06",
         "Description": "Incoming inspection: sensory evaluation (colour, odour, texture), microbiological screen, heavy metals check. All results within specification.",
         "Temperature": "0–2 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P009", "Step_Order": 7, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-07",
         "Description": "Delivered on dry ice in insulated seafood box within 2-hour slot. Fisherman-to-door traceability QR code visible on every package.",
         "Temperature": "-1–2 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P010": [  # Tiger Prawns (Frozen)
        {"Product_ID": "P010", "Step_Order": 1, "Stage": "Aquaculture Farm",
         "Location": "Zhanjiang, Guangdong", "Date": "2026-02-20",
         "Description": "Black tiger prawns reared in certified aquaculture ponds in Zhanjiang — China's 'Capital of Prawns'. Antibiotic-free growth cycle; water quality monitored daily.",
         "Temperature": "26–30 °C", "Duration": "90 days", "Vehicle": None, "Certifications": "ASC Certified, GAP Certified"},
        {"Product_ID": "P010", "Step_Order": 2, "Stage": "Harvest & Grading",
         "Location": "Zhanjiang, Guangdong", "Date": "2026-02-22",
         "Description": "Prawns harvested by seine net and immediately transferred to iced transport tanks. Size-graded (16/20 count per kg) and head-on integrity checked.",
         "Temperature": "0–4 °C", "Duration": "5 hours", "Vehicle": None, "Certifications": "ASC Certified"},
        {"Product_ID": "P010", "Step_Order": 3, "Stage": "Processing & IQF Freezing",
         "Location": "Guangzhou", "Date": "2026-02-23",
         "Description": "Head-on shell-on prawns processed at HACCP facility. IQF (Individually Quick Frozen) at -35 °C in 12 minutes — preserving texture and flavour better than block freezing.",
         "Temperature": "-35 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000, ASC Certified"},
        {"Product_ID": "P010", "Step_Order": 4, "Stage": "Frozen Storage",
         "Location": "Guangzhou", "Date": "2026-02-25",
         "Description": "Stored at -18 °C in automated cold warehouse with 24/7 temperature monitoring and digital FIFO batch management.",
         "Temperature": "-18 °C", "Duration": "5 days", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P010", "Step_Order": 5, "Stage": "Cold Chain Transit",
         "Location": "Shanghai", "Date": "2026-03-02",
         "Description": "Reefer container transported to Shanghai. Frozen at -18 °C throughout; temperature logger data archived with lot record.",
         "Temperature": "-18 °C", "Duration": "24 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P010", "Step_Order": 6, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-03",
         "Description": "Received at CP's frozen DC in Shanghai. Stored in blast-freeze zone pending consumer orders.",
         "Temperature": "-18 °C", "Duration": "14 days", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P010", "Step_Order": 7, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-17",
         "Description": "Delivered in dry-ice insulated box. Freshness seal intact on arrival; consumer receives product at ≤-12 °C throughout the 2-hour delivery window.",
         "Temperature": "-12 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P011": [  # Hokkaido Scallops
        {"Product_ID": "P011", "Step_Order": 1, "Stage": "Sea Harvest",
         "Location": "Hokkaido, Japan", "Date": "2026-01-10",
         "Description": "Hokkaido hotate scallops dredge-harvested from the nutrient-rich Sea of Okhotsk. Hokkaido Marine Fishery Co-op certification ensures sustainable harvest quotas.",
         "Temperature": "2–8 °C (sea)", "Duration": "8 hours", "Vehicle": "Fishing Vessel", "Certifications": "MSC Certified, Japan GAP"},
        {"Product_ID": "P011", "Step_Order": 2, "Stage": "Processing Facility",
         "Location": "Hokkaido, Japan", "Date": "2026-01-11",
         "Description": "Shucked and roe-off processed at licensed Hokkaido seafood plant. Adductor muscle graded by size (3S–3L). Lot batch-coded for export.",
         "Temperature": "0–2 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000, MSC Certified"},
        {"Product_ID": "P011", "Step_Order": 3, "Stage": "IQF Freezing",
         "Location": "Hokkaido, Japan", "Date": "2026-01-12",
         "Description": "IQF frozen at -40 °C in spiral freezer to lock in natural sweetness and coral-white colour. Each scallop individually sealed and glazed.",
         "Temperature": "-40 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P011", "Step_Order": 4, "Stage": "Sea Freight",
         "Location": "Osaka, Japan", "Date": "2026-01-14",
         "Description": "Loaded into -18 °C reefer container at Osaka Port. 5-day sea voyage to Shanghai with continuous temperature monitoring and logging.",
         "Temperature": "-18 °C", "Duration": "5 days", "Vehicle": "Reefer Container Ship", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P011", "Step_Order": 5, "Stage": "Import Customs",
         "Location": "Shanghai", "Date": "2026-01-20",
         "Description": "Received at Waigaoqiao cold storage terminal. GACC-registered Japanese exporter; health certificate and fishing area documentation verified. Quarantine sampling passed.",
         "Temperature": "-18 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "GACC Registered, HACCP"},
        {"Product_ID": "P011", "Step_Order": 6, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-01-21",
         "Description": "Incoming QC: sensory scoring (sweetness, firmness, glaze uniformity), microbiological test, heavy metals screen — all within CFDA limits.",
         "Temperature": "-18 °C", "Duration": "24 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P011", "Step_Order": 7, "Stage": "Frozen Storage",
         "Location": "Shanghai", "Date": "2026-01-22",
         "Description": "Stored at -18 °C in CP's Shanghai cold hub awaiting order dispatch. FIFO rotation managed digitally to maintain freshness sequence.",
         "Temperature": "-18 °C", "Duration": "55 days", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P011", "Step_Order": 8, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-17",
         "Description": "Shipped with dry ice in premium seafood gift box. Delivered within 2-hour priority slot; maintains -12 °C or below on arrival.",
         "Temperature": "-12 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P012": [  # Free-Range Eggs CP Select
        {"Product_ID": "P012", "Step_Order": 1, "Stage": "CP Group Poultry Farm",
         "Location": "Henan, China", "Date": "2026-03-13",
         "Description": "Eggs laid by free-range hens at CP's Henan poultry farm. Hens raised cage-free on 3 m²/bird, fed CP-formulated non-GMO feed. Antibiotic-free flock health programme.",
         "Temperature": "Ambient (18–24 °C)", "Duration": "1 day", "Vehicle": None, "Certifications": "CP Select Certified, Free-Range Certified, GAP Certified"},
        {"Product_ID": "P012", "Step_Order": 2, "Stage": "Collection & Grading",
         "Location": "Henan, China", "Date": "2026-03-13",
         "Description": "Eggs collected twice daily, conveyor-graded by weight (L: 63–72 g), candled for internal quality, and checked for shell integrity. Substandard eggs rejected.",
         "Temperature": "15–18 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P012", "Step_Order": 3, "Stage": "Packaging",
         "Location": "Zhengzhou, Henan", "Date": "2026-03-14",
         "Description": "Stamped with lay date, best-before date (28 days), and CP Select QR traceability code. Packed in 6-egg moulded pulp tray.",
         "Temperature": "8–12 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P012", "Step_Order": 4, "Stage": "Cold Chain Transit",
         "Location": "Tianjin", "Date": "2026-03-15",
         "Description": "Refrigerated transport maintains 8–12 °C to prevent condensation and shell contamination. Eggs handled in padded trays to prevent breakage.",
         "Temperature": "8–12 °C", "Duration": "10 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P012", "Step_Order": 5, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-16",
         "Description": "Received at Shanghai DC. FIFO dispatch ensures no egg exceeds 5 days from lay to consumer.",
         "Temperature": "8–12 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P012", "Step_Order": 6, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-17",
         "Description": "Delivered in foam egg box, handled upright as marked. Consumer receives eggs within 4 days of lay — fresher than typical supermarket shelf average.",
         "Temperature": "8–15 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P013": [  # Greek Yoghurt (Plain)
        {"Product_ID": "P013", "Step_Order": 1, "Stage": "Milk Collection",
         "Location": "Hebei, China", "Date": "2026-03-09",
         "Description": "Fresh whole milk collected from CP's contracted dairy farms in Hebei. Cows raised on pasture; no rBST hormones. Milk tested for somatic cell count and antibiotic residues at farm.",
         "Temperature": "4 °C", "Duration": "1 day", "Vehicle": "Milk Tanker", "Certifications": "GAP Certified, Dairy Farm Standard"},
        {"Product_ID": "P013", "Step_Order": 2, "Stage": "Pasteurization",
         "Location": "Beijing", "Date": "2026-03-10",
         "Description": "HTST pasteurization at 72 °C for 15 seconds at CP's Beijing processing plant. Protein content standardised to ≥3.8 g/100 ml; fat adjusted for Greek-style thickness.",
         "Temperature": "72 °C → 4 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P013", "Step_Order": 3, "Stage": "Fermentation & Production",
         "Location": "Shanghai", "Date": "2026-03-11",
         "Description": "Inoculated with proprietary Lactobacillus bulgaricus and Streptococcus thermophilus blend. Fermented at 42 °C for 5 hours, then strained to achieve thick Greek-style texture.",
         "Temperature": "42 °C → 4 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P013", "Step_Order": 4, "Stage": "Quality Testing",
         "Location": "Shanghai", "Date": "2026-03-11",
         "Description": "Lab testing: total viable count, yeast/mould, pH (4.3–4.6), protein (≥5.6 g/100 g), and sensory panel evaluation. Batch released only on full pass.",
         "Temperature": "4 °C", "Duration": "6 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P013", "Step_Order": 5, "Stage": "Packaging",
         "Location": "Shanghai", "Date": "2026-03-12",
         "Description": "Filled into 400 g resealable tubs under clean-room conditions. Sealed with tamper-evident foil; best-before date (21 days) printed on lid.",
         "Temperature": "4 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P013", "Step_Order": 6, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-13",
         "Description": "Delivered in CP's cold-bag system within 4-hour window. Consumer receives product just 2 days from production — far fresher than typical retail shelf yoghurt.",
         "Temperature": "2–8 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P014": [  # Wagyu Beef Ribeye A4
        {"Product_ID": "P014", "Step_Order": 1, "Stage": "Cattle Farm",
         "Location": "Victoria, Australia", "Date": "2026-01-15",
         "Description": "Wagyu-Angus F1 cross cattle raised on Victoria's pasture for 18 months, then grain-finished for 300+ days. Each animal registered with Wagyu Australia breed register.",
         "Temperature": "Ambient", "Duration": "300 days feedlot", "Vehicle": None, "Certifications": "Wagyu Australia Registered, HGP-Free"},
        {"Product_ID": "P014", "Step_Order": 2, "Stage": "Feedlot Finishing",
         "Location": "Victoria, Australia", "Date": "2026-01-20",
         "Description": "300-day grain-finishing programme with CP-formulated barley-based ration. Marbling development monitored by ultrasound at 100-day intervals.",
         "Temperature": "Ambient", "Duration": "300 days", "Vehicle": None, "Certifications": "HGP-Free, Wagyu Australia Registered"},
        {"Product_ID": "P014", "Step_Order": 3, "Stage": "Slaughter & Processing",
         "Location": "Melbourne, Australia", "Date": "2026-02-01",
         "Description": "Processed at ESCAS-accredited, HACCP-certified Melbourne abattoir. Carcass scored A4 by AUS-MEAT accredited grader. Primal ribeye cut and vacuum-packed within 2 hours.",
         "Temperature": "0–2 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000, AUS-MEAT Graded"},
        {"Product_ID": "P014", "Step_Order": 4, "Stage": "Vacuum Packing & Wet Ageing",
         "Location": "Melbourne, Australia", "Date": "2026-02-02",
         "Description": "Wet-aged under vacuum at 0–2 °C for 14 days. Natural enzymes break down connective tissue, enhancing tenderness. Each bag labelled with kill date and lot code.",
         "Temperature": "0–2 °C", "Duration": "14 days", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P014", "Step_Order": 5, "Stage": "Sea Freight",
         "Location": "Melbourne, Australia", "Date": "2026-02-16",
         "Description": "Loaded into AFAM-compliant reefer containers at Melbourne Port. 14-day voyage to Shanghai under continuous 0–2 °C cold chain.",
         "Temperature": "0–2 °C", "Duration": "14 days", "Vehicle": "Reefer Container Ship", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P014", "Step_Order": 6, "Stage": "Import Customs",
         "Location": "Shanghai", "Date": "2026-03-02",
         "Description": "Cleared via GACC-registered Australian beef exporter lane. Veterinary health certificate and export documentation verified. Quarantine inspection passed.",
         "Temperature": "0–2 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "GACC Registered, HACCP"},
        {"Product_ID": "P014", "Step_Order": 7, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-03-03",
         "Description": "In-house inspection: marbling score verification (IMF ≥18%), sensory pass, microbiological screen, and drug residue multi-panel. Batch cleared for premium retail.",
         "Temperature": "0–2 °C", "Duration": "24 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP, AUS-MEAT Graded"},
        {"Product_ID": "P014", "Step_Order": 8, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-04",
         "Description": "White-glove cold delivery in insulated premium box with dry ice. Dedicated 2-hour priority slot. Marbling card and QR traceability certificate included in package.",
         "Temperature": "0–4 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
    "P015": [  # Chilled Chicken Breast CP Select
        {"Product_ID": "P015", "Step_Order": 1, "Stage": "CP Group Poultry Farm",
         "Location": "Hebei, China", "Date": "2026-03-11",
         "Description": "Broiler chickens raised at CP Group's vertically integrated Hebei farm. Antibiotic growth promoter-free; fed CP-formulated corn-soy ration. Biosecurity Level 3 facility.",
         "Temperature": "Ambient (18–22 °C)", "Duration": "42 days", "Vehicle": None, "Certifications": "CP Select Certified, GAP Certified, Antibiotic-Free"},
        {"Product_ID": "P015", "Step_Order": 2, "Stage": "Veterinary Inspection",
         "Location": "Hebei, China", "Date": "2026-03-12",
         "Description": "Ante-mortem and post-mortem inspection by licensed government veterinarian. 100% carcass inspection; residue surveillance sampling per NMPA protocol.",
         "Temperature": "Ambient", "Duration": "4 hours", "Vehicle": None, "Certifications": "Government Veterinary Certified, HACCP"},
        {"Product_ID": "P015", "Step_Order": 3, "Stage": "Slaughter & Processing",
         "Location": "Tianjin", "Date": "2026-03-12",
         "Description": "Processed at CP's HACCP-certified Tianjin plant. Deboning line yields consistent 185–215 g skinless chicken breast fillets. Batch code assigned to each tray.",
         "Temperature": "0–4 °C", "Duration": "8 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000, Halal Certified"},
        {"Product_ID": "P015", "Step_Order": 4, "Stage": "Chilling & Packaging",
         "Location": "Tianjin", "Date": "2026-03-13",
         "Description": "Chilled to ≤4 °C within 4 hours of processing. MAP-packed in modified-atmosphere trays (60% CO₂ / 40% N₂) to extend shelf life to 7 days from pack date.",
         "Temperature": "0–4 °C", "Duration": "4 hours", "Vehicle": None, "Certifications": "ISO 22000"},
        {"Product_ID": "P015", "Step_Order": 5, "Stage": "Cold Chain Transit",
         "Location": "Beijing", "Date": "2026-03-13",
         "Description": "Loaded onto refrigerated truck for overnight transit to Beijing hub. In-cab temperature logger records every 5 minutes; deviation triggers driver alert.",
         "Temperature": "0–4 °C", "Duration": "4 hours", "Vehicle": "Refrigerated Truck", "Certifications": "Cold Chain Certified"},
        {"Product_ID": "P015", "Step_Order": 6, "Stage": "Distribution Center",
         "Location": "Shanghai", "Date": "2026-03-14",
         "Description": "Received at CP's Shanghai fulfilment centre. Lot allocated to same-day consumer dispatch wave; no lot held more than 12 hours.",
         "Temperature": "0–4 °C", "Duration": "12 hours", "Vehicle": None, "Certifications": "HACCP, ISO 22000"},
        {"Product_ID": "P015", "Step_Order": 7, "Stage": "Quality Inspection",
         "Location": "Shanghai", "Date": "2026-03-15",
         "Description": "Final QC: colour assessment (pinkish-white), package integrity, MAP gas ratio check, and random microbiological sampling. Cleared for consumer release.",
         "Temperature": "0–4 °C", "Duration": "3 hours", "Vehicle": None, "Certifications": "ISO 22000, HACCP"},
        {"Product_ID": "P015", "Step_Order": 8, "Stage": "Last-Mile Delivery",
         "Location": "Shanghai", "Date": "2026-03-16",
         "Description": "Delivered in insulated bag with cold pack. Farm-to-door in under 5 days; MAP seal intact on delivery. Consumer receives product 3 days before best-before date.",
         "Temperature": "0–6 °C", "Duration": "2 hours", "Vehicle": "Insulated Delivery Van", "Certifications": "Cold Chain Certified"},
    ],
}


def get_traceability(product_id: str) -> list[dict]:
    pid = str(product_id).strip().upper()
    # Try Excel / in-memory data first
    excel_rows = [
        row for row in _data["traceability"]
        if str(row.get("Product_ID", "")).strip().upper() == pid
    ]
    if excel_rows:
        return excel_rows
    # Fall back to hardcoded trace data for all 15 products
    return _TRACE_DATA.get(pid, [])


def get_market_data() -> list[dict]:
    return _data["market_data"]


def get_opportunities() -> list[dict]:
    return _data["opportunities"]


def get_personas() -> list[dict]:
    return _data["personas"]


# ---------------------------------------------------------------------------
# Inventory — fully self-contained hardcoded dataset (no Excel dependency)
# ---------------------------------------------------------------------------

_INVENTORY_DATA: list[dict] = [
    # ── Vegetables ──────────────────────────────────────────────────────────
    {
        "Product_ID": "P001", "Product_Name": "Organic Baby Spinach",
        "Category": "Vegetables", "Sub_Category": "Leafy Greens",
        "Unit": "bag (200g)", "Price_CNY": 18.9,
        "Stock_Status": "In Stock",  "Stock_Qty": 312,
        "Sales_7D": 68,  "Sales_30D": 274, "Revenue_30D": 5172.6,
        "Last_Restocked": "2026-03-10",
    },
    {
        "Product_ID": "P002", "Product_Name": "Heirloom Tomatoes",
        "Category": "Vegetables", "Sub_Category": "Fruiting Veg",
        "Unit": "punnet (500g)", "Price_CNY": 24.5,
        "Stock_Status": "Out of Stock", "Stock_Qty": 0,
        "Sales_7D": 0,   "Sales_30D": 0,   "Revenue_30D": 0.0,
        "Last_Restocked": "2026-02-14",
    },
    {
        "Product_ID": "P003", "Product_Name": "Sweet Corn (3-pack)",
        "Category": "Vegetables", "Sub_Category": "Corn & Root",
        "Unit": "pack (3 ears)", "Price_CNY": 12.8,
        "Stock_Status": "In Stock",  "Stock_Qty": 185,
        "Sales_7D": 42,  "Sales_30D": 163, "Revenue_30D": 2086.4,
        "Last_Restocked": "2026-03-12",
    },
    {
        "Product_ID": "P004", "Product_Name": "Purple Asparagus",
        "Category": "Vegetables", "Sub_Category": "Specialty Veg",
        "Unit": "bundle (250g)", "Price_CNY": 38.0,
        "Stock_Status": "Out of Stock", "Stock_Qty": 0,
        "Sales_7D": 0,   "Sales_30D": 0,   "Revenue_30D": 0.0,
        "Last_Restocked": "2026-01-28",
    },
    # ── Fruits ──────────────────────────────────────────────────────────────
    {
        "Product_ID": "P005", "Product_Name": "Strawberries CP Select",
        "Category": "Fruits", "Sub_Category": "Berries",
        "Unit": "punnet (300g)", "Price_CNY": 29.9,
        "Stock_Status": "In Stock",  "Stock_Qty": 421,
        "Sales_7D": 95,  "Sales_30D": 388, "Revenue_30D": 11601.2,
        "Last_Restocked": "2026-03-15",
    },
    {
        "Product_ID": "P006", "Product_Name": "Japanese Kyoho Grapes",
        "Category": "Fruits", "Sub_Category": "Grapes",
        "Unit": "cluster (500g)", "Price_CNY": 88.0,
        "Stock_Status": "Out of Stock", "Stock_Qty": 0,
        "Sales_7D": 0,   "Sales_30D": 0,   "Revenue_30D": 0.0,
        "Last_Restocked": "2026-02-05",
    },
    {
        "Product_ID": "P007", "Product_Name": "Mango (Ataulfo)",
        "Category": "Fruits", "Sub_Category": "Tropical",
        "Unit": "piece (avg 350g)", "Price_CNY": 22.0,
        "Stock_Status": "In Stock",  "Stock_Qty": 78,
        "Sales_7D": 21,  "Sales_30D": 84,  "Revenue_30D": 1848.0,
        "Last_Restocked": "2026-03-08",
    },
    {
        "Product_ID": "P008", "Product_Name": "Blueberries CP Select",
        "Category": "Fruits", "Sub_Category": "Berries",
        "Unit": "punnet (125g)", "Price_CNY": 35.5,
        "Stock_Status": "In Stock",  "Stock_Qty": 256,
        "Sales_7D": 53,  "Sales_30D": 211, "Revenue_30D": 7490.5,
        "Last_Restocked": "2026-03-14",
    },
    # ── Seafood ─────────────────────────────────────────────────────────────
    {
        "Product_ID": "P009", "Product_Name": "Wild-Caught King Salmon Fillet",
        "Category": "Seafood", "Sub_Category": "Fish",
        "Unit": "fillet (400g)", "Price_CNY": 168.0,
        "Stock_Status": "Out of Stock", "Stock_Qty": 0,
        "Sales_7D": 0,   "Sales_30D": 0,   "Revenue_30D": 0.0,
        "Last_Restocked": "2026-02-20",
    },
    {
        "Product_ID": "P010", "Product_Name": "Tiger Prawns (Frozen)",
        "Category": "Seafood", "Sub_Category": "Shellfish",
        "Unit": "bag (500g)", "Price_CNY": 89.0,
        "Stock_Status": "In Stock",  "Stock_Qty": 134,
        "Sales_7D": 31,  "Sales_30D": 127, "Revenue_30D": 11303.0,
        "Last_Restocked": "2026-03-11",
    },
    {
        "Product_ID": "P011", "Product_Name": "Hokkaido Scallops",
        "Category": "Seafood", "Sub_Category": "Shellfish",
        "Unit": "tray (300g)", "Price_CNY": 198.0,
        "Stock_Status": "Out of Stock", "Stock_Qty": 0,
        "Sales_7D": 0,   "Sales_30D": 0,   "Revenue_30D": 0.0,
        "Last_Restocked": "2026-01-15",
    },
    # ── Dairy & Eggs ────────────────────────────────────────────────────────
    {
        "Product_ID": "P012", "Product_Name": "Free-Range Eggs CP Select",
        "Category": "Dairy & Eggs", "Sub_Category": "Eggs",
        "Unit": "6-pack", "Price_CNY": 22.9,
        "Stock_Status": "In Stock",  "Stock_Qty": 509,
        "Sales_7D": 112, "Sales_30D": 445, "Revenue_30D": 10190.5,
        "Last_Restocked": "2026-03-16",
    },
    {
        "Product_ID": "P013", "Product_Name": "Greek Yoghurt (Plain)",
        "Category": "Dairy & Eggs", "Sub_Category": "Yoghurt",
        "Unit": "tub (400g)", "Price_CNY": 28.0,
        "Stock_Status": "In Stock",  "Stock_Qty": 67,
        "Sales_7D": 18,  "Sales_30D": 72,  "Revenue_30D": 2016.0,
        "Last_Restocked": "2026-03-09",
    },
    # ── Meat ────────────────────────────────────────────────────────────────
    {
        "Product_ID": "P014", "Product_Name": "Wagyu Beef Ribeye A4",
        "Category": "Meat", "Sub_Category": "Beef",
        "Unit": "slice pack (200g)", "Price_CNY": 328.0,
        "Stock_Status": "Out of Stock", "Stock_Qty": 0,
        "Sales_7D": 0,   "Sales_30D": 0,   "Revenue_30D": 0.0,
        "Last_Restocked": "2026-02-01",
    },
    {
        "Product_ID": "P015", "Product_Name": "Chilled Chicken Breast CP Select",
        "Category": "Meat", "Sub_Category": "Poultry",
        "Unit": "pack (500g)", "Price_CNY": 45.0,
        "Stock_Status": "In Stock",  "Stock_Qty": 198,
        "Sales_7D": 44,  "Sales_30D": 178, "Revenue_30D": 8010.0,
        "Last_Restocked": "2026-03-13",
    },
]


def get_inventory() -> list[dict]:
    """Return the hardcoded inventory + sales dataset.

    Fully self-contained — does NOT depend on Excel data being loaded.
    If the Excel products sheet was loaded successfully, dynamically
    override Price_CNY and Product_Name from live data where available.
    """
    # Build a quick lookup from live product data (may be empty)
    live: dict[str, dict] = {}
    for p in _data.get("products", []):
        pid = str(p.get("Product_ID", "")).strip().upper()
        if pid:
            live[pid] = p

    result = []
    for item in _INVENTORY_DATA:
        row = dict(item)  # copy so we don't mutate the master list
        pid = row["Product_ID"]
        if pid in live:
            # Prefer live names / prices if available
            live_name = live[pid].get("Product_Name") or live[pid].get("Name_EN")
            if live_name:
                row["Product_Name"] = live_name
            live_price = live[pid].get("Price_CNY")
            if live_price:
                row["Price_CNY"] = live_price
                row["Revenue_30D"] = round(row["Sales_30D"] * live_price, 2)
        result.append(row)
    return result
