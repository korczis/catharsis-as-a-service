// @ts-check
// The audience lens: ?view= decides how much apparatus is unfolded, never what is claimed.
// Everything a lens reveals is in the document at every lens, so the no-JS document is whole.
const fs = require('node:fs');
const path = require('node:path');
const { test, expect } = require('@playwright/test');

const BASE = new URL(process.env.BASE_URL || 'http://127.0.0.1:4173/catharsis-as-a-service/');
const SANDBOX = { en: 'detection-sandbox/', cs: 'cs/detection-sandbox/' };
const LANDING = { en: '', cs: 'cs/' };

const url = (relative) => new URL(relative, BASE).href;

// The lens vocabulary comes from the file the page reads, not from a second copy in the test.
const TAXONOMY = fs.readFileSync(path.join(__dirname, '..', 'data', 'audiences.toml'), 'utf8');

const LENSES = TAXONOMY.split(/^\[\[audiences\]\]\s*$/m)[0]
  .split(/^\[\[lenses\]\]\s*$/m)
  .slice(1)
  .map((entry) => {
    const id = /^id\s*=\s*"([^"]+)"/m.exec(entry);
    const label = /^label\s*=\s*\{\s*en\s*=\s*"([^"]*)"\s*,\s*cs\s*=\s*"([^"]*)"\s*\}/m.exec(entry);
    return id && label ? { id: id[1], en: label[1], cs: label[2] } : null;
  })
  .filter(Boolean);

const DEFAULT_LENS = /^default_lens\s*=\s*"([^"]+)"/m.exec(TAXONOMY)[1];

test.beforeAll(() => {
  expect(LENSES).toHaveLength(6);
  expect(LENSES.map((lens) => lens.id)).toContain(DEFAULT_LENS);
});

function watch(page) {
  const problems = [];
  page.on('console', (message) => {
    if (message.type() === 'error') problems.push(`console: ${message.text()}`);
  });
  page.on('pageerror', (error) => problems.push(`pageerror: ${error.message}`));
  page.on('requestfailed', (request) => {
    const reason = request.failure()?.errorText ?? '';
    if (request.url().startsWith(BASE.origin) && !reason.includes('ERR_ABORTED')) {
      problems.push(`requestfailed: ${request.url()} ${reason}`);
    }
  });
  page.on('response', (response) => {
    if (response.url().startsWith(BASE.origin) && response.status() >= 400) {
      problems.push(`http ${response.status()}: ${response.url()}`);
    }
  });
  return problems;
}

async function open(page, relative) {
  const response = await page.goto(url(relative), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await expect(page.locator('html')).toHaveAttribute('data-alpine', 'ready');
  return response;
}

const block = (page, lens) => page.locator(`[data-lens-for~="${lens}"]`).first();
const option = (page, lens) => page.locator(`.lens-switch [data-lens-option="${lens}"]`).first();

test('the sandbox opens at the default lens', async ({ page }) => {
  const problems = watch(page);
  await open(page, SANDBOX.en);

  await expect(page.locator('html')).toHaveAttribute('data-lens', DEFAULT_LENS);
  await expect(block(page, 'essential')).toBeVisible();
  await expect(block(page, 'technical')).toBeHidden();

  expect(problems).toEqual([]);
});

test('?view=technical unfolds the technical lens in both languages', async ({ page }) => {
  for (const [code, relative] of Object.entries(SANDBOX)) {
    const problems = watch(page);
    await open(page, `${relative}?view=technical`);

    await expect(page.locator('html')).toHaveAttribute('data-lens', 'technical');
    await expect(block(page, 'technical'), code).toBeVisible();
    await expect(block(page, 'essential'), code).toBeHidden();

    expect(problems, relative).toEqual([]);
    page.removeAllListeners();
  }
});

test('choosing a lens writes the address, and Back walks it home', async ({ page }) => {
  const problems = watch(page);
  await open(page, SANDBOX.en);

  await option(page, 'research').click();
  await expect.poll(() => page.url()).toContain('?view=research');
  await expect(option(page, 'research')).toHaveAttribute('aria-current', 'true');
  await expect(option(page, 'technical')).toHaveAttribute('aria-current', 'false');
  await expect(page.locator('html')).toHaveAttribute('data-lens', 'research');
  await expect(block(page, 'research')).toBeVisible();

  await option(page, 'technical').click();
  await expect.poll(() => page.url()).toContain('?view=technical');
  await expect(page.locator('html')).toHaveAttribute('data-lens', 'technical');

  await page.goBack();
  await expect.poll(() => page.url()).toContain('?view=research');
  await expect(page.locator('html')).toHaveAttribute('data-lens', 'research');
  await expect(option(page, 'research')).toHaveAttribute('aria-current', 'true');

  expect(problems).toEqual([]);
});

test('an unknown lens falls back to the default', async ({ page }) => {
  const problems = watch(page);
  await open(page, `${SANDBOX.en}?view=nonsense`);

  await expect(page.locator('html')).toHaveAttribute('data-lens', DEFAULT_LENS);
  await expect(block(page, DEFAULT_LENS)).toBeVisible();

  expect(problems).toEqual([]);
});

test('without JavaScript the document is still complete', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  const response = await page.goto(url(`${SANDBOX.en}?view=research`), { waitUntil: 'load' });
  expect(response?.status()).toBe(200);

  // The research material is in the markup even where CSS keeps it folded away.
  const research = block(page, 'research');
  await expect(research).toHaveCount(1);
  const heading = await research.locator('h2').first().textContent();
  expect((heading || '').trim().length).toBeGreaterThan(0);
  const body = await research.textContent();
  expect((body || '').trim().length).toBeGreaterThan(40);
  expect(await page.content()).toContain((heading || '').trim());

  // The switch is real links, so a lens can be reached and sent before any script runs.
  const links = page.locator('.lens-switch a[data-lens-option]');
  await expect(links).toHaveCount(LENSES.length);
  for (const href of await links.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href')))) {
    expect(href).toContain('?view=');
  }

  await context.close();
});

test('every lens renders in Czech with Czech labels', async ({ page }) => {
  for (const lens of LENSES) {
    const problems = watch(page);
    await open(page, `${SANDBOX.cs}?view=${lens.id}`);
    await expect(page.locator('html')).toHaveAttribute('data-lens', lens.id);

    const heading = await block(page, lens.id).locator('h2').first().textContent();
    expect((heading || '').trim().length, `${lens.id} heading`).toBeGreaterThan(0);

    expect(problems, lens.id).toEqual([]);
    page.removeAllListeners();
  }

  await open(page, SANDBOX.cs);
  const labels = await page
    .locator('.lens-switch [data-lens-option]')
    .evaluateAll((nodes) => nodes.map((node) => node.textContent.trim()));
  expect(labels).toEqual(LENSES.map((lens) => lens.cs));
});

test('the landing page offers one entry point per lens', async ({ page }) => {
  for (const [code, relative] of Object.entries(LANDING)) {
    const problems = watch(page);
    await open(page, relative);

    const entries = page.locator('.audience-entries .audience-entry');
    await expect(entries, code).toHaveCount(LENSES.length);

    for (let index = 0; index < LENSES.length; index += 1) {
      const entry = entries.nth(index);
      await expect(entry.locator('.audience-question')).toHaveText(/\S/);
      const hrefs = await entry
        .locator('a')
        .evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href') || ''));
      expect(hrefs.some((href) => href.includes('?view=')), `${code} entry ${index}`).toBe(true);
    }

    const labels = await page
      .locator('.audience-entries .audience-lens')
      .evaluateAll((nodes) => nodes.map((node) => node.textContent.trim()));
    expect(labels).toEqual(LENSES.map((lens) => (code === 'cs' ? lens.cs : lens.en)));

    expect(problems, relative).toEqual([]);
    page.removeAllListeners();
  }
});
