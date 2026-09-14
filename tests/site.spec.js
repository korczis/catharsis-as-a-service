// @ts-check
// End-to-end contract for the site. Runs against a local subpath preview or, with BASE_URL, production.
const fs = require('node:fs');
const path = require('node:path');
const { test, expect } = require('@playwright/test');

const BASE = new URL(process.env.BASE_URL || 'http://127.0.0.1:4173/catharsis-as-a-service/');
const PRODUCTION = Boolean(process.env.BASE_URL);
const SCREENSHOTS = path.join('screenshots', PRODUCTION ? 'production' : 'local');
const LOCALES = [
  { code: 'en', path: '', about: 'About', glossary: 'glossary/', models: 'models/', search: 'search/' },
  { code: 'cs', path: 'cs/', about: 'O projektu', glossary: 'slovnik/', models: 'modely/', search: 'hledat/' },
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

// project.no-scroll-containers: the page scrolls, nothing inside it does. The mobile navigation drawer
// is the one exception — a full-height panel whose scroll stands in for the page's own.
const scrollContainers = (page) =>
  page.evaluate(() =>
    [...document.querySelectorAll('body *')]
      .filter((el) => {
        if (el.closest('#nav-drawer')) return false;
        const style = getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return false;
        const scrolls = (axis, size, client) =>
          ['auto', 'scroll'].includes(style[axis]) && el[size] - el[client] > 1;
        return scrolls('overflowX', 'scrollWidth', 'clientWidth') || scrolls('overflowY', 'scrollHeight', 'clientHeight');
      })
      .map((el) => `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}.${el.className}`.trim().slice(0, 120)));

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

  test(`${locale.code}: nothing inside the page scrolls`, async ({ page }) => {
    const problems = watch(page);
    const pages = [
      locale.path,
      `${locale.path}research/venting-hypothesis/`,
      `${locale.path}research/stress-and-social-buffering/`,
      `${locale.path}methods/`,
      `${locale.path}evidence/`,
      `${locale.path}status/`,
      `${locale.path}artifacts/catharsis-as-a-service/`,
      `${locale.path}studies/`,
      `${locale.path}terms/rumination/`,
    ];
    for (const width of [390, 768, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      for (const relative of pages) {
        await open(page, relative);
        expect(await scrollContainers(page), `scroll container on /${relative} at ${width}px`).toEqual([]);
        expect(await overflow(page), `overflow on /${relative} at ${width}px`).toBeLessThanOrEqual(0);
      }
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

  for (const relative of [
    'about/',
    'guides/',
    'commands/',
    'research/',
    'advice/',
    'tags/',
    'artifacts/',
    'artifacts/catharsis-as-a-service/',
    'research/relief-is-not-resolution/',
    'research/method-majordomus/',
    'research/music-and-emotion-regulation/',
    'advice/after-trauma/',
    'methods/',
    'evidence/',
    'status/',
    'theory/',
    'artifacts/closure-as-a-service/',
    'studies/',
    'studies/watkins-2008/',
    'terms/rumination/',
    locale.glossary,
    locale.models,
    locale.search,
  ]) {
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

test('structured data describes the site, the artwork and the breadcrumb', async ({ page, request }) => {
  const graphOf = async (relative) => {
    await page.goto(url(relative));
    const blocks = await page.locator('script[type="application/ld+json"]').allTextContents();
    expect(blocks).toHaveLength(1);
    const document = JSON.parse(blocks[0]);
    expect(document['@context']).toBe('https://schema.org');
    return document['@graph'];
  };
  const byType = (graph, type) => graph.find((node) => node['@type'] === type);

  const home = await graphOf('');
  expect(home.map((node) => node['@type'])).toEqual(expect.arrayContaining(['WebSite', 'Person', 'VisualArtwork']));
  const artwork = byType(home, 'VisualArtwork');
  expect(artwork.width.value).toBe(4800);
  expect(artwork.height.value).toBe(7200);
  expect((await request.get(artwork.image)).status()).toBe(200);

  const artifact = await graphOf('cs/artifacts/catharsis-as-a-service/');
  expect(byType(artifact, 'WebSite').inLanguage).toBe('cs');
  const crumbs = byType(artifact, 'BreadcrumbList').itemListElement;
  expect(crumbs.map((crumb) => crumb.position)).toEqual([1, 2, 3]);
  expect(crumbs[0].item).toBe(url('cs/'));
  expect(crumbs[1].item).toBe(url('cs/artifacts/'));
  expect(crumbs[2].item).toBe(url('cs/artifacts/catharsis-as-a-service/'));
});

test('link previews are localized and reachable', async ({ page, request }) => {
  const preview = async (relative) => {
    await page.goto(url(relative));
    const read = (selector) => page.locator(selector).first().getAttribute('content');
    return {
      image: await read('meta[property="og:image"]'),
      alt: await read('meta[property="og:image:alt"]'),
      locale: await read('meta[property="og:locale"]'),
      alternate: await read('meta[property="og:locale:alternate"]'),
      card: await read('meta[name="twitter:card"]'),
    };
  };
  const en = await preview('');
  const cs = await preview('cs/');
  expect([en.locale, en.alternate]).toEqual(['en_US', 'cs_CZ']);
  expect([cs.locale, cs.alternate]).toEqual(['cs_CZ', 'en_US']);
  expect(en.image).not.toBe(cs.image);
  for (const card of [en, cs]) {
    expect(card.card).toBe('summary_large_image');
    expect(card.alt).toBeTruthy();
    const response = await request.get(String(card.image));
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toMatch(/image\/(png|jpeg)/);
  }
});

test('feeds, sitemap alternates, favicon and manifest icons are served', async ({ request }) => {
  for (const [relative, code] of [['atom.xml', 'en'], ['cs/atom.xml', 'cs']]) {
    const response = await request.get(url(relative));
    expect(response.status()).toBe(200);
    const body = await response.text();
    expect(body).toContain('<feed');
    expect(body).toContain(`xml:lang="${code}"`);
    expect(body).toContain('Catharsis as a Service');
  }

  const sitemap = await (await request.get(url('sitemap.xml'))).text();
  const entries = sitemap.match(/<url>[\s\S]*?<\/url>/g) ?? [];
  expect(entries.length).toBeGreaterThan(0);
  // Tag term pages have no translated counterpart, so only they may omit alternates.
  for (const entry of entries) {
    const loc = entry.match(/<loc>([^<]+)<\/loc>/)[1];
    const isTerm = /\/tags\/[^/]+\/$/.test(loc);
    for (const code of ['en', 'cs', 'x-default']) {
      expect(entry.includes(`hreflang="${code}"`), `${loc} ${code}`).toBe(!isTerm);
    }
  }

  expect((await request.get(url('favicon.ico'))).status()).toBe(200);
  const manifest = await (await request.get(url('site.webmanifest'))).json();
  for (const icon of manifest.icons) {
    expect((await request.get(url(icon.src))).status(), icon.src).toBe(200);
  }
});

test('the content API is served next to the site', async ({ request }) => {
  const index = await (await request.get(url('api/v1/index.json'))).json();
  expect(index.api_version).toBe(1);
  expect(index.endpoint).toEqual({ method: 'POST', path: '/v1/catharsis', status: 200, problem_solved: false });
  for (const language of index.languages) {
    const advice = await request.get(url(`api/v1/${index.collections.advice[language]}`));
    expect(advice.status()).toBe(200);
    const entries = await advice.json();
    expect(entries.length).toBeGreaterThan(0);
    for (const entry of entries) expect(entry.url.startsWith(index.site)).toBe(true);
  }
});

test('the FAQ uses a working Flowbite accordion', async ({ page }) => {
  await open(page, '');
  const buttons = page.locator('#faq-accordion [data-accordion-target]');
  expect(await buttons.count()).toBeGreaterThan(3);
  await expect(page.locator('#faq-body-1')).toBeVisible();
  await expect(page.locator('#faq-body-2')).toBeHidden();
  await buttons.nth(1).click();
  await expect(page.locator('#faq-body-2')).toBeVisible();
  await expect(buttons.nth(1)).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#faq-body-1')).toBeHidden();
});

test('research and advice pages carry breadcrumbs, references and localized previews', async ({ page, request }) => {
  for (const locale of LOCALES) {
    for (const relative of ['research/what-is-catharsis/', 'advice/reappraise/']) {
      await open(page, `${locale.path}${relative}`);
      await expect(page.locator('nav.breadcrumb li')).toHaveCount(3);
      await expect(page.locator('nav.breadcrumb [aria-current="page"]')).toHaveCount(1);
      const references = page.locator('.references li');
      expect(await references.count()).toBeGreaterThan(0);
      const doi = page.locator('.references a[href^="https://doi.org/"]').first();
      if ((await doi.count()) > 0) expect(await doi.getAttribute('href')).toMatch(/^https:\/\/doi\.org\/10\./);
      const image = await page.locator('meta[property="og:image"]').getAttribute('content');
      expect((await request.get(String(image))).status()).toBe(200);
      await expect(page.locator('.tag-list a[rel="tag"]').first()).toBeVisible();
    }
  }
});

test('print styles turn the artifact into a paper document', async ({ page }) => {
  await open(page, '');
  await page.emulateMedia({ media: 'print' });
  await expect(page.locator('header.site-header')).toBeHidden();
  for (const name of ['experience', 'diagnostic', 'raw']) {
    await expect(page.locator(`#panel-${name}`)).toBeVisible();
  }
  const paper = () =>
    page.evaluate(() =>
      [document.documentElement, document.body].map((node) => {
        const style = getComputedStyle(node);
        return `${style.backgroundColor}|${style.color}`;
      }),
    );
  await expect.poll(paper).toEqual(['rgb(255, 255, 255)|rgb(0, 0, 0)', 'rgb(255, 255, 255)|rgb(0, 0, 0)']);
});

test('guides have a working table of contents in both languages', async ({ page }) => {
  for (const locale of LOCALES) {
    await open(page, `${locale.path}guides/`);
    const links = page.locator('nav.toc a');
    expect(await links.count()).toBeGreaterThan(4);
    const targets = await links.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href')));
    for (const target of targets) {
      await expect(page.locator(String(target))).toHaveCount(1);
    }
  }
});

test('the landing page states the thesis, the venting evidence and the clinical boundary', async ({ page }) => {
  const problems = watch(page);
  await open(page, '');
  await expect(page.locator('[data-hero-line]')).toHaveText('relief detected ≠ cause resolved');
  await expect(page.locator('#experience .kind-artistic')).toBeVisible();
  await expect(page.locator('#thesis-title')).toContainText('The body can change state');
  await expect(page.locator('#venting')).toContainText('10,189');
  await expect(page.locator('#venting')).toContainText('g = −0.63');
  await expect(page.locator('#questions .question-list li')).toHaveCount(6);
  await expect(page.locator('#boundary [role="note"]')).toContainText('emergency services');
  await expect(page.locator('#observability .badge')).toHaveText(/Artistic/);
  await expect(page.locator('#making .screen-label')).toHaveText(/illustrative data/i);
  expect(problems).toEqual([]);
});

test('claims show their grade and open their sources (Alpine), and stay open without JavaScript', async ({ page, browser }) => {
  const problems = watch(page);
  await open(page, 'evidence/');
  const cards = page.locator('#claims .claim-card');
  expect(await cards.count()).toBeGreaterThan(20);
  const card = page.locator('#claims .claim-card:has(.claim-toggle)').first();
  await expect(card.locator('.claim-badges .level-badge')).toBeVisible();
  await expect(card.locator('.claim-badges .confidence-badge')).toBeVisible();
  const panel = card.locator('.claim-sources');
  const toggle = card.locator('.claim-toggle');
  await expect(panel).toBeHidden();
  await toggle.click();
  await expect(panel).toBeVisible();
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(panel.locator('.source-item').first()).toBeVisible();
  await expect(page.locator('#sources tbody tr')).not.toHaveCount(0);
  await expect(page.locator('#changelog li').first()).toBeVisible();
  expect(problems).toEqual([]);

  const context = await browser.newContext({ javaScriptEnabled: false });
  const noJs = await context.newPage();
  await noJs.goto(url('evidence/'));
  await expect(noJs.locator('#claims .claim-sources').first()).toBeVisible();
  await context.close();
});

test('research notes list the ledger claims they make', async ({ page }) => {
  for (const locale of LOCALES) {
    await open(page, `${locale.path}research/venting-hypothesis/`);
    await expect(page.locator('.page-claims .claim-card').first()).toBeVisible();
    await expect(page.locator('.page-claims a[href*="evidence/"]')).toHaveCount(1);
  }
});

test('the detection simulation is labelled and never claims more than it can', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'methods/');
  const sim = page.locator('#simulation');
  await expect(sim.locator('.sim-banner')).toHaveText(/not biometric analysis/i);
  const out = (name) => sim.locator(`[data-output="${name}"]`);
  await expect(out('phase')).toHaveAttribute('data-phase', 'discharge');
  await expect(out('problem')).toHaveText('false');
  await expect(out('confidence')).toHaveText('LOW');

  await sim.locator('#sim-relief').fill('2');
  await expect(out('phase')).toHaveAttribute('data-phase', 'peak');
  await expect(out('problem')).toHaveText('unknown');

  await sim.locator('#sim-heart_rate').fill('0');
  await sim.locator('#sim-eda').fill('1');
  await expect(out('phase')).toHaveAttribute('data-phase', 'baseline');

  await sim.locator('#sim-cause').check();
  await expect(out('cause')).toContainText(/reported/);
  await sim.getByRole('button', { name: /reset/i }).click();
  await expect(out('phase')).toHaveAttribute('data-phase', 'discharge');
  await expect(sim.locator('#sim-cause')).not.toBeChecked();

  for (const id of ['detection-chain', 'temporal-model', 'detection-matrix', 'uncertainty', 'errors', 'architecture']) {
    await expect(page.locator(`#${id}`)).toHaveCount(1);
  }
  await expect(page.locator('#architecture [data-status="not-planned"]').first()).toBeVisible();
  expect(problems).toEqual([]);
});

test('the glossary is bilingual, anchored and described as a DefinedTermSet', async ({ page }) => {
  for (const locale of LOCALES) {
    await open(page, `${locale.path}${locale.glossary}`);
    await expect(page.locator('html')).toHaveAttribute('lang', locale.code);
    expect(await page.locator('article.term').count()).toBeGreaterThan(40);
    await expect(page.locator('#catharsis dfn')).toBeVisible();
    const letters = await page.locator('.letter-nav a').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href')));
    for (const target of letters) await expect(page.locator(String(target))).toHaveCount(1);

    expect(await page.locator('link[rel="alternate"][hreflang="en"]').getAttribute('href')).toBe(url('glossary/'));
    expect(await page.locator('link[rel="alternate"][hreflang="cs"]').getAttribute('href')).toBe(url('cs/slovnik/'));
    const graph = JSON.parse(await page.locator('script[type="application/ld+json"]').textContent())['@graph'];
    const set = graph.find((node) => node['@type'] === 'DefinedTermSet');
    expect(set.hasDefinedTerm.length).toBeGreaterThan(40);
  }
});

test('library pages are Articles with citations, never MedicalWebPage', async ({ page }) => {
  for (const relative of ['research/venting-hypothesis/', 'advice/reappraise/', 'methods/', 'evidence/', 'about/', 'cs/research/measuring-emotion/']) {
    await page.goto(url(relative));
    const text = await page.locator('script[type="application/ld+json"]').textContent();
    expect(text).not.toContain('MedicalWebPage');
    const article = JSON.parse(String(text))['@graph'].find((node) => node['@type'] === 'Article');
    expect(article, relative).toBeTruthy();
    expect(article.url).toBe(url(relative));
    if (relative.includes('research/')) expect(article.citation.length).toBeGreaterThan(0);
  }
});

test('the footer carries the science note and build metadata; /status/ is generated', async ({ page }) => {
  await open(page, 'status/');
  const footer = page.locator('footer');
  await expect(footer.locator('.footer-science')).toContainText('Nothing on this site measures');
  await expect(footer.locator('[data-build="evidence-date"]')).toHaveText(/^\d{4}-\d{2}-\d{2}$/);
  await expect(footer.locator('[data-build="version"]')).not.toBeEmpty();
  expect(Number(await page.locator('[data-stat="claims"]').textContent())).toBeGreaterThan(20);
  expect(Number(await page.locator('[data-stat="sources"]').textContent())).toBeGreaterThan(40);
  await expect(page.locator('#next-reviews-title + .table-frame tbody tr').first()).toBeVisible();
  if (PRODUCTION) await expect(page.locator('main [data-build="revision"] a, main [data-build="revision"]').first()).not.toHaveText('local');
});

// Concept screen previews: every page that renders library.screens, in both locales.
const SCREEN_PAGES = [
  { relative: '', total: 3, lang: 'en' },
  { relative: 'cs/', total: 3, lang: 'cs' },
  { relative: 'research/method-majordomus/', total: 8, lang: 'en' },
  { relative: 'cs/research/method-majordomus/', total: 8, lang: 'cs' },
  { relative: 'about/', total: 2, lang: 'en' },
  { relative: 'cs/about/', total: 2, lang: 'cs' },
];
const SCREEN_UI = {
  en: { previous: 'Previous screen', next: 'Next screen', close: 'Close', original: 'Open original PNG' },
  cs: { previous: 'Předchozí obrazovka', next: 'Další obrazovka', close: 'Zavřít', original: 'Otevřít originální PNG' },
};

function screenViewer(page) {
  const viewer = page.locator('[data-screen-viewer]:not(.poster-viewer)');
  return {
    page,
    figure: page.locator('figure.screens'),
    triggers: page.locator('figure.screens [data-screen-open]'),
    viewer,
    close: viewer.locator('[data-screen-close]'),
    prev: viewer.locator('[data-screen-prev]'),
    next: viewer.locator('[data-screen-next]'),
    count: viewer.locator('[data-screen-count]'),
    title: viewer.locator('[data-screen-title]'),
    caption: viewer.locator('[data-screen-caption]'),
    image: viewer.locator('[data-screen-image]'),
    original: viewer.locator('[data-screen-original]'),
  };
}

// The dialog shows exactly what the thumbnail at `position` shows, with its full-size image loaded,
// and the address names that screen.
async function expectScreen(s, position, total) {
  const trigger = s.triggers.nth(position);
  const id = String(await s.figure.getAttribute('id'));
  await expect(s.page).toHaveURL(new RegExp(`#${id}-${position + 1}$`));
  await expect(s.count).toHaveText(`${position + 1} / ${total}`);
  await expect(s.title).toHaveText(String(await trigger.getAttribute('data-title')));
  await expect(s.caption).toHaveText(String(await trigger.getAttribute('data-caption')));
  await expect(s.image).toHaveAttribute('alt', String(await trigger.locator('img').getAttribute('alt')));
  await expect(s.image).toHaveAttribute('src', String(await trigger.getAttribute('data-full')));
  await expect(s.original).toHaveAttribute('href', String(await trigger.getAttribute('href')));
  await expect.poll(() => s.image.evaluate((img) => img.complete && img.naturalWidth > 0)).toBe(true);
}

for (const { relative, total, lang } of SCREEN_PAGES) {
  test(`concept screen preview on /${relative}: opens in place, pages through every screen, closes`, async ({ page }) => {
    const problems = watch(page);
    const ui = SCREEN_UI[lang];
    await open(page, relative);
    const s = screenViewer(page);
    await expect(s.triggers).toHaveCount(total);
    await expect(page.locator('body > [data-screen-viewer]:not(.poster-viewer)')).toHaveCount(1);
    await expect(s.viewer).toBeHidden();
    await expect(s.prev).toHaveAttribute('aria-label', ui.previous);
    await expect(s.next).toHaveAttribute('aria-label', ui.next);
    await expect(s.close).toContainText(ui.close);
    await expect(s.original).toContainText(ui.original);

    const trigger = s.triggers.nth(1);
    await trigger.scrollIntoViewIfNeeded();
    await trigger.click();
    await expect(s.viewer).toBeVisible();
    await expect(s.viewer).toHaveAttribute('role', 'dialog');
    await expect(s.viewer).toHaveAttribute('aria-modal', 'true');
    await expect(s.close).toBeFocused();
    await expect(page.locator('body')).toHaveClass(/overflow-hidden/);
    await expectScreen(s, 1, total);
    const labelledBy = String(await s.viewer.getAttribute('aria-labelledby'));
    await expect(page.locator(`[id="${labelledBy}"]`)).toHaveText(String(await trigger.getAttribute('data-title')));

    // Next visits every remaining screen and wraps to the first.
    for (let step = 2; step <= total; step += 1) {
      await s.next.click();
      await expectScreen(s, step % total, total);
    }
    await page.keyboard.press('ArrowLeft');
    await expectScreen(s, total - 1, total);
    await page.keyboard.press('ArrowRight');
    await expectScreen(s, 0, total);
    await s.prev.click();
    await expectScreen(s, total - 1, total);

    await page.keyboard.press('Escape');
    await expect(s.viewer).toBeHidden();
    await expect(trigger).toBeFocused();
    await expect(page.locator('body')).not.toHaveClass(/overflow-hidden/);
    await expect(page).toHaveURL(url(relative));
    expect(problems).toEqual([]);
  });
}

test('concept screen preview: the address names the open screen; Back, Forward and bookmarks work', async ({ page }) => {
  const problems = watch(page);
  const relative = 'research/method-majordomus/';
  const total = 8;
  await open(page, relative);
  const s = screenViewer(page);
  const id = String(await s.figure.getAttribute('id'));

  await s.triggers.nth(1).scrollIntoViewIfNeeded();
  await s.triggers.nth(1).click();
  await expectScreen(s, 1, total);
  await s.next.click();
  await expectScreen(s, 2, total);
  await page.goBack();
  await expect(s.viewer).toBeHidden();
  await expect(page).toHaveURL(url(relative));
  await page.goForward();
  await expect(s.viewer).toBeVisible();
  await expectScreen(s, 2, total);
  await s.close.click();
  await expect(s.viewer).toBeHidden();
  await expect(page).toHaveURL(url(relative));

  // A bookmarked address opens its screen on load; closing it keeps the reader on the page.
  await open(page, 'about/');
  await open(page, `${relative}#${id}-5`);
  await expect(s.viewer).toBeVisible();
  await expectScreen(s, 4, total);
  await page.keyboard.press('Escape');
  await expect(s.viewer).toBeHidden();
  await expect(page).toHaveURL(url(relative));
  await expect(s.triggers.nth(4)).toBeFocused();

  // Addresses that name no screen leave the page as it is.
  for (const hash of [`#${id}-0`, `#${id}-${total + 1}`, `#${id}-x`, '#references-title']) {
    await open(page, 'about/');
    await open(page, `${relative}${hash}`);
    await expect(s.viewer).toBeHidden();
    await expect(page).toHaveURL(url(`${relative}${hash}`));
  }
  expect(problems).toEqual([]);
});

test('concept screen preview: keyboard opening, focus trap, print and backdrop close', async ({ page }) => {
  const problems = watch(page);
  await open(page, '');
  const s = screenViewer(page);
  const trigger = s.triggers.first();
  await trigger.focus();
  await page.keyboard.press('Enter');
  await expect(s.viewer).toBeVisible();
  await expect(s.close).toBeFocused();
  await expectScreen(s, 0, 3);

  await page.keyboard.press('Tab');
  await expect(s.original).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(s.prev).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(s.original).toBeFocused();
  await s.prev.focus();
  await page.keyboard.press('Enter');
  await expectScreen(s, 2, 3);

  await page.emulateMedia({ media: 'print' });
  await expect(s.viewer).toBeHidden();
  await page.emulateMedia({ media: 'screen' });
  await expect(s.viewer).toBeVisible();

  await page.mouse.click(10, 500);
  await expect(s.viewer).toBeHidden();
  await expect(trigger).toBeFocused();
  expect(problems).toEqual([]);
});

test('concept screen preview: Home and End, touch swipe and neighbour preloading', async ({ page }) => {
  const problems = watch(page);
  const total = 8;
  await open(page, 'research/method-majordomus/');
  const s = screenViewer(page);
  const fulls = await s.triggers.evaluateAll((nodes) => nodes.map((node) => node.dataset.full));
  const fetched = () => page.evaluate(() => performance.getEntriesByType('resource').map((entry) => entry.name));

  await s.triggers.nth(3).scrollIntoViewIfNeeded();
  await s.triggers.nth(3).click();
  await expectScreen(s, 3, total);
  await expect.poll(fetched).toEqual(expect.arrayContaining([fulls[2], fulls[4]]));

  await page.keyboard.press('End');
  await expectScreen(s, total - 1, total);
  await expect.poll(fetched).toEqual(expect.arrayContaining([fulls[0], fulls[total - 2]]));
  await page.keyboard.press('Home');
  await expectScreen(s, 0, total);

  const stroke = async (pointerType, dx, dy) => {
    const box = await s.image.boundingBox();
    if (!box) throw new Error('preview image has no layout box');
    const x = box.x + box.width / 2;
    const y = box.y + box.height / 2;
    const init = { pointerId: 7, isPrimary: true, pointerType, bubbles: true };
    await s.image.dispatchEvent('pointerdown', { ...init, clientX: x, clientY: y });
    await s.image.dispatchEvent('pointerup', { ...init, clientX: x + dx, clientY: y + dy });
  };
  await stroke('touch', -120, 10);
  await expectScreen(s, 1, total);
  await stroke('touch', 120, -10);
  await expectScreen(s, 0, total);
  await stroke('touch', 120, 0);
  await expectScreen(s, total - 1, total);
  await stroke('pen', -120, 0);
  await expectScreen(s, 0, total);
  // Too short, mostly vertical, or a mouse drag: no paging.
  await stroke('touch', -30, 0);
  await stroke('touch', -80, 140);
  await stroke('mouse', -200, 0);
  await expectScreen(s, 0, total);

  await page.keyboard.press('Escape');
  await expect(s.viewer).toBeHidden();
  expect(problems).toEqual([]);
});

test('concept screen preview: modified and non-primary clicks keep the link behaviour', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'about/');
  const s = screenViewer(page);
  const trigger = s.triggers.first();
  await expect(trigger).toHaveAttribute('href', /\/assets\/majordomus\/cockpit-[a-z]+\.png$/);

  // Whether a new tab opens depends on the operating system and browser, so this checks the page's own
  // decision instead: a window listener, which runs after the link's, records whether the preview
  // cancelled the click and then cancels it so that nothing navigates.
  const clickWith = (init) =>
    trigger.evaluate((node, options) => {
      let prevented = null;
      const record = (event) => {
        prevented = event.defaultPrevented;
        event.preventDefault();
      };
      window.addEventListener('click', record, { once: true });
      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, button: 0, ...options }));
      return prevented;
    }, init);

  for (const init of [{ ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { altKey: true }, { button: 1 }]) {
    expect(await clickWith(init), JSON.stringify(init)).toBe(false);
    await expect(s.viewer).toBeHidden();
    await expect(page).toHaveURL(url('about/'));
  }
  expect(await clickWith({})).toBe(true);
  await expect(s.viewer).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(s.viewer).toBeHidden();
  expect(problems).toEqual([]);
});

test('concept screens without JavaScript link to the original PNG and keep the dialog hidden', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(url('research/method-majordomus/'));
  const triggers = page.locator('figure.screens [data-screen-open]');
  await expect(triggers).toHaveCount(8);
  await expect(page.locator('[data-screen-viewer]:not(.poster-viewer)')).toBeHidden();

  const assets = await triggers.evaluateAll((nodes) => nodes.map((node) => ({ png: node.href, webp: node.dataset.full })));
  for (const { png, webp } of assets) {
    const original = await page.request.get(png);
    expect(original.status(), png).toBe(200);
    expect(original.headers()['content-type'], png).toContain('image/png');
    const preview = await page.request.get(String(webp));
    expect(preview.status(), webp).toBe(200);
    expect(preview.headers()['content-type'], webp).toContain('image/webp');
  }

  // The screen addresses are plain anchors, so a bookmark still lands on the screen without JavaScript.
  const id = String(await page.locator('figure.screens').getAttribute('id'));
  await expect(page.locator(`figure.screens li[id="${id}-3"]`)).toHaveCount(1);
  await page.goto(url(`research/method-majordomus/#${id}-3`));
  await expect(page.locator(`[id="${id}-3"]`)).toBeInViewport();
  await expect(page.locator('[data-screen-viewer]:not(.poster-viewer)')).toBeHidden();

  const [tab] = await Promise.all([context.waitForEvent('page'), triggers.first().click()]);
  await tab.waitForLoadState();
  expect(tab.url()).toBe(assets[0].png);
  await context.close();
});

test('concept screen preview fits a 390 px viewport', async ({ page }) => {
  const problems = watch(page);
  const viewport = { width: 390, height: 844 };
  await page.setViewportSize(viewport);
  await open(page, 'cs/');
  const s = screenViewer(page);
  await s.triggers.first().scrollIntoViewIfNeeded();
  await s.triggers.first().click();
  await expectScreen(s, 0, 3);
  for (const control of [s.prev, s.next, s.close, s.image, s.title, s.original]) {
    const box = await control.boundingBox();
    if (!box) throw new Error('control has no layout box');
    expect(box.x).toBeGreaterThanOrEqual(0);
    expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);
    expect(box.y + box.height).toBeLessThanOrEqual(viewport.height);
  }
  expect(await overflow(page)).toBeLessThanOrEqual(0);
  await s.close.click();
  await expect(s.viewer).toBeHidden();
  expect(problems).toEqual([]);
});

test('concept screen preview with a single screen hides paging and keeps focus inside', async ({ page }) => {
  const problems = watch(page);
  // No page ships a single screen, so drop all but the first from /about/ once the document is
  // parsed and before the deferred app.js runs (readyState turns interactive before deferred scripts).
  await page.addInitScript(() => {
    document.addEventListener('readystatechange', () => {
      if (document.readyState !== 'interactive') return;
      document.querySelectorAll('figure.screens li.screen:not(:first-child)').forEach((node) => node.remove());
    });
  });
  await open(page, 'about/');
  const s = screenViewer(page);
  await expect(s.triggers).toHaveCount(1);

  await s.triggers.first().click();
  await expect(s.viewer).toBeVisible();
  await expectScreen(s, 0, 1);
  for (const control of [s.prev, s.next, s.count]) await expect(control).toBeHidden();
  await expect(s.prev).toBeDisabled();
  await expect(s.next).toBeDisabled();

  await page.keyboard.press('ArrowRight');
  await expectScreen(s, 0, 1);
  await expect(s.close).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(s.original).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(s.close).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(s.original).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(s.viewer).toBeHidden();
  expect(problems).toEqual([]);
});

test('concept screens are labelled as illustrative wherever they appear', async ({ page }) => {
  for (const relative of ['research/method-majordomus/', 'about/', 'cs/about/']) {
    await open(page, relative);
    const figure = page.locator('figure.screens');
    await expect(figure.locator('.screen-label')).toBeVisible();
    const images = figure.locator('img');
    expect(await images.count()).toBeGreaterThan(1);
    for (const alt of await images.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('alt')))) {
      expect(String(alt).length).toBeGreaterThan(40);
    }
  }
});

test('interactive models respond to their inputs and stay labelled as illustrative', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'models/');
  await expect(page.locator('.sim-banner').first()).toBeVisible();

  const relief = page.locator('[data-model="relief-loop"]');
  await relief.locator('#rl-change').fill('0');
  await expect(relief.locator('[data-output="resolved"]')).toHaveAttribute('data-resolved', '0');
  await relief.locator('#rl-change').fill('30');
  await expect(relief.locator('[data-output="resolved"]')).toHaveAttribute('data-resolved', /^[1-9]\d*$/);
  await expect(relief.locator('path.series-blood')).toHaveAttribute('d', /^M/);

  const venting = page.locator('[data-model="venting-arousal"]');
  await venting.locator('input[value="venting"]').check();
  const vented = Number(await venting.locator('[data-output="at-ten"]').textContent());
  await venting.locator('input[value="calming"]').check();
  await expect.poll(async () => Number(await venting.locator('[data-output="at-ten"]').textContent())).toBeLessThan(vented);

  const peak = page.locator('[data-model="peak-end"]');
  await expect(peak.locator('[data-output="peak-end"]')).toHaveText('7');
  await expect(peak.locator('[data-output="total"]')).toHaveText('42');
  await peak.locator('[data-action="add"]').click();
  await expect(peak.locator('[data-output="peak-end"]')).toHaveText('5.5');
  await expect(peak.locator('[data-output="total"]')).toHaveText('45');

  const sync = page.locator('[data-model="synchrony"]');
  await sync.locator('#sy-coupling').fill('4');
  await sync.locator('#sy-spread').fill('0.2');
  for (let i = 0; i < 6; i += 1) await sync.locator('[data-action="step"]').click();
  await expect.poll(async () => Number(await sync.locator('[data-output="order"]').textContent())).toBeGreaterThan(0.8);

  const load = page.locator('[data-model="allostatic-load"]');
  await load.locator('#al-frequency').fill('2');
  await load.locator('#al-recovery').fill('30');
  const low = Number(await load.locator('[data-output="peak"]').textContent());
  await load.locator('#al-frequency').fill('14');
  await load.locator('#al-recovery').fill('2');
  await expect.poll(async () => Number(await load.locator('[data-output="peak"]').textContent())).toBeGreaterThan(low * 5);
  expect(problems).toEqual([]);
});

test('search finds pages and glossary terms in both languages, ignoring diacritics', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'search/?q=venting');
  const results = page.locator('.search-result');
  await expect(results.first()).toBeVisible();
  await expect(page.locator('.search-result a[href$="/research/venting-hypothesis/"]')).toHaveCount(1);
  await page.locator('[data-filter="glossary"]').click();
  await expect(page.locator('[data-filter="glossary"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('.search-result a[href*="/glossary/#venting"]')).toHaveCount(1);
  expect(problems).toEqual([]);

  await open(page, 'cs/hledat/');
  await page.locator('#search-input').fill('katarzi');
  await expect(page.locator('.search-result a[href*="/cs/"]').first()).toBeVisible();
  await expect(page).toHaveURL(/q=katarzi/);
  await page.locator('#search-input').fill('prehodnoceni');
  await expect(page.locator('.search-result').first()).toBeVisible();
});

test('library pages link their glossary terms and related reading', async ({ page }) => {
  for (const locale of LOCALES) {
    await open(page, `${locale.path}research/venting-hypothesis/`);
    const terms = page.locator('[data-terms] a');
    expect(await terms.count()).toBeGreaterThan(2);
    const target = String(await terms.first().getAttribute('href'));
    expect(target).toContain(`${locale.path}${locale.glossary}#`);
    await expect(page.locator('[data-related] .card')).not.toHaveCount(0);
  }
  await open(page, 'advice/reappraise/');
  await expect(page.locator('[data-related] .card').first()).toBeVisible();
});

test('every content page has its own social preview image', async ({ page, request }) => {
  const seen = new Set();
  for (const relative of ['', 'cs/', 'research/venting-hypothesis/', 'cs/research/venting-hypothesis/', 'models/', 'cs/slovnik/', 'artifacts/closure-as-a-service/']) {
    await page.goto(url(relative));
    const image = String(await page.locator('meta[property="og:image"]').getAttribute('content'));
    expect(image, relative).toContain('/og/');
    expect(seen.has(image), `${relative} reuses ${image}`).toBe(false);
    seen.add(image);
    const response = await request.get(image);
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toContain('image/jpeg');
    expect(await page.locator('meta[property="og:image:alt"]').getAttribute('content')).toContain('Catharsis as a Service');
  }
});

test('the theory section and the second artifact are part of the library and the series', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'theory/');
  const cards = page.locator('.card-title a');
  expect(await cards.count()).toBeGreaterThan(5);
  await cards.first().click();
  await expect(page.locator('nav.breadcrumb li')).toHaveCount(3);
  await expect(page.locator('nav.breadcrumb li').nth(1)).toContainText('Theory');
  await expect(page.locator('.kind-theoretical').first()).toBeVisible();

  await open(page, 'artifacts/closure-as-a-service/');
  await expect(page.locator('[data-status-line]')).toHaveText('grief_resolved: pending');
  await expect(page.locator('[data-hero-line]')).toContainText('≠');
  await open(page, '');
  await expect(page.locator('#archive .archive-row')).toHaveCount(2);
  await expect(page.locator('#experience [data-status-line]')).toHaveText('problem_solved: false');
  expect(problems).toEqual([]);
});

test('interactive state is bookmarkable: models, simulation, search filter and claim links', async ({ page }) => {
  const problems = watch(page);
  await open(page, 'models/?rl-change=0&pe-moments=1,9,2&sy-coupling=4&al-frequency=14');
  const relief = page.locator('[data-model="relief-loop"]');
  await expect(relief.locator('#rl-change')).toHaveValue('0');
  await expect(relief.locator('[data-output="resolved"]')).toHaveAttribute('data-resolved', '0');
  await expect(page.locator('[data-model="peak-end"] [data-output="peak-end"]')).toHaveText('5.5');
  await expect(page.locator('#sy-coupling')).toHaveValue('4');
  await expect(page.locator('#al-frequency')).toHaveValue('14');
  await relief.locator('#rl-relief').fill('45');
  await expect(page).toHaveURL(/rl-relief=45/);
  await relief.getByRole('button', { name: /reset/i }).click();
  await expect(page).not.toHaveURL(/rl-relief|rl-change/);

  await open(page, 'methods/?sim-relief=2&sim-cause=1');
  await expect(page.locator('#sim-relief')).toHaveValue('2');
  await expect(page.locator('#sim-cause')).toBeChecked();
  await expect(page.locator('#simulation [data-output="phase"]')).toHaveAttribute('data-phase', 'peak');

  await open(page, 'search/?q=anger&search-section=advice');
  await expect(page.locator('[data-filter="advice"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('.search-result a[href*="/advice/"]').first()).toBeVisible();
  await expect(page.locator('.search-result a[href*="/research/"]')).toHaveCount(0);

  await open(page, 'evidence/');
  const first = page.locator('#claims .claim-card:has(.claim-toggle)').first();
  const id = String(await first.getAttribute('id'));
  await open(page, `evidence/#${id}`);
  await expect(page.locator(`#${id} .claim-sources`)).toBeVisible();
  expect(problems).toEqual([]);
});
