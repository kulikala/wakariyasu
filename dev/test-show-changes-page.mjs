#!/usr/bin/env node
import assert from 'node:assert/strict'
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { spawn } from 'node:child_process'
import { tmpdir } from 'node:os'
import { createServer } from 'node:net'

const urls = [
  'https://cdn.jsdelivr.net/npm/vue@3.5.44/+esm',
  'https://cdn.jsdelivr.net/npm/@vue/compiler-dom@3.5.44/+esm',
  'https://cdn.jsdelivr.net/npm/@lucide/vue@1.61.0/+esm',
  'https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.3.3',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/core.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/javascript.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/typescript.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/python.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/bash.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/yaml.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/xml.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/css.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/json.js/+esm',
  'https://cdn.jsdelivr.net/npm/highlight.js@11.12.0/es/languages/sql.js/+esm',
  'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap'
]
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
const staticOnly = process.argv.includes('--static-only')
const pagePath = process.argv.slice(2).find(arg => !arg.startsWith('--'))
let page = pagePath ? readFileSync(resolve(pagePath), 'utf8') : ''
if (!page) for await (const chunk of process.stdin) page += chunk
const marker = /^const DATA = (.*);?\n/m
const dataMatch = page.match(marker)
assert(dataMatch, '埋め込み JSON がありません')
const data = JSON.parse(dataMatch[1].replace(/;$/, ''))
/** Check application resource declarations, excluding the embedded user data. */
function checkExternalLoads (html) {
  const shell = html.replace(marker, 'const DATA = null\n')
  const allowed = new Set(urls)
  // Firefox refuses an import map once the artifact host has loaded a module, so imports name full URLs.
  assert(!/type=["']importmap["']/i.test(shell), 'import map があります')
  for (const [, url] of shell.matchAll(/\bimport\b[^'"]*?\bfrom\s*['"]([^'"]+)['"]/g)) assert(allowed.has(url), `未許可の import: ${url}`)
  for (const tag of shell.matchAll(/<(?:link|script|img|iframe|object|embed|source|audio|video)\b[^>]*>/gi)) {
    for (const attr of tag[0].matchAll(/\b(?:src|href|data|srcset)\s*=\s*["']([^"']*)["']/gi)) {
      assert(allowed.has(attr[1]), `未許可の外部リソース: ${attr[1]}`)
    }
  }
  assert(!/(?:\burl\s*\(|@import\b|\bfetch\s*\(|\bimport\s*\()/i.test(shell), '追加の動的外部読み込みがあります')
  for (const url of urls) assert(shell.includes(url), `固定 URL がありません: ${url}`)
  assert(!/href=["']#/.test(shell), 'ハッシュリンクがあります')
}
checkExternalLoads(page)
for (const extra of ['<img src="https://example.com/x">', '<style>@import "https://example.com/x";</style>', '<script>fetch("https://example.com/x")</script>']) {
  assert.throws(() => checkExternalLoads(page.replace('<title>', extra + '<title>')))
}
if (staticOnly) {
  process.stdout.write(JSON.stringify({ ok: true, staticOnly: true, browser: 'not-run', staticExternalLoads: urls }) + '\n')
  process.exit(0)
}

// Keep the browser profile outside the repository; Chrome helpers may still be writing when the main process exits.
const work = mkdtempSync(join(tmpdir(), 'diff-vue-cdp-'))
const portServer = createServer()
let port = 0
let portError = ''
try {
  await new Promise((resolve, reject) => {
    portServer.once('error', reject)
    portServer.listen(0, '127.0.0.1', resolve)
  })
  port = portServer.address().port
  await new Promise(resolve => portServer.close(resolve))
} catch (error) {
  portError = error.message
  // Let Chrome choose its own free debugging port when Node cannot bind a socket.
}
const errors = []
const networkFailures = []
const requests = new Map()
let launchError
const chromePath = process.env.CHROME || (process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : 'google-chrome')
const chrome = spawn(chromePath, ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--no-first-run', '--no-default-browser-check', '--disable-component-update', `--remote-debugging-port=${port}`, `--user-data-dir=${join(work, 'profile')}`, 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] })
chrome.on('error', error => { launchError = error })
let chromeLog = ''
chrome.stderr.on('data', chunk => { chromeLog += chunk })
let socket
let nextId = 0
const pending = new Map()
const checks = []
function send (method, params = {}) {
  const id = ++nextId
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)) }, 30000)
    pending.set(id, { resolve, reject, timer })
    socket.send(JSON.stringify({ id, method, params }))
  })
}
async function evaluate (expression) {
  const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })
  assert(!result.exceptionDetails, JSON.stringify(result.exceptionDetails))
  return result.result.value
}
async function waitFor (expression, label, timeout = 30000) {
  const start = Date.now()
  while (Date.now() - start < timeout) {
    if (await evaluate(expression)) return
    await sleep(80)
  }
  throw new Error(`待機失敗: ${label}; console=${JSON.stringify(errors)}; network=${JSON.stringify(networkFailures)}`)
}
function check (value, label) {
  assert(value, label)
  checks.push(label)
}
/** Move the pointer and dispatch mouse press/release through Chrome itself. */
async function click (selector) {
  await evaluate(`document.querySelector(${JSON.stringify(selector)})?.scrollIntoView({block:'nearest',inline:'nearest'})`)
  await sleep(50)
  const rect = await evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); if (!el) return null; const r = el.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2, width: r.width, height: r.height } })()`)
  assert(rect && rect.width > 0 && rect.height > 0, `クリックできません: ${selector}`)
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: rect.x, y: rect.y })
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: rect.x, y: rect.y, button: 'left', clickCount: 1 })
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: rect.x, y: rect.y, button: 'left', clickCount: 1 })
  await sleep(100)
}
async function search (text) {
  await click('#filter')
  // Select through the DOM: the select-all shortcut is Ctrl+A on Linux but Cmd+A on macOS.
  await evaluate("document.querySelector('#filter').select()")
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 })
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 })
  if (text) await send('Input.insertText', { text })
  await sleep(350)
}
/** Pick the first (Home) or last (End) source in the select box. */
async function pickSource (key) {
  if (process.platform === 'darwin') {
    // macOS draws the <select> popup natively, outside the page, so keys sent to the page do not reach it.
    await evaluate(`(() => { const s = document.querySelector('#source'); s.selectedIndex = ${key === 'Home' ? 0 : 's.options.length - 1'}; s.dispatchEvent(new Event('change')) })()`)
  } else {
    await click('#source')
    const code = key === 'Home' ? 36 : 35
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key, code: key, windowsVirtualKeyCode: code })
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code: key, windowsVirtualKeyCode: code })
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 })
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 })
  }
  await sleep(200)
}
async function navigate (html, name) {
  const file = join(work, name + '.html')
  // A page built with --artifact has no document skeleton; wrap it the way the artifact host does,
  // with a host module script running before the page.
  const wrapped = /^\s*<!DOCTYPE/i.test(html) ? html
    : '<!doctype html><html><head><script type="module">window.__host = true</script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + html + '</body></html>'
  writeFileSync(file, wrapped)
  await send('Page.navigate', { url: pathToFileURL(file).href })
  await waitFor("document.querySelector('#app')?.dataset.ready === 'true'", 'Vue mount', 60000)
  await sleep(250)
}
const fileCount = "document.querySelectorAll('#files article[data-file-id]').length"
const allOpen = "[...document.querySelectorAll('#files .file-header')].every(e => e.getAttribute('aria-expanded') === 'true')"
const allClosed = "[...document.querySelectorAll('#files .file-header')].every(e => e.getAttribute('aria-expanded') === 'false')"
try {
  let targets
  for (let n = 0; n < 150; n++) {
    if (launchError) throw launchError
    if (chrome.exitCode !== null || chrome.signalCode !== null) break
    if (!port) {
      try { port = Number(readFileSync(join(work, 'profile', 'DevToolsActivePort'), 'utf8').split('\n')[0]) } catch {}
    }
    if (!port) { await sleep(100); continue }
    try { targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break } catch {}
    await sleep(100)
  }
  assert(targets?.length, `Chrome を起動できません: ${portError}; ${chromeLog.slice(-1500)}`)
  socket = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl)
  await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }) })
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data)
    if (message.id) {
      const item = pending.get(message.id)
      if (!item) return
      clearTimeout(item.timer)
      pending.delete(message.id)
      if (message.error) item.reject(new Error(JSON.stringify(message.error)))
      else item.resolve(message.result)
    } else if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails.text + ': ' + (message.params.exceptionDetails.exception?.description || ''))
    else if (message.method === 'Runtime.consoleAPICalled' && message.params.type === 'error') errors.push(message.params.args.map(a => a.value || a.description).join(' '))
    else if (message.method === 'Network.requestWillBeSent') requests.set(message.params.requestId, message.params.request.url)
    else if (message.method === 'Network.loadingFailed') networkFailures.push({ url: requests.get(message.params.requestId), error: message.params.errorText })
  })
  await send('Runtime.enable')
  await send('Page.enable')
  await send('Network.enable')
  await send('Emulation.setDeviceMetricsOverride', { width: 1400, height: 900, deviceScaleFactor: 1, mobile: false })
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'dark' }] })
  await navigate(page, 'sample')
  const total = data.sources.reduce((n, source) => n + source.files.length, 0)
  const availableFull = data.sources.some(source => source.files.some(file => typeof file.full_body === 'string'))
  check(await evaluate(fileCount) === total, 'sample: 全ファイルの見出し')
  check(await evaluate('document.documentElement.dataset.theme') === 'dark', 'OS の初期配色に従う')
  check(await evaluate("document.querySelector('#full').disabled") === !availableFull, '全文の有無で切替を制御')
  check(await evaluate("!!document.querySelector('#source')") === (data.sources.length > 1), '単一対象では対象選択を非表示')
  check(await evaluate("document.querySelector('#version').textContent") === data.data_version, 'バージョンをそのまま表示')
  check(await evaluate("!document.querySelector('details, summary, a[href^=\"#\"]')"), '独自開閉とハッシュ非依存')
  if (total) {
    await click('#files .file-header')
    check(await evaluate("document.querySelector('#files .file-header').getAttribute('aria-expanded') === 'true'"), '見出しで開く')
    await click('#files .file-header')
    check(await evaluate("document.querySelector('#files .file-header').getAttribute('aria-expanded') === 'false'"), '見出しで閉じる')
    await click('#openAll')
    check(await evaluate(allOpen), 'すべて開く')
    await click('#closeAll')
    check(await evaluate(allClosed), 'すべて閉じる')
    check(await evaluate("document.querySelectorAll('#files .diff-body').length === 0"), '閉じたファイルの本文は未描画')
    const sidebarWidth = () => evaluate("document.querySelector('#sidebar').getBoundingClientRect().width")
    const before = await sidebarWidth()
    const handle = await evaluate("(() => { const r = document.querySelector('#resizer').getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 } })()")
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: handle.x, y: handle.y })
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: handle.x, y: handle.y, button: 'left', clickCount: 1 })
    for (const dx of [40, 80, 120]) await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: handle.x + dx, y: handle.y, button: 'left', buttons: 1 })
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: handle.x + 120, y: handle.y, button: 'left', clickCount: 1 })
    await sleep(100)
    check(Math.abs(await sidebarWidth() - before - 120) <= 2, '境目のドラッグで一覧の幅が変わる')
    await click('#toggleSidebar')
    check(await evaluate("document.querySelector('#sidebar').getBoundingClientRect().width === 0 && !document.querySelector('#resizer') && document.querySelector('#toggleSidebar').getAttribute('aria-expanded') === 'false'"), '一覧を隠す')
    await click('#toggleSidebar')
    check(Math.abs(await sidebarWidth() - before - 120) <= 2, '一覧を出すと前の幅に戻る')
    await click('#filelist button[data-file-id]')
    check(await evaluate("document.querySelector('#files .file-header').getAttribute('aria-expanded') === 'true' && location.hash === ''"), '一覧から開いて移動')
    // Scroll into the middle of the longest file: its header and the current hunk header stay on screen.
    const longest = data.sources.flatMap((source, ri) => source.files.map((file, fi) => ({ id: `f-${ri}-${fi}`, rows: file.body.split('\n').length })))
      .sort((x, y) => y.rows - x.rows)[0]
    await click(`#filelist button[data-file-id="${longest.id}"]`)
    await sleep(400)
    const stuck = await evaluate(`(() => {
      const main = document.querySelector('#main')
      const article = document.querySelector('#files article[data-file-id="${longest.id}"]')
      if (article.offsetHeight < main.clientHeight * 2) return null
      main.scrollTop += article.getBoundingClientRect().top - main.getBoundingClientRect().top + main.clientHeight
      const head = article.querySelector('.file-header-row').getBoundingClientRect()
      const hunk = [...article.querySelectorAll('td.hunk')].map(td => td.getBoundingClientRect()).filter(r => r.top <= head.bottom + 1).at(-1)
      return { head: head.top - main.getBoundingClientRect().top, hunk: hunk && hunk.top - head.bottom }
    })()`)
    check(stuck === null || (Math.abs(stuck.head) <= 1 && stuck.hunk !== undefined && Math.abs(stuck.hunk) <= 1), 'スクロールしてもファイル名と節の見出しが上に残る: ' + JSON.stringify(stuck))
    await evaluate("document.querySelector('#main').scrollTop = 0")
    await send('Browser.grantPermissions', { permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite'] }).catch(() => {})
    const clipboard = "navigator.clipboard.readText()"
    const firstPath = data.sources.find(s => s.files.length).files[0].path
    await click('#files .copy-path')
    check(await evaluate("document.querySelector('#files .file-header').getAttribute('aria-expanded') === 'true'"), 'パスのコピーで開閉しない')
    check(await evaluate(clipboard) === firstPath, 'ファイル名の横のボタンでパスをコピー')
    await evaluate("(() => { const text = document.querySelector('#diff-app h1'); const range = document.createRange(); range.selectNodeContents(text); getSelection().removeAllRanges(); getSelection().addRange(range) })()")
    await waitFor("!!document.querySelector('#copySelection')", '選んだ文字列のコピーのボタン', 5000)
    const selected = await evaluate('getSelection().toString()')
    await click('#copySelection')
    check(await evaluate(clipboard) === selected && selected.length > 0, '選んだ文字列をコピー')
    await evaluate('getSelection().removeAllRanges()')
    await waitFor("!document.querySelector('#copySelection')", '選択を外すとボタンが消える', 5000)
    await search(data.sources.find(s => s.files.length).files[0].path)
    check(await evaluate(fileCount) > 0, 'ファイル名検索')
    // The hunk header text may also appear in a file's own lines; only those files may match.
    const hunkQuery = '@@ -0,0'
    const bodyHits = data.sources.flatMap(s => s.files).filter(f => [f.path, f.old || ''].some(p => p.toLowerCase().includes(hunkQuery)) ||
      String(f.body || '').split('\n').some(line => !line.startsWith('@@') && /^[ +-]/.test(line) && line.slice(1).toLowerCase().includes(hunkQuery))).length
    await search(hunkQuery)
    check(await evaluate(fileCount) === bodyHits, 'ハンク記号は検索しない')
    await search('')
    await click('#openAll')
    const ids = await evaluate("[...document.querySelectorAll('#files article[data-file-id]')].map(e => e.dataset.fileId)")
    for (const layout of ['unified', 'split']) {
      await click('#' + layout)
      for (const scope of availableFull ? ['diff', 'full'] : ['diff']) {
        await click('#' + scope)
        for (const id of ids) {
          await evaluate(`document.querySelector('#files article[data-file-id="${id}"]').scrollIntoView({block:'center'})`)
          await waitFor(`!!document.querySelector('#files article[data-file-id="${id}"] .diff-body')`, `render ${id}`)
          check(await evaluate(`(() => { const table = document.querySelector('#files article[data-file-id="${id}"] table'); return !table || (table.dataset.layout === '${layout}' && table.dataset.scope === '${scope}') })()`), `render ${id} ${layout}/${scope}`)
        }
        check(await evaluate(fileCount) === total, `全ファイル描画 ${layout}/${scope}`)
      }
    }
    await click('#closeAll')
  }
  for (const theme of ['light', 'dark', 'hybrid']) {
    await click('#' + theme)
    check(await evaluate('document.documentElement.dataset.theme') === theme, `配色 ${theme}`)
  }
  const fixture = {
    ...data, title: '操作検証', data_version: 'test', full_text: true, group_depth: 2,
    sources: [
      { name: '対象一', kind: 'git', base_ref: 'before', target_ref: 'after', base: '', target: '', commits: [['1234567890123456', '2026-11-05', '検証コミット']], files: [
        { path: 'docs/example.md', old: 'old-only.md', status: 'R100', added: 3, deleted: 1, binary: false, notice: '', body: '@@ -1 +1,3 @@\n-old\n+# **見出し検索**\n+- list `code`\n+[link](https://example.com)', full_body: '@@ -1,2 +1,4 @@\n unchanged\n-old\n+# **見出し検索**\n+- list `code`\n+[link](https://example.com)' },
        { path: 'src/test.js', old: null, status: 'M', added: 1, deleted: 1, binary: false, notice: '', body: '@@ -1 +1 @@\n-const old = 1\n+const needle = 2', full_body: '@@ -1 +1 @@\n-const old = 1\n+const needle = 2' }
      ] },
      { name: '対象二', kind: 'plain', base_ref: 'before', target_ref: 'after', base: '', target: '', commits: [], files: [
        { path: 'other.txt', old: null, status: 'A', added: 1, deleted: 0, binary: false, notice: '', body: '@@ -0,0 +1 @@\n+other body', full_body: '@@ -0,0 +1 @@\n+other body' }
      ] }
    ]
  }
  const fixturePage = page.replace(marker, () => 'const DATA = ' + JSON.stringify(fixture).replace(/</g, '\\u003c') + ';\n')
  await navigate(fixturePage, 'fixture')
  await click('#hybrid')
  await navigate(fixturePage, 'fixture')
  check(await evaluate('document.documentElement.dataset.theme') === 'hybrid', '同じファイルで配色の保存と復元')
  await search('needle')
  check(await evaluate(fileCount) === 1, '本文検索')
  await click('#filelist button[data-file-id]')
  check(await evaluate("!!document.querySelector('#files mark.search')"), 'コード上の検索強調')
  await click('#closeAll')
  await search('old-only')
  check(await evaluate(fileCount) === 1, '旧パス検索')
  await search('見出し検索')
  await click('#filelist button[data-file-id]')
  check(await evaluate("!!document.querySelector('#files mark.search')"), 'Markdown 上の検索強調')
  await search('')
  await click('#openAll')
  await pickSource('End')
  check(await evaluate(fileCount) === 1, '対象選択')
  await click('#openAll')
  await click('#closeAll')
  check(await evaluate(allClosed), '対象で絞った一括開閉')
  await pickSource('Home')
  check(await evaluate("[...document.querySelectorAll('#files .file-header')].filter(e => e.getAttribute('aria-expanded') === 'true').length") === 2, '対象外ファイルの開閉状態を保持')
  // Whitespace: changed blanks carry marks drawn by CSS, and ignoring whitespace hides blank-only changes.
  const spaceFile = (path, body) => ({ path, old: null, status: 'M', added: 2, deleted: 2, binary: false, notice: '', body })
  const spaceFixture = { ...fixture, sources: [{ name: '空白', kind: 'plain', base_ref: 'before', target_ref: 'after', base: '', target: '', commits: [], files: [
    spaceFile('blank.py', '@@ -1,2 +1,2 @@\n-\tone  \r\n-a　b\n+    one\n+a b'),
    spaceFile('real.py', '@@ -1,2 +1,2 @@\n-\tkeep\n-old\n+    keep\n+new'),
    { ...spaceFile('run.sh', ''), added: 0, deleted: 0, notice: '内容の差分はありません。', old_mode: '100644', new_mode: '100755' },
    { ...spaceFile('moved.py', ''), old: 'before.py', status: 'R100', added: 0, deleted: 0 },
    { ...spaceFile('gone.py', ''), status: 'D', added: 0, deleted: 1 },
    { ...spaceFile('link', ''), added: 1, deleted: 1, old_mode: '120000', new_mode: '120000' }
  ] }] }
  await navigate(page.replace(marker, () => 'const DATA = ' + JSON.stringify(spaceFixture).replace(/</g, '\\u003c') + ';\n'), 'space')
  await click('#openAll')
  await waitFor("document.querySelectorAll('#files table').length === 2", '空白の検証の描画')
  check((await evaluate("document.querySelectorAll('#files article')[2].querySelector('.file-mode')?.textContent")) === '通常のファイル（100644） → 実行できるファイル（100755）', 'モードの変更を出す')
  const marks = await evaluate("[...document.querySelectorAll('#files article')[0].querySelectorAll('.ws')].map(e => e.className.replace('ws ws-', ''))")
  check(['tab', 'space', 'cr', 'ideo'].every(name => marks.includes(name)), '変わった空白に記号を付ける: ' + marks.join(','))
  const firstLine = "document.querySelector('#files article .line-text')"
  await evaluate(`(() => { const range = document.createRange(); range.selectNodeContents(${firstLine}); getSelection().removeAllRanges(); getSelection().addRange(range) })()`)
  check(await evaluate('getSelection().toString()') === '\tone  \r', '記号を付けた行を選ぶと元の文字だけが入る')
  await evaluate('getSelection().removeAllRanges()')
  await click('#spaceIgnore')
  await waitFor("!!document.querySelector('#files .space-only')", '空白だけの変更の案内')
  check(await evaluate("document.querySelectorAll('#files article')[1].querySelectorAll('tr td:last-child .line-text').length") === 3, '空白を無視すると、空白だけ変わった行は1行にまとまる')
  check(await evaluate("document.querySelector('#totals').textContent.includes('+1') && document.querySelector('#totals').textContent.includes('−1')"), '空白を無視した行数を合計に出す')
  await click('#split')
  check(await evaluate("[...document.querySelectorAll('#files article')[1].querySelectorAll('tr')].some(t => { const cells = t.querySelectorAll('.line-text'); return cells.length === 2 && cells[0].textContent === '\\tkeep' && cells[1].textContent === '    keep' })"), '左右の配置では、それぞれの側の空白のまま出す')
  await click('#unified')
  await click('#spaceShow')
  await click('#contentOnly')
  check(await evaluate("[...document.querySelectorAll('#files article .file-header')].map(e => e.textContent.split(' / ')[1]).join()") === 'blank.py,real.py' && await evaluate("document.querySelectorAll('#filelist button[data-file-id]').length") === 2, '追加・変更したファイルだけにすると、権限だけの変更・移動・削除・シンボリックリンクを出さない')
  await click('#contentOnly')
  check(await evaluate(fileCount) === 6, '絞り込みを外すと、すべてのファイルを出す')
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true })
  const mobileFixture = structuredClone(fixture)
  mobileFixture.sources[0].files = Array.from({ length: 45 }, (_, i) => ({ ...fixture.sources[0].files[0], path: `docs/mobile-${i}.md` }))
  const mobilePage = page.replace(marker, () => 'const DATA = ' + JSON.stringify(mobileFixture).replace(/</g, '\\u003c') + ';\n')
  await navigate(mobilePage, 'mobile')
  check(await evaluate("document.querySelector('#diff-screen').dataset.screen === 'list'"), 'モバイル初期画面は一覧')
  check(await evaluate("!document.querySelector('#resizer') && document.querySelector('#toggleSidebar').getBoundingClientRect().width === 0"), 'モバイルでは幅の境目と一覧を隠すボタンが無い')
  check(await evaluate("document.querySelector('#diff-screen').getBoundingClientRect().left >= innerWidth - 1"), 'モバイル差分の開始位置は画面右側')
  await search('見出し検索')
  const oldSearch = await evaluate("document.querySelector('#filter').value")
  await evaluate("document.querySelector('#sidebar').scrollTop = document.querySelector('#filelist button[data-file-id=\"f-0-15\"]').offsetTop - 200")
  const listScroll = await evaluate("document.querySelector('#sidebar').scrollTop")
  await click('#filelist button[data-file-id="f-0-15"]')
  await sleep(400)
  check(await evaluate("document.querySelector('#diff-screen').dataset.screen === 'diff'"), 'モバイル一覧から差分に切り替え')
  check(await evaluate("document.querySelector('#diff-screen').getBoundingClientRect().left >= -1 && document.querySelector('#diff-screen').getBoundingClientRect().right <= innerWidth + 1"), 'モバイル差分のスライド完了')
  check(await evaluate("[...document.querySelectorAll('.bar .button-text')].every(e => getComputedStyle(e).display === 'none')"), 'モバイルツールバーはアイコンのみ')
  await click('#back')
  await sleep(400)
  check(await evaluate("document.querySelector('#diff-screen').dataset.screen === 'list'"), 'モバイル戻る')
  check(await evaluate("document.querySelector('#filter').value") === oldSearch, '戻った一覧の検索を保持')
  check(await evaluate("document.querySelector('#sidebar').scrollTop") === listScroll, '戻った一覧のスクロール位置を保持')
  check(await evaluate('document.documentElement.scrollWidth <= innerWidth'), 'モバイル横方向のはみ出しなし')
  // The static check sees only URLs written in the page; modules and fonts load further URLs at run time.
  const loaded = [...requests.values()].filter(url => /^https?:/.test(url)).map(url => new URL(url))
  const outside = loaded.filter(url => !(url.host === 'cdn.jsdelivr.net' ? url.pathname.startsWith('/npm/')
    : ['fonts.googleapis.com', 'fonts.gstatic.com'].includes(url.host)))
  check(outside.length === 0, '実行中に読み込んだ外部アドレスが jsDelivr の /npm/ と Google Fonts だけ: ' + outside.join(' '))
  check(networkFailures.length === 0, '外部の読み込みの失敗なし: ' + JSON.stringify(networkFailures))
  check(errors.length === 0, 'コンソールエラーなし: ' + errors.join('\n'))
  process.stdout.write(JSON.stringify({ ok: true, files: total, checks: checks.length, results: checks, staticExternalLoads: urls, consoleErrors: errors, networkFailures }) + '\n')
} catch (error) {
  process.stderr.write(JSON.stringify({ ok: false, browser: 'failed', message: error.message, consoleErrors: errors, networkFailures }) + '\n')
  process.exitCode = 1
} finally {
  socket?.close()
  chrome.kill('SIGTERM')
  for (const item of pending.values()) clearTimeout(item.timer)
  if (chrome.exitCode === null && chrome.signalCode === null && !launchError) {
    await Promise.race([new Promise(resolve => chrome.once('exit', resolve)), sleep(2000)])
    if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL')
  }
  rmSync(work, { recursive: true, force: true, maxRetries: 10, retryDelay: 300 })
}
