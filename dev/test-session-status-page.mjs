#!/usr/bin/env node
// Open a built session-status page in headless Chrome: selecting text shows a copy button, and pressing it puts the selection on the clipboard.
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { launch, sleep } from './browser-cdp.mjs'

const pagePath = process.argv.slice(2).find(arg => !arg.startsWith('--'))
assert(pagePath, 'give the page to open')
const page = readFileSync(resolve(pagePath), 'utf8')
const expected = (process.argv.find(arg => arg.startsWith('--expect-label=')) || '').slice('--expect-label='.length)
const checks = []
const check = (value, label) => { assert(value, label); checks.push(label) }
const browser = await launch({ width: 1200, height: 900 })
const { send, evaluate, waitFor, click, open } = browser
try {
  await send('Browser.grantPermissions', { permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite'] }).catch(() => {})
  await open(page, 'status')
  await waitFor("document.querySelector('#status-page')?.dataset.ready === 'true'", 'Vue mount', 60000)
  await sleep(250)
  check(await evaluate('!document.querySelector("#copySelection") || document.querySelector("#copySelection").hidden'), 'no button before anything is selected')
  const select = selector => evaluate(`(() => { const node = document.querySelector(${JSON.stringify(selector)}); const range = document.createRange(); range.selectNodeContents(node); getSelection().removeAllRanges(); getSelection().addRange(range); return getSelection().toString() })()`)
  const selected = await select('#status-page h1')
  check(selected.trim().length > 0, 'the page has a title to select')
  await waitFor("document.querySelector('#copySelection') && !document.querySelector('#copySelection').hidden", 'the button appears on selecting text', 5000)
  const button = await evaluate("(() => { const b = document.querySelector('#copySelection'); const r = b.getBoundingClientRect(); return { label: b.getAttribute('aria-label'), title: b.title, svg: !!b.querySelector('svg'), inView: r.top >= 0 && r.left >= 0 && r.right <= innerWidth && r.width > 0 } })()")
  check(button.svg && button.inView && button.title === button.label, 'the button has an inline icon, a label and sits on the screen')
  if (expected) check(button.label === expected, `the button label comes from the labels: ${button.label}`)
  await evaluate("navigator.clipboard.writeText('before')")
  await click('#copySelection')
  await waitFor("document.querySelector('#copySelection').title === document.querySelector('#copySelection').getAttribute('aria-label') && !!document.querySelector('#copySelection svg path[d=\"M20 6 9 17l-5-5\"]')", 'the button shows the copied state', 5000)
  check(await evaluate('navigator.clipboard.readText()') === selected, 'pressing the button puts the selected text on the clipboard')
  check(await evaluate('getSelection().toString()') === selected, 'the selection stays after copying')
  await waitFor("!!document.querySelector('#copySelection svg rect')", 'the button goes back to the copy icon', 5000)
  await evaluate('getSelection().removeAllRanges()')
  await waitFor("document.querySelector('#copySelection').hidden", 'the button disappears when the selection is cleared', 5000)
  // Text typed into a field is the viewer's own; no button there.
  const field = await evaluate("(() => { const f = document.querySelector('#status-page textarea, #status-page input[type=text]'); if (!f) return false; f.value = 'typed text'; f.focus(); f.select(); return true })()")
  check(field, 'the page has a field to select text in')
  await sleep(400)
  check(await evaluate("document.querySelector('#copySelection').hidden"), 'no button for text selected in a field')
  // Without the Clipboard API and without execCommand the page says that copying was refused.
  await evaluate("document.activeElement?.blur()")
  await select('#status-page h1')
  await waitFor("!document.querySelector('#copySelection').hidden", 'the button appears again', 5000)
  await evaluate("Object.defineProperty(navigator, 'clipboard', { value: undefined, configurable: true }); document.execCommand = () => false")
  await click('#copySelection')
  await waitFor("!document.querySelector('#copySelectionNotice').hidden && document.querySelector('#copySelectionNotice').textContent.length > 0", 'a refused copy is told', 5000)
  check(browser.errors.length === 0, 'no console errors: ' + browser.errors.join('\n'))
  process.stdout.write(JSON.stringify({ ok: true, checks: checks.length, results: checks }) + '\n')
} catch (error) {
  process.stderr.write(JSON.stringify({ ok: false, browser: 'failed', message: error.message, consoleErrors: browser.errors, networkFailures: browser.failures }) + '\n')
  process.exitCode = 1
} finally {
  await browser.close()
}
