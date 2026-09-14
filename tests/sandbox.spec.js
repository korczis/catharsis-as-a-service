// @ts-check
// The detection sandbox: the panel must show what static/js/sandbox.js computes, must never
// reduce the readings to one, and must stay readable without JavaScript.
const { test, expect } = require('@playwright/test');

const BASE = new URL(process.env.BASE_URL || 'http://127.0.0.1:4173/catharsis-as-a-service/');
const PAGES = [
  { code: 'en', path: 'detection-sandbox/' },
  { code: 'cs', path: 'cs/detection-sandbox/' },
];
const SIGNAL_KEYS = ['heart', 'movement', 'vocal', 'alignment', 'reported'];
const DERIVED_KEYS = ['arousal', 'synchrony', 'effort', 'gap'];

const url = (relative) => new URL(relative, BASE).href;

// The conventions of tests/site.spec.js, copied rather than imported so each spec stands alone.
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

const panel = (page) => page.locator('[data-model="detection-sandbox"]');

// The labels the page renders with, read from the page itself rather than restated here.
const labelsOf = async (page) =>
  JSON.parse((await panel(page).getAttribute('data-labels')) || '{}');

async function setSignals(page, signals) {
  for (const key of SIGNAL_KEYS) {
    if (!(key in signals)) continue;
    await page.locator(`#ds-${key}`).evaluate((el, value) => {
      el.value = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }, signals[key]);
  }
}

const readSignals = (page) =>
  page.evaluate(
    (keys) =>
      Object.fromEntries(keys.map((key) => [key, Number(document.getElementById(`ds-${key}`).value)])),
    SIGNAL_KEYS,
  );

const shares = async (page) =>
  (await page.locator('[data-output="readings"] .sandbox-reading-share').allTextContents()).map(
    (text) => Number.parseFloat(text.replace('%', '').trim()),
  );

test('the sandbox page renders in both languages', async ({ page }) => {
  for (const locale of PAGES) {
    const problems = watch(page);
    const response = await open(page, locale.path);
    expect(response?.status(), locale.path).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(panel(page)).toBeVisible();

    const labels = await labelsOf(page);
    expect(labels.banner, `${locale.code} banner`).toBeTruthy();
    await expect(page.locator('.sandbox .sim-banner')).toHaveText(labels.banner);
    // The banner has to say the inputs are not measurements.
    expect(labels.banner).toMatch(/synthetic|uměl/i);

    expect(problems, locale.path).toEqual([]);
    page.removeAllListeners();
  }
});

test('the derived features are what sandbox.js derives', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'detection-sandbox/');

  const signals = { heart: 168, movement: 82, vocal: 34, alignment: 77, reported: 41 };
  await setSignals(page, signals);

  // The expectation comes from the function under test, evaluated in the page, so the
  // assertion is that the panel shows derive()'s result and not that it shows a constant.
  const expected = await page.evaluate((s) => window.caasSandbox.derive(s), signals);
  for (const key of DERIVED_KEYS) {
    await expect
      .poll(() => page.locator(`[data-output="${key}"]`).textContent(), { message: key })
      .toBe(String(expected[key]));
  }

  expect(problems).toEqual([]);
});

test('every reading is listed and the shares sum to a hundred', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'detection-sandbox/');
  await setSignals(page, { heart: 150, movement: 70, vocal: 55, alignment: 60, reported: 50 });

  const readings = page.locator('[data-output="readings"] li.sandbox-reading');
  await expect(readings).toHaveCount(5);

  // Rounding each share to a tenth costs a little: the sum has to be a hundred, not exactly.
  await expect
    .poll(async () => {
      const list = await shares(page);
      if (list.length !== 5 || !list.every(Number.isFinite)) return null;
      return Math.abs(list.reduce((sum, value) => sum + value, 0) - 100) <= 0.5;
    })
    .toBe(true);

  // A reading is never returned alone: the leader is one row of five, each one named.
  const names = await page.locator('[data-output="readings"] .sandbox-reading-name').allTextContents();
  expect(names).toHaveLength(5);
  expect(names.filter((name) => name.trim().length > 0)).toHaveLength(5);
  expect(new Set(names).size).toBe(5);

  expect(problems).toEqual([]);
});

test('the same signals lead to a different reading in a different setting', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'detection-sandbox/');

  // Search the page's own functions for signals that the two settings read differently,
  // rather than hard-coding a set that the weights could move out from under.
  const found = await page.evaluate(() => {
    const { derive, hypotheses } = window.caasSandbox;
    for (let heart = 60; heart <= 190; heart += 10) {
      for (let movement = 0; movement <= 100; movement += 10) {
        for (let vocal = 0; vocal <= 100; vocal += 10) {
          for (let alignment = 0; alignment <= 100; alignment += 10) {
            const signals = { heart, movement, vocal, alignment, reported: 50 };
            const derived = derive(signals);
            const concert = hypotheses(derived, 'concert')[0].id;
            const emergency = hypotheses(derived, 'emergency')[0].id;
            if (concert !== emergency) return { signals, concert, emergency };
          }
        }
      }
    }
    return null;
  });
  expect(found, 'no signals distinguish the two settings').not.toBeNull();

  await page.selectOption('#ds-context', 'concert');
  await setSignals(page, found.signals);

  const leader = page.locator('[data-output="readings"] li.sandbox-reading').first().locator('.sandbox-reading-name');
  const labels = await labelsOf(page);
  await expect.poll(() => leader.textContent()).toBe(labels[`reading_${found.concert}`]);

  const before = await readSignals(page);
  await page.selectOption('#ds-context', 'emergency');
  await expect.poll(() => leader.textContent()).toBe(labels[`reading_${found.emergency}`]);
  const after = await readSignals(page);

  // The demonstration only demonstrates anything if the inputs did not move.
  expect(after).toEqual(before);
  expect(problems).toEqual([]);
});

test('two close readings are reported as undecided', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'detection-sandbox/');

  const found = await page.evaluate(() => {
    const { derive, hypotheses, CONTEXTS } = window.caasSandbox;
    for (const context of Object.keys(CONTEXTS)) {
      for (let heart = 60; heart <= 190; heart += 5) {
        for (let movement = 0; movement <= 100; movement += 5) {
          for (let vocal = 0; vocal <= 100; vocal += 5) {
            for (let alignment = 0; alignment <= 100; alignment += 5) {
              const signals = { heart, movement, vocal, alignment, reported: 50 };
              const ranked = hypotheses(derive(signals), context);
              const gap = ranked[0].share - ranked[1].share;
              if (gap >= 0 && gap < 10) return { signals, context, gap };
            }
          }
        }
      }
    }
    return null;
  });
  expect(found, 'no inputs leave the top two readings within ten points').not.toBeNull();

  await page.selectOption('#ds-context', found.context);
  await setSignals(page, found.signals);

  const verdict = page.locator('[data-output="separation"]');
  await expect(verdict).toHaveAttribute('data-undecided', 'true');
  const labels = await labelsOf(page);
  await expect.poll(() => verdict.innerText()).toBe(labels.undecided);

  expect(problems).toEqual([]);
});

test('the sandbox state travels in the URL', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'detection-sandbox/?ds-context=emergency&ds-heart=170');

  await expect.poll(() => page.locator('#ds-context').inputValue()).toBe('emergency');
  await expect.poll(() => page.locator('#ds-heart').inputValue()).toBe('170');

  await setSignals(page, { movement: 23 });
  await expect.poll(() => page.url()).toContain('ds-movement=23');

  await page.locator('.sandbox-inputs button').click();
  await expect.poll(() => new URL(page.url()).search).not.toMatch(/ds-/);
  await expect.poll(() => page.locator('#ds-context').inputValue()).toBe('concert');

  expect(problems).toEqual([]);
});

test('the page is readable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  const response = await page.goto(url('detection-sandbox/'), { waitUntil: 'load' });
  expect(response?.status()).toBe(200);

  await expect(page.locator('h1')).toHaveText(/\S/);
  await expect(page.locator('.prose-page')).toContainText(/\S/);

  const labels = JSON.parse((await panel(page).getAttribute('data-labels')) || '{}');
  expect(labels.nojs).toBeTruthy();
  // The explanation is delivered by the document itself, not assembled by a script.
  await expect(page.locator('noscript')).toHaveCount(1);
  expect(await page.locator('noscript').innerHTML()).toContain(labels.nojs);

  for (const id of ['sandbox-assumptions-title', 'sandbox-limits-title']) {
    const section = page.locator(`section[aria-labelledby="${id}"]`);
    await expect(section.locator('h2')).toHaveText(/\S/);
    expect(await section.locator('li').count()).toBeGreaterThan(0);
    await expect(section.locator('li').first()).toHaveText(/\S/);
  }

  await context.close();
});

test('the panel is operable and labelled', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'detection-sandbox/');

  const ranges = page.locator('.sandbox-inputs input[type="range"]');
  await expect(ranges).toHaveCount(SIGNAL_KEYS.length);
  for (const id of await ranges.evaluateAll((nodes) => nodes.map((node) => node.id))) {
    expect(id, 'a range input has no id to label').toBeTruthy();
    await expect(page.locator(`label[for="${id}"]`)).toHaveCount(1);
    await expect(page.locator(`label[for="${id}"]`)).toHaveText(/\S/);
  }
  await expect(page.locator('label[for="ds-context"]')).toHaveText(/\S/);

  await expect(page.locator('figure.sandbox')).toHaveAccessibleName(/\S/);

  // The value readouts are the panel's live regions: <output> carries role=status implicitly.
  const outputs = page.locator('.sandbox-inputs output');
  await expect(outputs).toHaveCount(SIGNAL_KEYS.length);
  for (const key of SIGNAL_KEYS) {
    await expect(page.locator(`#ds-${key}-value`)).toHaveText(/\d/);
  }

  await page.locator('#ds-context').focus();
  await expect(page.locator('#ds-context')).toBeFocused();
  const reset = page.locator('.sandbox-inputs button');
  let reached = false;
  for (let step = 0; step < 12 && !reached; step += 1) {
    await page.keyboard.press('Tab');
    reached = await reset.evaluate((node) => node === document.activeElement);
  }
  expect(reached, 'the reset button is not reachable from the context select by Tab').toBe(true);

  expect(problems).toEqual([]);
});
