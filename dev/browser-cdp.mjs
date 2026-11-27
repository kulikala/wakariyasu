// Drive headless Chrome through the DevTools protocol. Shared by the browser tests of the skills' pages.
import assert from 'node:assert/strict'
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { spawn } from 'node:child_process'
import { tmpdir } from 'node:os'
import { createServer } from 'node:net'

export const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

/** Start Chrome with a throwaway profile and connect to its first page. Call close() when done. */
export async function launch ({ width = 1200, height = 900, scheme = 'light' } = {}) {
  const work = mkdtempSync(join(tmpdir(), 'page-cdp-'))
  const errors = []
  const failures = []
  const requests = new Map()
  const pending = new Map()
  let nextId = 0
  let socket
  let launchError
  let port = 0
  let portError = ''
  const portServer = createServer()
  try {
    await new Promise((resolve, reject) => { portServer.once('error', reject); portServer.listen(0, '127.0.0.1', resolve) })
    port = portServer.address().port
    await new Promise(resolve => portServer.close(resolve))
  } catch (error) {
    portError = error.message
  }
  const chromePath = process.env.CHROME || (process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : 'google-chrome')
  const chrome = spawn(chromePath, ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--no-first-run', '--no-default-browser-check', '--disable-component-update', `--remote-debugging-port=${port}`, `--user-data-dir=${join(work, 'profile')}`, 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] })
  chrome.on('error', error => { launchError = error })
  let chromeLog = ''
  chrome.stderr.on('data', chunk => { chromeLog += chunk })
  const send = (method, params = {}) => {
    const id = ++nextId
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)) }, 30000)
      pending.set(id, { resolve, reject, timer })
      socket.send(JSON.stringify({ id, method, params }))
    })
  }
  const close = async () => {
    socket?.close()
    chrome.kill('SIGTERM')
    for (const item of pending.values()) clearTimeout(item.timer)
    if (chrome.exitCode === null && chrome.signalCode === null && !launchError) {
      await Promise.race([new Promise(resolve => chrome.once('exit', resolve)), sleep(2000)])
      if (chrome.exitCode === null && chrome.signalCode === null) chrome.kill('SIGKILL')
    }
    rmSync(work, { recursive: true, force: true, maxRetries: 10, retryDelay: 300 })
  }
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
    assert(targets?.length, `Cannot start Chrome: ${portError}; ${chromeLog.slice(-1500)}`)
    socket = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl)
    await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }) })
    socket.addEventListener('message', event => {
      const message = JSON.parse(event.data)
      if (message.id) {
        const item = pending.get(message.id)
        if (!item) return
        clearTimeout(item.timer)
        pending.delete(message.id)
        if (message.error) item.reject(new Error(message.error.message))
        else item.resolve(message.result)
      } else if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails.exception?.description || message.params.exceptionDetails.text)
      else if (message.method === 'Runtime.consoleAPICalled' && message.params.type === 'error') errors.push(message.params.args.map(a => a.value || a.description).join(' '))
      else if (message.method === 'Network.requestWillBeSent') requests.set(message.params.requestId, message.params.request.url)
      else if (message.method === 'Network.loadingFailed') failures.push({ url: requests.get(message.params.requestId), error: message.params.errorText })
    })
    await send('Runtime.enable')
    await send('Page.enable')
    await send('Network.enable')
    await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false })
    // A headless page is not focused by itself, and the clipboard needs a focused document.
    await send('Emulation.setFocusEmulationEnabled', { enabled: true })
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: scheme }] })
  } catch (error) {
    await close()
    throw error
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
    throw new Error(`Wait failed: ${label}; console=${JSON.stringify(errors)}; network=${JSON.stringify(failures)}`)
  }
  /** Press and release the mouse on the middle of an element, through Chrome itself. */
  async function click (selector) {
    await evaluate(`document.querySelector(${JSON.stringify(selector)})?.scrollIntoView({block:'nearest',inline:'nearest'})`)
    await sleep(50)
    const rect = await evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); if (!el) return null; const r = el.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2, width: r.width, height: r.height } })()`)
    assert(rect && rect.width > 0 && rect.height > 0, `Cannot click: ${selector}`)
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: rect.x, y: rect.y })
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: rect.x, y: rect.y, button: 'left', clickCount: 1 })
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: rect.x, y: rect.y, button: 'left', clickCount: 1 })
    await sleep(100)
  }
  /** Open an HTML text as a file page. */
  async function open (html, name) {
    const file = join(work, name + '.html')
    writeFileSync(file, html)
    await send('Page.navigate', { url: pathToFileURL(file).href })
  }
  return { send, evaluate, waitFor, click, open, close, errors, failures }
}
