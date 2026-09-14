/*
 * Case study (content/case-study): the recorded timeline and the task lifecycle diagram.
 * The server renders every event and every step with a stable anchor; this script filters, expands
 * and selects, and mirrors that state into the URL (query `tl-kind`, `tl-q`; hash `event-<id>` or
 * `step-<id>`) so a bookmarked link reopens the same view. Loaded before Alpine on this page only.
 */
(() => {
  'use strict';

  const PREFIX = 'tl';
  const DEFAULTS = { kind: '', q: '' };

  // The contract of static/js/url-state.js, used only when a build does not load the shared helper.
  const localUrlState = {
    read(prefix, defaults) {
      const params = new URLSearchParams(window.location.search);
      const values = {};
      for (const key of Object.keys(defaults)) {
        const raw = params.get(`${prefix}-${key}`);
        if (raw !== null) values[key] = raw;
      }
      return values;
    },
    write(prefix, state, defaults = {}) {
      const next = new URL(window.location.href);
      for (const [key, value] of Object.entries(state)) {
        const name = `${prefix}-${key}`;
        if (key in defaults && String(defaults[key]) === String(value)) next.searchParams.delete(name);
        else next.searchParams.set(name, String(value));
      }
      if (next.href !== window.location.href) window.history.replaceState(window.history.state, '', next);
    },
  };
  const urlState = () => window.caasUrlState || localUrlState;

  // Case- and diacritic-insensitive matching, so "rozsah" and "Rozsah" find the same events.
  const fold = (text) =>
    String(text || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();

  const currentHash = () => decodeURIComponent(window.location.hash.slice(1));

  const setHash = (id) => {
    const next = new URL(window.location.href);
    next.hash = id ? `#${id}` : '';
    if (next.href !== window.location.href) window.history.replaceState(window.history.state, '', next);
  };

  document.addEventListener('alpine:init', () => {
    const { Alpine } = window;

    Alpine.data('caseTimeline', () => {
      // DOM nodes stay outside Alpine's reactive state.
      let items = [];

      return {
        kinds: [],
        query: '',
        shown: 0,
        total: 0,

        init() {
          items = [...this.$el.querySelectorAll('[data-event]')];
          this.total = items.length;
          const known = new Set(items.map((item) => item.dataset.kind));
          const saved = urlState().read(PREFIX, DEFAULTS);
          this.kinds = String(saved.kind ?? '')
            .split(',')
            .filter((kind) => known.has(kind));
          this.query = String(saved.q ?? '');
          this.apply();
          this.$watch('kinds', () => this.update());
          this.$watch('query', () => this.update());

          for (const item of items) {
            const details = item.querySelector('details');
            details?.addEventListener('toggle', () => {
              if (details.open) setHash(item.id);
              else if (currentHash() === item.id) setHash('');
            });
          }
          this.reveal(currentHash());
          window.addEventListener('hashchange', () => this.reveal(currentHash()));
        },

        isKind(kind) {
          return this.kinds.includes(kind);
        },

        toggle(kind) {
          this.kinds = this.isKind(kind) ? this.kinds.filter((item) => item !== kind) : [...this.kinds, kind];
        },

        reset() {
          this.kinds = [];
          this.query = '';
        },

        update() {
          this.apply();
          urlState().write(PREFIX, { kind: this.kinds.join(','), q: this.query.trim() }, DEFAULTS);
        },

        apply() {
          const needle = fold(this.query);
          let shown = 0;
          for (const item of items) {
            const kindMatches = !this.kinds.length || this.kinds.includes(item.dataset.kind);
            const textMatches = !needle || fold(item.dataset.search).includes(needle);
            item.hidden = !(kindMatches && textMatches);
            if (!item.hidden) shown += 1;
          }
          this.shown = shown;
        },

        // A bookmarked or clicked #event-<id> opens that event, clearing filters that would hide it.
        reveal(id) {
          if (!id.startsWith('event-')) return;
          const item = items.find((candidate) => candidate.id === id);
          if (!item) return;
          if (item.hidden) {
            this.reset();
            this.apply();
          }
          const details = item.querySelector('details');
          if (details) details.open = true;
          item.scrollIntoView({ block: 'start' });
        },
      };
    });

    Alpine.data('caseLifecycle', () => {
      let steps = [];

      return {
        active: '',

        init() {
          steps = [...this.$el.querySelectorAll('[data-step]')].map((el) => el.dataset.step);
          const fromHash = this.stepFromHash();
          this.active = fromHash || steps[0] || '';
          if (fromHash) {
            this.$nextTick(() => document.getElementById(`step-${fromHash}`)?.scrollIntoView({ block: 'start' }));
          }
          window.addEventListener('hashchange', () => {
            const step = this.stepFromHash();
            if (step) this.active = step;
          });
        },

        stepFromHash() {
          const hash = currentHash();
          const step = hash.startsWith('step-') ? hash.slice('step-'.length) : '';
          return steps.includes(step) ? step : '';
        },

        isActive(step) {
          return this.active === step;
        },

        select(step) {
          this.active = step;
          setHash(`step-${step}`);
        },
      };
    });
  });
})();
