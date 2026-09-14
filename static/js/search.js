/*
 * Library search (content/search). Loads api/v1/search.<lang>.json once and ranks entries in the
 * browser: title, then kicker and tags, then description, then body text. Matching ignores case and
 * diacritics and compares word stems, so Czech inflections (katarze, katarzi) find each other.
 * The query is mirrored into ?q= so results can be linked; nothing leaves the browser.
 */
(() => {
  'use strict';

  const MIN_TERM = 2;
  const STEM_FROM = 6;
  const STEM_TRIM = 2;
  const STEM_MIN = 5;
  const MAX_RESULTS = 50;
  const WEIGHTS = { title: 10, meta: 5, description: 3, text: 1 };

  const normalize = (value) =>
    String(value ?? '')
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .toLowerCase();

  const stem = (term) => (term.length >= STEM_FROM ? term.slice(0, Math.max(STEM_MIN, term.length - STEM_TRIM)) : term);

  document.addEventListener('alpine:init', () => {
    window.Alpine.data('siteSearch', () => ({
      query: '',
      section: 'all',
      entries: [],
      loaded: false,
      failed: false,

      async init() {
        this.query = new URLSearchParams(window.location.search).get('q') ?? '';
        const sections = Array.from(this.$el.querySelectorAll('[data-filter]'), (node) => node.dataset.filter);
        const state = window.caasUrlState;
        if (state) {
          const restored = state.read('search', { section: 'all' });
          if (!sections.includes(restored.section)) restored.section = 'all';
          Object.assign(this, restored);
          window.Alpine.effect(() => state.write('search', { section: this.section }, { section: 'all' }));
        }
        this.$watch('query', (value) => {
          const next = new URL(window.location.href);
          const trimmed = value.trim();
          if (trimmed) next.searchParams.set('q', trimmed);
          else next.searchParams.delete('q');
          window.history.replaceState(window.history.state, '', next);
        });
        try {
          const response = await fetch(this.$el.dataset.index);
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          const entries = await response.json();
          this.entries = entries.map((entry) => ({
            ...entry,
            hay: {
              title: normalize(entry.title),
              meta: normalize(`${entry.kicker} ${(entry.tags ?? []).join(' ')}`),
              description: normalize(entry.description),
              text: normalize(entry.text),
            },
          }));
          this.loaded = true;
        } catch (error) {
          this.failed = true;
        }
      },

      get terms() {
        return normalize(this.query)
          .split(/[^\p{L}\p{N}]+/u)
          .filter((term) => term.length >= MIN_TERM)
          .map(stem);
      },

      score(entry) {
        let total = 0;
        for (const term of this.terms) {
          let points = 0;
          for (const [field, weight] of Object.entries(WEIGHTS)) {
            if (entry.hay[field].includes(term)) points += weight;
          }
          if (!points) return 0;
          total += points;
        }
        return total;
      },

      get results() {
        if (!this.terms.length) return [];
        return this.entries
          .filter((entry) => this.section === 'all' || entry.section === this.section)
          .map((entry) => [this.score(entry), entry])
          .filter(([points]) => points > 0)
          .sort((a, b) => b[0] - a[0] || a[1].title.localeCompare(b[1].title))
          .slice(0, MAX_RESULTS)
          .map(([, entry]) => entry);
      },

      count(section) {
        if (!this.terms.length) return 0;
        return this.entries.filter((entry) => (section === 'all' || entry.section === section) && this.score(entry) > 0).length;
      },
    }));
  });
})();
