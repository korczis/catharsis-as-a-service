// @ts-check
// End-to-end contract for the site. Runs against a local subpath preview or, with BASE_URL, production.
const fs = require('node:fs');
const path = require('node:path');
const { test, expect } = require('@playwright/test');

const BASE = new URL(process.env.BASE_URL || 'http://127.0.0.1:4173/catharsis-as-a-service/');
const PRODUCTION = Boolean(process.env.BASE_URL);
const SCREENSHOTS = path.join('screenshots', PRODUCTION ? 'production' : 'local');
const LOCALES = [
  { code: 'en', path: '', about: 'About' },
  { code: 'cs', path: 'cs/', about: 'O projektu' },
];
const VIEWPORTS = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 1000 },
  { name: 'wide', width: 1920, height: 1080 },
];
const EXTRA_WIDTHS = [320, 375, 430, 1024, 1280];

const url = (relative) => new URL(relative, BASE).href;

function watch(page) {
  const problems = [];
  page.on('console', (message) => {
    if (message.type() === 'error') problems.push(`console: ${message.text()}`);
  });
  page.on('pageerror', (error) => problems.push(`pageerror: ${error.message}`));
  page.on('requestfailed', (request) => {
    const reason = request.failure()?.errorText ?? '';
    // ERR_ABORTED is the browser cancelling a request it no longer needs (srcset switch, navigation).
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

const overflow = (page) =>
  page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

async function scrollThrough(page) {
  await page.evaluate(async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += 700) {
      window.scrollTo(0, y);
      await new Promise((resolve) => setTimeout(resolve, 40));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForLoadState('networkidle');
}

test.beforeAll(() => fs.mkdirSync(SCREENSHOTS, { recursive: true }));

for (const locale of LOCALES) {
  for (const viewport of VIEWPORTS) {
    test(`${locale.code} ${viewport.name} ${viewport.width}×${viewport.height}: renders cleanly`, async ({ page }) => {
      const problems = watch(page);
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      const response = await open(page, locale.path);

      expect(response?.status()).toBe(200);
      await expect(page.locator('html')).toHaveAttribute('lang', locale.code);
      await expect(page.locator('h1')).toHaveCount(1);

      const hero = page.locator('#experience img');
      await expect(hero).toBeVisible();
      const box = await hero.evaluate((img) => ({
        loaded: img.complete && img.naturalWidth > 0,
        ratio: img.getBoundingClientRect().height / img.getBoundingClientRect().width,
      }));
      expect(box.loaded).toBe(true);
      expect(box.ratio).toBeGreaterThan(1.45);
      expect(box.ratio).toBeLessThan(1.55);

      await scrollThrough(page);
      expect(await overflow(page)).toBeLessThanOrEqual(0);

      const broken = await page.evaluate(() =>
        [...document.images]
          .filter((img) => img.offsetParent !== null)
          .filter((img) => !(img.complete && img.naturalWidth > 0))
          .map((img) => img.currentSrc || img.src),
      );
      expect(broken).toEqual([]);

      const fonts = await page.evaluate(() =>
        [...document.fonts].filter((face) => face.status === 'loaded').map((face) => face.family.replace(/"/g, '')),
      );
      expect(fonts).toEqual(expect.arrayContaining(['Anton', 'JetBrains Mono']));
      expect(await page.evaluate(() => window.__caasAlpineInits)).toBe(1);

      await page.screenshot({
        path: path.join(SCREENSHOTS, `${locale.code}-${viewport.name}.png`),
        fullPage: true,
      });
      expect(problems).toEqual([]);
    });
  }

  test(`${locale.code}: no horizontal overflow at ${EXTRA_WIDTHS.join(', ')} px`, async ({ page }) => {
    const problems = watch(page);
    for (const width of EXTRA_WIDTHS) {
      await page.setViewportSize({ width, height: 900 });
      await open(page, locale.path);
      expect(await overflow(page), `overflow at ${width}px`).toBeLessThanOrEqual(0);
    }
    expect(problems).toEqual([]);
  });

  test(`${locale.code}: metadata is complete and self-canonical`, async ({ page, request }) => {
    const problems = watch(page);
    await open(page, locale.path);
    const expected = url(locale.path);

    expect(await page.locator('link[rel="canonical"]').getAttribute('href')).toBe(expected);
    expect(await page.locator('meta[property="og:url"]').getAttribute('content')).toBe(expected);
    for (const code of ['en', 'cs', 'x-default']) {
      await expect(page.locator(`link[rel="alternate"][hreflang="${code}"]`)).toHaveCount(1);
    }
    expect(await page.locator('meta[name="description"]').getAttribute('content')).toBeTruthy();
    await expect(page).toHaveTitle(/Catharsis as a Service/);

    const image = await page.locator('meta[property="og:image"]').getAttribute('content');
    expect((await request.get(String(image))).status()).toBe(200);
    expect(problems).toEqual([]);
  });

  for (const relative of ['about/', 'artifacts/', 'artifacts/catharsis-as-a-service/']) {
    test(`${locale.code}: /${relative} renders`, async ({ page }) => {
      const problems = watch(page);
      const response = await open(page, `${locale.path}${relative}`);
      expect(response?.status()).toBe(200);
      await expect(page.locator('html')).toHaveAttribute('lang', locale.code);
      await expect(page.locator('h1')).toHaveCount(1);
      expect(await overflow(page)).toBeLessThanOrEqual(0);
      expect(problems).toEqual([]);
    });
  }
}

test('diagnostic view switch works by pointer and keyboard', async ({ page }) => {
  const problems = watch(page);
  await open(page, '');
  const panel = (name) => page.locator(`#panel-${name}`);

  await expect(panel('experience')).toBeVisible();
  await expect(panel('raw')).toBeHidden();

  await page.locator('#tab-raw').click();
  await expect(panel('raw')).toBeVisible();
  await expect(panel('raw')).toContainText('"problem_solved": false');
  await expect(panel('experience')).toBeHidden();
  await expect(page.locator('#tab-raw')).toHaveAttribute('aria-selected', 'true');

  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#tab-experience')).toBeFocused();
  await expect(panel('experience')).toBeVisible();

  await page.keyboard.press('ArrowRight');
  await expect(panel('diagnostic')).toBeVisible();
  await expect(panel('diagnostic')).toContainText('200 OK');
  expect(problems).toEqual([]);
});

test('artwork viewer (Flowbite modal) opens, traps focus and closes', async ({ page }) => {
  const problems = watch(page);
  await open(page, '');
  const trigger = page.locator('#experience [data-artwork-open]');
  const viewer = page.locator('#artwork-viewer');
  const close = viewer.locator('[data-artwork-close]');

  await trigger.click();
  await expect(viewer).toBeVisible();
  await expect(close).toBeFocused();
  await expect
    .poll(() => viewer.locator('img').evaluate((img) => img.complete && img.naturalWidth > 0))
    .toBe(true);

  await page.keyboard.press('Tab');
  await expect(close).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(viewer).toBeHidden();
  await expect(trigger).toBeFocused();

  await trigger.click();
  await expect(viewer).toBeVisible();
  await page.mouse.click(10, 500);
  await expect(viewer).toBeHidden();
  expect(problems).toEqual([]);
});

test('mobile navigation (Flowbite drawer) opens, closes and navigates', async ({ page }) => {
  const problems = watch(page);
  await page.setViewportSize({ width: 390, height: 844 });
  await open(page, '');
  const opener = page.locator('header [data-drawer-open]');
  const drawer = page.locator('#nav-drawer');

  await expect(drawer).not.toBeInViewport();
  await opener.click();
  await expect(drawer).toBeInViewport();
  await expect(opener).toHaveAttribute('aria-expanded', 'true');
  await expect(drawer.locator('[data-drawer-close]')).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(drawer).not.toBeInViewport();
  await expect(opener).toHaveAttribute('aria-expanded', 'false');

  await opener.click();
  await drawer.getByRole('link', { name: 'Diagnostic' }).click();
  await expect(drawer).not.toBeInViewport();
  await expect(page).toHaveURL(/#diagnostic$/);
  expect(problems).toEqual([]);
});

test('conceptual metrics tooltip (Flowbite) appears on hover', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await open(page, '');
  const tooltip = page.locator('#tooltip-conceptual');
  await expect(tooltip).toBeHidden();
  await page.locator('[data-tooltip-target="tooltip-conceptual"]').hover();
  await expect(tooltip).toBeVisible();
});

test('endpoint copy button copies the request (Alpine)', async ({ page, context }) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: BASE.origin });
  await open(page, '');
  const button = page.locator('#endpoint .terminal-bar [data-requires-js]');
  await button.click();
  await expect(button).toHaveText('Copied');
  expect(await page.evaluate(() => navigator.clipboard.readText())).toContain('curl -X POST /v1/catharsis');
});

test('content remains readable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, locale: 'en-US' });
  const page = await context.newPage();
  await page.goto(BASE.href);
  await expect(page.locator('h1')).toContainText('Catharsis');
  for (const name of ['experience', 'diagnostic', 'raw']) {
    await expect(page.locator(`#panel-${name}`)).toBeVisible();
  }
  await expect(page.locator('#experience img')).toBeVisible();
  await context.close();
});

test.describe('locale negotiation', () => {
  test('a Czech browser lands on /cs/ from the neutral root', async ({ browser }) => {
    const context = await browser.newContext({ locale: 'cs-CZ' });
    const page = await context.newPage();
    await page.goto(BASE.href);
    await expect(page).toHaveURL(url('cs/'));
    await expect(page.locator('html')).toHaveAttribute('lang', 'cs');
    await context.close();
  });

  test('an English browser stays on the root', async ({ browser }) => {
    const context = await browser.newContext({ locale: 'en-US' });
    const page = await context.newPage();
    await page.goto(BASE.href, { waitUntil: 'load' });
    expect(page.url()).toBe(BASE.href);
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    await context.close();
  });

  test('explicit locale URLs win over the browser preference', async ({ browser }) => {
    const czech = await browser.newContext({ locale: 'cs-CZ' });
    const czechPage = await czech.newPage();
    await czechPage.goto(url('about/'), { waitUntil: 'load' });
    expect(czechPage.url()).toBe(url('about/'));
    await expect(czechPage.locator('html')).toHaveAttribute('lang', 'en');
    await czech.close();

    const english = await browser.newContext({ locale: 'en-US' });
    const englishPage = await english.newPage();
    await englishPage.goto(url('cs/'), { waitUntil: 'load' });
    expect(englishPage.url()).toBe(url('cs/'));
    await english.close();
  });

  test('a manual choice overrides the browser preference without redirect loops', async ({ browser }) => {
    const context = await browser.newContext({ locale: 'cs-CZ', viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();
    let navigations = 0;
    page.on('framenavigated', (frame) => {
      if (frame === page.mainFrame()) navigations += 1;
    });

    await page.goto(BASE.href);
    await expect(page).toHaveURL(url('cs/'));
    await page.locator('header .locale-switcher a[hreflang="en"]').click();
    await expect(page).toHaveURL(BASE.href);
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    expect(await page.evaluate(() => localStorage.getItem('caas.locale'))).toBe('en');

    navigations = 0;
    await page.goto(BASE.href, { waitUntil: 'load' });
    await page.waitForTimeout(750);
    expect(page.url()).toBe(BASE.href);
    expect(navigations).toBe(1);
    await context.close();
  });

  test('the language switch keeps the equivalent page', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await open(page, 'about/');
    await page.locator('header .locale-switcher a[hreflang="cs"]').click();
    await expect(page).toHaveURL(url('cs/about/'));
    await expect(page.locator('h1')).toHaveText(LOCALES[1].about);
  });
});

test('unknown routes render the bespoke 404', async ({ page }) => {
  const response = await page.goto(url(PRODUCTION ? '__state-transition-failed__/' : '404.html'));
  if (PRODUCTION) expect(response?.status()).toBe(404);
  await expect(page.locator('h1')).toHaveText(/state transition failed/i);
  await expect(page.locator('body')).toContainText('problem_solved: false');
  expect(await page.evaluate(() => getComputedStyle(document.documentElement).backgroundColor)).toBe('rgb(5, 5, 5)');
});
