from __future__ import annotations

import datetime
from typing import Any

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import data_loader

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------
app = FastAPI(title="CP Group Fresh Food Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Auth constants
# ---------------------------------------------------------------------------
JWT_SECRET = "cp-group-secret-2026"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# Hardcoded users  {username: (hashed_password, role)}
_USERS: dict[str, tuple[str, str]] = {
    "admin": (pwd_context.hash("admin123"), "ADMIN"),
    "analyst": (pwd_context.hash("analyst123"), "ANALYST"),
    "consumer": (pwd_context.hash("consumer123"), "CONSUMER"),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _ok(data: Any) -> dict:
    return {"code": 200, "message": "success", "data": data, "timestamp": _now_iso()}


def _make_token(username: str, role: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return _decode_token(token)


def require_analyst(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") not in ("ADMIN", "ANALYST"):
        raise HTTPException(status_code=403, detail="Analyst or Admin role required")
    return current_user


# ---------------------------------------------------------------------------
# Startup: load xlsx data
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    data_loader.load_all()


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/v1/auth/login")
async def login(body: LoginRequest):
    user = _USERS.get(body.username)
    if not user or not pwd_context.verify(body.password, user[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    role = user[1]
    token = _make_token(body.username, role)
    return _ok({"token": token, "role": role, "username": body.username})


# ---------------------------------------------------------------------------
# Data endpoints (no auth required for demo)
# ---------------------------------------------------------------------------
@app.get("/api/v1/competitors")
async def get_competitors():
    return _ok(data_loader.get_competitors())


@app.get("/api/v1/products")
async def get_products():
    return _ok(data_loader.get_products())


@app.get("/api/v1/products/{product_id}/traceability")
async def get_traceability(product_id: str):
    nodes = data_loader.get_traceability(product_id)
    return _ok(nodes)


@app.get("/api/v1/market-data")
async def get_market_data():
    return _ok(data_loader.get_market_data())


@app.get("/api/v1/opportunities")
async def get_opportunities():
    return _ok(data_loader.get_opportunities())


@app.get("/api/v1/personas")
async def get_personas():
    return _ok(data_loader.get_personas())


@app.get("/api/v1/inventory")
async def get_inventory(current_user: dict = Depends(require_analyst)):
    return _ok(data_loader.get_inventory())


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "timestamp": _now_iso()}
