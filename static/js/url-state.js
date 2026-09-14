/*
 * Bookmarkable interactive state. Components mirror their inputs into the query string as
 * `<prefix>-<key>` with history.replaceState and restore them on load, so a shared link reopens
 * the same view. Values equal to the defaults are omitted, keeping canonical URLs clean.
 * Loaded on every page before Alpine and the page scripts.
 */
(() => {
  'use strict';

  const serialize = (value) => {
    if (Array.isArray(value)) return value.join(',');
    if (typeof value === 'boolean') return value ? '1' : '0';
    return String(value);
  };

  const parse = (raw, fallback) => {
    if (Array.isArray(fallback)) {
      const list = raw.split(',').filter(Boolean).map(Number);
      return list.length && list.every(Number.isFinite) ? list : undefined;
    }
    if (typeof fallback === 'number') {
      const number = Number(raw);
      return raw !== '' && Number.isFinite(number) ? number : undefined;
    }
    if (typeof fallback === 'boolean') return raw === '1';
    return raw;
  };

  window.caasUrlState = {
    read(prefix, defaults) {
      const params = new URLSearchParams(window.location.search);
      const values = {};
      for (const [key, fallback] of Object.entries(defaults)) {
        const raw = params.get(`${prefix}-${key}`);
        if (raw === null) continue;
        const value = parse(raw, fallback);
        if (value !== undefined) values[key] = value;
      }
      return values;
    },

    write(prefix, state, defaults = {}) {
      const next = new URL(window.location.href);
      for (const [key, value] of Object.entries(state)) {
        const name = `${prefix}-${key}`;
        const serial = serialize(value);
        if (key in defaults && serialize(defaults[key]) === serial) next.searchParams.delete(name);
        else next.searchParams.set(name, serial);
      }
      if (next.href !== window.location.href) window.history.replaceState(window.history.state, '', next);
    },
  };

  /*
   * Switching language keeps the view: parameter names, claim ids and poster anchors are
   * language-neutral, so the current query string and hash carry over to the translated page.
   * Capture phase, so the href is rewritten before the link is followed.
   */
  document.addEventListener('click', (event) => {
    const link = event.target.closest && event.target.closest('a[data-locale-choice]');
    if (!link) return;
    const suffix = window.location.search + window.location.hash;
    if (suffix) link.href = link.href.split(/[?#]/)[0] + suffix;
  }, true);
})();
