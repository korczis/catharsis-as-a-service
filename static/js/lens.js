/*
 * The audience lens: one parameter, ?view=, that changes how much of the apparatus around a
 * statement is unfolded.
 *
 * Three rules this file keeps, and the reason for each.
 *
 * A lens never changes what is claimed. It adds and removes disclosure, never text that
 * contradicts another lens, so the markup for every lens is in the page before this script
 * runs and nothing is fetched or generated here.
 *
 * The page is correct before this script runs. The server renders the lens named by the
 * query string, so a reader without JavaScript, a crawler and a printed page all get a
 * complete document; this file only makes switching instant and keeps the address honest.
 *
 * Nothing is stored. The lens lives in the URL, which means it can be sent to somebody,
 * bookmarked and read back, and it means the choice leaves no trace on the reader's machine.
 */
(() => {
  'use strict';

  const PARAM = 'view';
  const root = document.documentElement;
  const lenses = (root.dataset.lenses || '').split(',').filter(Boolean);
  const fallback = root.dataset.lensDefault || lenses[0] || 'essential';

  const valid = (value) => lenses.includes(value);
  const fromUrl = () => {
    const value = new URLSearchParams(window.location.search).get(PARAM);
    return valid(value) ? value : fallback;
  };

  /* The whole switch: one attribute on <html>, which every lens-aware block is written
     against in CSS. No element is created, destroyed or rewritten, so assistive technology
     sees a document that gained or lost detail rather than one that was replaced. */
  const apply = (lens) => {
    root.setAttribute('data-lens', lens);
    document.querySelectorAll('[data-lens-option]').forEach((node) => {
      const selected = node.dataset.lensOption === lens;
      node.setAttribute('aria-current', selected ? 'true' : 'false');
    });
    document.querySelectorAll('[data-lens-announce]').forEach((node) => {
      node.textContent = node.dataset[`lensAnnounce${lens.charAt(0).toUpperCase()}${lens.slice(1)}`] || '';
    });
  };

  const write = (lens) => {
    const url = new URL(window.location.href);
    if (lens === fallback) url.searchParams.delete(PARAM);
    else url.searchParams.set(PARAM, lens);
    window.history.pushState({ lens }, '', `${url.pathname}${url.search}${url.hash}`);
  };

  const onReady = (fn) => {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn, { once: true });
    else fn();
  };

  onReady(() => {
    if (!lenses.length) return;
    apply(fromUrl());

    document.querySelectorAll('[data-lens-option]').forEach((node) => {
      node.addEventListener('click', (event) => {
        const lens = node.dataset.lensOption;
        if (!valid(lens) || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        write(lens);
        apply(lens);
      });
    });

    // Back and forward move between lenses, because a lens is part of the address.
    window.addEventListener('popstate', () => apply(fromUrl()));
  });
})();
