/*
 * Locale negotiation. Loaded synchronously in <head> so a redirect happens before first paint.
 * Priority: explicit locale URL > stored manual choice > navigator.languages > default.
 * Only the default-language home is a neutral entry point; every other URL is explicit and never redirects.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  var STORAGE_KEY = 'caas.locale';

  root.classList.remove('no-js');
  root.classList.add('js');

  function read() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (error) {
      return null;
    }
  }

  function write(value) {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch (error) {
      /* storage unavailable: the choice lasts for this navigation only */
    }
  }

  window.caasLocale = { key: STORAGE_KEY, get: read, set: write };

  if (root.getAttribute('data-neutral-entry') !== 'true') return;

  var supported = (root.getAttribute('data-locales') || '').split(',').filter(Boolean);
  var current = root.getAttribute('lang');
  var target = read();

  if (supported.indexOf(target) === -1) {
    target = null;
    var preferred = navigator.languages && navigator.languages.length
      ? navigator.languages
      : [navigator.language || ''];
    for (var i = 0; i < preferred.length && !target; i++) {
      var base = String(preferred[i]).toLowerCase().split('-')[0];
      if (supported.indexOf(base) !== -1) target = base;
    }
  }

  if (!target || target === current) return;

  var href = root.getAttribute('data-home-' + target);
  if (href) window.location.replace(href + window.location.hash);
})();
