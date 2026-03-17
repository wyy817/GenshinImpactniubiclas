<template>
  <!-- Floating Action Button -->
  <Teleport to="body">
    <div class="report-fab" @click="dialogVisible = true" title="Open Report Editor">
      <el-icon size="16"><Document /></el-icon>
      <span>Report</span>
    </div>

    <!-- Draggable Floating Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="false"
      :show-close="false"
      draggable
      :modal="false"
      width="620px"
      class="report-dialog"
      :append-to-body="true"
    >
      <!-- Custom Header -->
      <template #header>
        <div class="report-dialog-header">
          <div class="header-left">
            <el-icon size="15" style="color:#409EFF"><Document /></el-icon>
            <input
              v-model="reportTitle"
              class="title-input"
              placeholder="Untitled Report"
              @keydown.enter.prevent
            />
          </div>
          <div class="header-right">
            <el-tooltip content="Export PDF" placement="top">
              <el-button size="small" type="primary" plain @click="exportPdf">
                <el-icon><Download /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="Clear document" placement="top">
              <el-button size="small" type="danger" plain @click="clearContent">
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-tooltip>
            <el-button size="small" @click="dialogVisible = false" text>
              <el-icon size="16"><Close /></el-icon>
            </el-button>
          </div>
        </div>
      </template>

      <!-- Formatting Toolbar -->
      <div class="toolbar" @mousedown.prevent>
        <el-button-group size="small">
          <el-button @click="exec('bold')" :class="{ active: states.bold }" title="Bold (Ctrl+B)">
            <b>B</b>
          </el-button>
          <el-button @click="exec('italic')" :class="{ active: states.italic }" title="Italic (Ctrl+I)">
            <i>I</i>
          </el-button>
          <el-button @click="exec('underline')" :class="{ active: states.underline }" title="Underline (Ctrl+U)">
            <u>U</u>
          </el-button>
          <el-button @click="exec('strikeThrough')" title="Strikethrough">
            <s>S</s>
          </el-button>
        </el-button-group>

        <el-divider direction="vertical" />

        <el-button-group size="small">
          <el-button @click="execBlock('h1')" title="Heading 1">H1</el-button>
          <el-button @click="execBlock('h2')" title="Heading 2">H2</el-button>
          <el-button @click="execBlock('h3')" title="Heading 3">H3</el-button>
          <el-button @click="execBlock('p')" title="Paragraph">¶</el-button>
        </el-button-group>

        <el-divider direction="vertical" />

        <el-button-group size="small">
          <el-button @click="exec('insertUnorderedList')" title="Bullet List">• UL</el-button>
          <el-button @click="exec('insertOrderedList')" title="Numbered List">1. OL</el-button>
        </el-button-group>

        <el-divider direction="vertical" />

        <el-button size="small" @click="insertHr" title="Horizontal Rule">—</el-button>
        <el-button size="small" @click="insertDate" title="Insert current date">📅</el-button>
      </div>

      <!-- Editor Body -->
      <div
        ref="editorRef"
        class="editor-body"
        contenteditable="true"
        spellcheck="false"
        @input="onInput"
        @keyup="updateStates"
        @mouseup="updateStates"
        @keydown="handleKeydown"
      ></div>

      <!-- Footer -->
      <div class="editor-footer">
        <span class="word-count">{{ wordCount }} words</span>
        <span class="save-hint" v-if="lastSaved">Auto-saved {{ lastSaved }}</span>
      </div>
    </el-dialog>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { Document, Download, Delete, Close } from '@element-plus/icons-vue'

const STORAGE_KEY = 'cp_report_draft'
const TITLE_KEY   = 'cp_report_title'

const dialogVisible = ref(false)
const reportTitle   = ref('Analysis Report')
const editorRef     = ref(null)
const lastSaved     = ref('')
const states        = ref({ bold: false, italic: false, underline: false })

// Word count from plain text
const wordCount = computed(() => {
  if (!editorRef.value) return 0
  const text = editorRef.value.innerText || ''
  return text.trim() ? text.trim().split(/\s+/).length : 0
})

onMounted(() => {
  reportTitle.value = localStorage.getItem(TITLE_KEY) || 'Analysis Report'
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved && editorRef.value) {
    editorRef.value.innerHTML = saved
    lastSaved.value = 'earlier'
  }
})

watch(reportTitle, val => localStorage.setItem(TITLE_KEY, val))

function onInput() {
  if (!editorRef.value) return
  localStorage.setItem(STORAGE_KEY, editorRef.value.innerHTML)
  const now = new Date()
  lastSaved.value = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function updateStates() {
  states.value = {
    bold:      document.queryCommandState('bold'),
    italic:    document.queryCommandState('italic'),
    underline: document.queryCommandState('underline'),
  }
}

function exec(cmd) {
  document.execCommand(cmd, false, null)
  editorRef.value?.focus()
  updateStates()
  onInput()
}

function execBlock(tag) {
  document.execCommand('formatBlock', false, tag)
  editorRef.value?.focus()
  onInput()
}

function insertHr() {
  document.execCommand('insertHTML', false, '<hr style="border:none;border-top:1px solid #ddd;margin:12px 0"/>')
  editorRef.value?.focus()
  onInput()
}

function insertDate() {
  const d = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
  document.execCommand('insertText', false, d)
  editorRef.value?.focus()
  onInput()
}

function clearContent() {
  if (!editorRef.value) return
  editorRef.value.innerHTML = ''
  localStorage.removeItem(STORAGE_KEY)
  lastSaved.value = ''
  editorRef.value.focus()
}

function handleKeydown(e) {
  // Tab → indent
  if (e.key === 'Tab') {
    e.preventDefault()
    document.execCommand('insertHTML', false, '&nbsp;&nbsp;&nbsp;&nbsp;')
  }
}

function exportPdf() {
  const content  = editorRef.value?.innerHTML || '<p>(empty)</p>'
  const title    = reportTitle.value || 'Analysis Report'
  const dateStr  = new Date().toLocaleString()

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>${title}</title>
  <style>
    @page { margin: 20mm 18mm; }
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 13px;
      color: #1a1a1a;
      max-width: 760px;
      margin: 0 auto;
      padding: 0 16px;
      line-height: 1.75;
    }
    .cover { border-bottom: 3px solid #409EFF; padding-bottom: 16px; margin-bottom: 28px; }
    .cover h1 { font-size: 26px; font-weight: 700; color: #1a1a2e; margin: 0 0 6px; }
    .cover .meta { color: #909399; font-size: 12px; }
    h1 { font-size: 20px; color: #1a1a2e; margin: 22px 0 8px; }
    h2 { font-size: 16px; color: #303133; margin: 18px 0 6px; border-bottom: 1px solid #eee; padding-bottom: 4px; }
    h3 { font-size: 14px; color: #303133; margin: 14px 0 4px; }
    p  { margin: 6px 0; }
    ul, ol { padding-left: 22px; margin: 6px 0; }
    li { margin: 3px 0; }
    hr { border: none; border-top: 1px solid #ddd; margin: 16px 0; }
    b, strong { font-weight: 700; }
    @media print {
      body { padding: 0; }
      .cover { border-bottom-color: #409EFF; }
    }
  </style>
</head>
<body>
  <div class="cover">
    <h1>${title}</h1>
    <div class="meta">CP Fresh Platform &nbsp;·&nbsp; Generated: ${dateStr}</div>
  </div>
  ${content}
</body>
</html>`

  const win = window.open('', '_blank', 'width=900,height=720')
  if (!win) return
  win.document.write(html)
  win.document.close()
  win.focus()
  setTimeout(() => {
    win.print()
  }, 350)
}
</script>

<style>
/* FAB — fixed, bottom-right */
.report-fab {
  position: fixed;
  bottom: 32px;
  right: 32px;
  z-index: 2000;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: #409EFF;
  color: #fff;
  border-radius: 24px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  box-shadow: 0 4px 16px rgba(64,158,255,0.45);
  user-select: none;
  transition: background 0.2s, box-shadow 0.2s, transform 0.15s;
}
.report-fab:hover {
  background: #337ecc;
  box-shadow: 0 6px 20px rgba(64,158,255,0.55);
  transform: translateY(-2px);
}

/* Override el-dialog for floating look */
.report-dialog .el-dialog {
  border-radius: 10px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.18);
  display: flex;
  flex-direction: column;
  max-height: 82vh;
}
.report-dialog .el-dialog__header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
  cursor: move;
}
.report-dialog .el-dialog__body {
  padding: 0;
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>

<style scoped>
/* Dialog header */
.report-dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}
.title-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  min-width: 0;
}
.title-input::placeholder { color: #c0c4cc; }
.header-right {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

/* Toolbar */
.toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 14px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
  user-select: none;
}
.toolbar .el-button.active {
  background: #ecf5ff;
  border-color: #409EFF;
  color: #409EFF;
}

/* Editor */
.editor-body {
  flex: 1;
  overflow-y: auto;
  padding: 18px 20px;
  min-height: 320px;
  max-height: 52vh;
  outline: none;
  font-size: 13px;
  line-height: 1.8;
  color: #303133;
  font-family: 'Segoe UI', Arial, sans-serif;
}
.editor-body:empty::before {
  content: 'Start writing your analysis report here...\A\AYou can use the toolbar to format text, or just start typing.';
  white-space: pre;
  color: #c0c4cc;
  pointer-events: none;
}
.editor-body h1 { font-size: 20px; font-weight: 700; margin: 14px 0 8px; color: #1a1a2e; }
.editor-body h2 { font-size: 16px; font-weight: 600; margin: 12px 0 6px; color: #303133; border-bottom: 1px solid #eee; padding-bottom: 3px; }
.editor-body h3 { font-size: 14px; font-weight: 600; margin: 10px 0 4px; }
.editor-body p  { margin: 4px 0; }
.editor-body ul, .editor-body ol { padding-left: 22px; }
.editor-body li { margin: 2px 0; }
.editor-body hr { border: none; border-top: 1px solid #ddd; margin: 12px 0; }

/* Footer */
.editor-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 18px;
  border-top: 1px solid #ebeef5;
  background: #fafafa;
  font-size: 11px;
  color: #c0c4cc;
}
</style>
