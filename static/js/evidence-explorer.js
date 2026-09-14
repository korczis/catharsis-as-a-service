/*
 * Evidence explorer (templates/evidence.html). Filters the claims ledger in place by text, claim type,
 * level of evidence and confidence. Every claim is already in the page: without JavaScript the full ledger
 * is listed and the filter bar is hidden. State mirrors into the query string (static/js/url-state.js),
 * so a filtered view can be shared. Nothing is stored or sent.
 */
(() => {
  'use strict';

  const PREFIX = 'ev';
  const DEFAULTS = { q: '', type: '', level: '', confidence: '' };

  const normalize = (text) =>
    String(text)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');

  // Pure: does one claim, described by its data attributes, match the filter state?
  const matches = (claim, state) => {
    if (state.type && claim.type !== state.type) return false;
    if (state.level && claim.level !== state.level) return false;
    if (state.confidence && claim.confidence !== state.confidence) return false;
    const query = normalize(state.q).trim();
    if (!query) return true;
    return query.split(/\s+/).every((word) => claim.text.includes(word));
  };

  window.caasEvidence = { matches, normalize };

  document.addEventListener('alpine:init', () => {
    window.Alpine.data('evidenceExplorer', () => ({
      ...DEFAULTS,
      shown: 0,
      total: 0,

      init() {
        this.claims = [...this.$root.querySelectorAll('[data-claim]')].map((el) => ({
          el,
          type: el.dataset.type,
          level: el.dataset.level,
          confidence: el.dataset.confidence,
          text: normalize(el.textContent),
        }));
        this.groups = [...this.$root.querySelectorAll('[data-claim-group]')];
        this.total = this.claims.length;

        const url = window.caasUrlState;
        if (url) Object.assign(this, url.read(PREFIX, DEFAULTS));
        this.$watch('q', () => this.apply());
        this.$watch('type', () => this.apply());
        this.$watch('level', () => this.apply());
        this.$watch('confidence', () => this.apply());
        this.apply();
      },

      get active() {
        return Object.keys(DEFAULTS).some((key) => this[key] !== DEFAULTS[key]);
      },

      apply() {
        const state = { q: this.q, type: this.type, level: this.level, confidence: this.confidence };
        let shown = 0;
        for (const claim of this.claims) {
          const visible = matches(claim, state);
          claim.el.hidden = !visible;
          if (visible) shown += 1;
        }
        for (const group of this.groups) {
          group.hidden = !group.querySelector('[data-claim]:not([hidden])');
        }
        this.shown = shown;
        if (window.caasUrlState) window.caasUrlState.write(PREFIX, state, DEFAULTS);
      },

      reset() {
        Object.assign(this, DEFAULTS);
      },
    }));
  });
})();
