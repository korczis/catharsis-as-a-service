// @ts-check
// Case study (/case-study/, /cs/pripadova-studie/): build-time records, the interactive timeline and
// lifecycle, bookmarkable state and the no-JavaScript fallback. Runs against the local subpath preview or,
// with BASE_URL, production.
const { test, expect } = require('@playwright/test');

const BASE = new URL(process.env.BASE_URL || 'http://127.0.0.1:4173/catharsis-as-a-service/');
const PAGES = [
  { code: 'en', path: 'case-study/', screensLabel: /illustrative data/i },
  { code: 'cs', path: 'cs/pripadova-studie/', screensLabel: /ilustrativní data/i },
];
const [EN] = PAGES;
const METRICS = ['tasks', 'checkpoints', 'handovers', 'decisions', 'findings', 'commits', 'pipelines', 'releases'];

const url = (relative) => new URL(relative, BASE).href;

function watch(page) {
  const problems = [];
  page.on('console', (message) => {
    if (message.type() === 'error') problems.push(`console: ${message.text()}`);
  });
  page.on('pageerror', (error) => problems.push(`pageerror: ${error.message}`));
  page.on('response', (response) => {
    if (response.url().startsWith(BASE.origin) && response.status() >= 400) {
      problems.push(`http ${response.status()}: ${response.url()}`);
    }
  });
  return problems;
}

async function open(page, relative) {
  const response = await page.goto(url(relative), { waitUntil: 'load' });
  await expect(page.locator('html')).toHaveAttribute('data-alpine', 'ready');
  return response;
}

const overflow = (page) =>
  page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

const events = (page) => page.locator('[data-event]');
const visibleEvents = (page) => page.locator('[data-event]:visible');
const params = (page) => new URL(page.url()).searchParams;

for (const locale of PAGES) {
  test(`case study ${locale.code}: renders cleanly at 390 px with records and labelled concept screens`, async ({ page }) => {
    const problems = watch(page);
    await page.setViewportSize({ width: 390, height: 844 });
    const response = await open(page, locale.path);

    expect(response?.status()).toBe(200);
    await expect(page.locator('html')).toHaveAttribute('lang', locale.code);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('[data-case-badge]')).toBeVisible();
    expect(await overflow(page)).toBeLessThanOrEqual(0);

    for (const name of METRICS) {
      const value = Number.parseInt(String(await page.locator(`[data-metric="${name}"] dd`).textContent()), 10);
      expect(value, name).toBeGreaterThan(0);
    }
    expect(Number(await page.locator('[data-metric="first-release"]').getAttribute('data-seconds'))).toBeGreaterThan(0);

    // Metrics and the timeline come from the same snapshot.
    const findings = Number.parseInt(String(await page.locator('[data-metric="findings"] dd').textContent()), 10);
    await expect(page.locator('[data-event][data-kind="finding"]')).toHaveCount(findings);
    await expect(page.locator('[data-finding]')).toHaveCount(findings);
    const commits = Number.parseInt(String(await page.locator('[data-metric="commits"] dd').textContent()), 10);
    await expect(page.locator('[data-event][data-kind="commit"]')).toHaveCount(commits);

    const screens = page.locator('figure.case-screens');
    await expect(screens.locator('.screen-label')).toHaveText(locale.screensLabel);
    expect(await screens.locator('img').count()).toBeGreaterThan(1);
    await expect(page.locator('figure.screens')).toHaveCount(0);

    const engineering = page.locator('[data-engineering-link]');
    await expect(engineering).toHaveCount(2);
    expect(await engineering.nth(0).getAttribute('href')).toBe('../engineering/');
    expect(await engineering.nth(1).getAttribute('href')).toBe('../engineering/time-accounting/');

    expect(await overflow(page)).toBeLessThanOrEqual(0);
    expect(problems).toEqual([]);
  });

  test(`case study ${locale.code}: links to registered Majordomus commands resolve to existing anchors`, async ({ page, request }) => {
    await open(page, locale.path);
    const hrefs = await page.evaluate(() => [
      ...new Set(
        [...document.querySelectorAll('a[href*="commands/#majordomus-"]')].map((link) => /** @type {HTMLAnchorElement} */ (link).href),
      ),
    ]);
    expect(hrefs.length).toBeGreaterThan(5);
    const bodies = new Map();
    for (const href of hrefs) {
      const [document, anchor] = href.split('#');
      if (!bodies.has(document)) {
        const response = await request.get(document);
        expect(response.status(), document).toBe(200);
        bodies.set(document, await response.text());
      }
      expect(bodies.get(document), `${href} has no anchor`).toMatch(new RegExp(`id="?${anchor}"?[\\s>]`));
    }
  });
}

test('case study timeline: kind chips and text search filter the list and are mirrored in the URL', async ({ page }) => {
  const problems = watch(page);
  await open(page, EN.path);
  const total = await events(page).count();
  expect(total).toBeGreaterThan(10);
  await expect(visibleEvents(page)).toHaveCount(total);

  const decisionChip = page.locator('[data-kind-chip="decision"]');
  const decisions = Number.parseInt(String(await decisionChip.locator('span').textContent()), 10);
  await decisionChip.click();
  await expect(decisionChip).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-kind-chip="all"]')).toHaveAttribute('aria-pressed', 'false');
  await expect(visibleEvents(page)).toHaveCount(decisions);
  expect(decisions).toBeLessThan(total);
  for (const kind of await visibleEvents(page).evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-kind')))) {
    expect(kind).toBe('decision');
  }
  await expect(page.locator('[data-timeline-shown]')).toHaveText(String(decisions));
  await expect.poll(() => params(page).get('tl-kind')).toBe('decision');

  await page.locator('[data-kind-chip="finding"]').click();
  await expect.poll(() => params(page).get('tl-kind')).toBe('decision,finding');

  await page.locator('[data-timeline-query]').fill('scope');
  await expect.poll(() => params(page).get('tl-q')).toBe('scope');
  const matching = await visibleEvents(page).count();
  expect(matching).toBeGreaterThan(0);
  for (const item of await visibleEvents(page).evaluateAll((nodes) =>
    nodes.map((node) => ({ kind: node.getAttribute('data-kind'), search: node.getAttribute('data-search') })),
  )) {
    expect(['decision', 'finding']).toContain(item.kind);
    expect(String(item.search)).toContain('scope');
  }

  await page.locator('[data-timeline-query]').fill('no event is called this');
  await expect(visibleEvents(page)).toHaveCount(0);
  await expect(page.locator('.case-empty')).toBeVisible();

  await page.locator('[data-timeline-reset]').click();
  await expect(visibleEvents(page)).toHaveCount(total);
  await expect.poll(() => [...params(page).keys()].filter((key) => key.startsWith('tl-'))).toEqual([]);
  expect(page.url()).toBe(url(EN.path));
  expect(problems).toEqual([]);
});

test('case study timeline: a bookmarked filter URL restores the view, and canonical stays clean', async ({ page }) => {
  const problems = watch(page);
  await open(page, `${EN.path}?tl-kind=decision,finding&tl-q=scope`);
  await expect(page.locator('[data-kind-chip="decision"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-kind-chip="finding"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-kind-chip="commit"]')).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('[data-timeline-query]')).toHaveValue('scope');
  const shown = await visibleEvents(page).count();
  expect(shown).toBeGreaterThan(0);
  expect(shown).toBeLessThan(await events(page).count());
  for (const kind of await visibleEvents(page).evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-kind')))) {
    expect(['decision', 'finding']).toContain(kind);
  }
  expect(await page.locator('link[rel="canonical"]').getAttribute('href')).toBe(url(EN.path));
  expect(await page.locator('meta[property="og:url"]').getAttribute('content')).toBe(url(EN.path));
  expect(problems).toEqual([]);
});

test('case study timeline: expanding an event shows its links and sets a bookmarkable hash', async ({ page, browser }) => {
  const problems = watch(page);
  await open(page, EN.path);
  const item = page.locator('[data-event][data-kind="finding"]').first();
  const id = String(await item.getAttribute('id'));
  await item.locator('summary').click();
  await expect(item.locator('details')).toHaveAttribute('open', '');
  const links = item.locator('[data-event-link]');
  expect(await links.count()).toBeGreaterThan(0);
  await expect(links.first()).toBeVisible();
  expect(String(await links.first().getAttribute('href'))).toMatch(/^https:\/\//);
  await expect.poll(() => new URL(page.url()).hash).toBe(`#${id}`);

  // A bookmarked event opens and is scrolled into view, even when the bookmarked filters would hide it.
  const context = await browser.newContext();
  const bookmarked = await context.newPage();
  await open(bookmarked, `${EN.path}?tl-kind=commit#event-finding-malformed-scope`);
  const target = bookmarked.locator('#event-finding-malformed-scope');
  await expect(target).toBeVisible();
  await expect(target.locator('details')).toHaveAttribute('open', '');
  await expect(target).toBeInViewport();
  await context.close();
  expect(problems).toEqual([]);
});

test('case study lifecycle: selecting a step updates the detail panel and the hash; a bookmarked step is restored', async ({ page, browser }) => {
  const problems = watch(page);
  await open(page, EN.path);
  const panels = page.locator('[data-step]');
  const count = await panels.count();
  expect(count).toBeGreaterThan(4);
  await expect(page.locator('[data-step]:visible')).toHaveCount(1);
  await expect(page.locator('#step-start')).toBeVisible();

  await page.locator('[data-step-link="finish"]').click();
  await expect(page.locator('#step-finish')).toBeVisible();
  await expect(page.locator('#step-start')).toBeHidden();
  await expect(page.locator('[data-step]:visible')).toHaveCount(1);
  await expect(page.locator('[data-step-link="finish"]')).toHaveAttribute('aria-current', 'step');
  await expect(page.locator('[data-step-link="start"]')).toHaveAttribute('aria-current', 'false');
  await expect.poll(() => new URL(page.url()).hash).toBe('#step-finish');
  const command = page.locator('#step-finish [data-command-link]');
  expect(String(await command.getAttribute('href'))).toMatch(/commands\/#majordomus-finish$/);
  const example = page.locator('#step-finish [data-step-example] a');
  const exampleHref = String(await example.getAttribute('href'));
  expect(exampleHref).toMatch(/^#event-/);
  await expect(page.locator(exampleHref)).toHaveCount(1);

  const context = await browser.newContext();
  const bookmarked = await context.newPage();
  await open(bookmarked, `${EN.path}#step-handover`);
  await expect(bookmarked.locator('#step-handover')).toBeVisible();
  await expect(bookmarked.locator('#step-start')).toBeHidden();
  await expect(bookmarked.locator('[data-step-link="handover"]')).toHaveAttribute('aria-current', 'step');
  await context.close();
  expect(problems).toEqual([]);
});

test('case study without JavaScript: every event and step is listed with its anchor, filters stay hidden', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, locale: 'en-US' });
  const page = await context.newPage();
  await page.goto(url(EN.path));
  await expect(page.locator('h1')).toHaveCount(1);
  const total = await events(page).count();
  expect(total).toBeGreaterThan(10);
  expect(total).toBe(Number(await page.locator('[data-timeline-total]').textContent()));
  await expect(visibleEvents(page)).toHaveCount(total);
  for (const id of await events(page).evaluateAll((nodes) => nodes.map((node) => node.id))) {
    expect(id).toMatch(/^event-[a-z0-9.-]+$/);
  }
  await expect(page.locator('.case-filters')).toBeHidden();
  const steps = await page.locator('[data-step]').count();
  await expect(page.locator('[data-step]:visible')).toHaveCount(steps);
  for (const href of await page.locator('[data-step-link]').evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href')))) {
    await expect(page.locator(String(href))).toHaveCount(1);
  }
  await page.goto(url(`${EN.path}#event-release-v0-1-0`));
  await expect(page.locator('#event-release-v0-1-0')).toBeVisible();
  await context.close();
});
