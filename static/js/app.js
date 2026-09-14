/*
 * Progressive enhancement for Catharsis as a Service.
 * Content never depends on this file. Ownership is split so no DOM state has two owners:
 *   Alpine.js — header state, diagnostic view switch, copy feedback
 *   Flowbite  — artwork viewer (Modal), mobile navigation (Drawer), tooltip
 *   vanilla   — locale choice persistence, reveal-on-scroll, pointer light
 */
(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const VIEWS = ['experience', 'diagnostic', 'raw'];
  const COPY_RESET_MS = 1800;
  const HEADER_REVEAL_OFFSET = 200;
  // Detector simulation thresholds (invented, documented on the methods page).
  const DETECTOR_HEART_RANGE = 40;
  const DETECTOR_EDA_RANGE = 12;
  const DETECTOR_LOW = 0.25;
  const DETECTOR_HIGH = 0.6;
  const DETECTOR_RELIEF = 6;
  const DETECTOR_SYNCHRONY = 50;

  const onReady = (fn) => {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  };

  const focusables = (root) =>
    [...root.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')];

  const trapFocus = (root, event) => {
    if (event.key !== 'Tab') return;
    const items = focusables(root);
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  document.addEventListener('alpine:init', () => {
    const { Alpine } = window;

    Alpine.data('navState', () => ({
      hidden: false,
      progress: 0,
      lastY: 0,
      frame: 0,

      init() {
        this.lastY = window.scrollY;
        this.measure();
        const schedule = () => {
          if (this.frame) return;
          this.frame = requestAnimationFrame(() => {
            this.frame = 0;
            this.measure();
          });
        };
        window.addEventListener('scroll', schedule, { passive: true });
        window.addEventListener('resize', schedule, { passive: true });
      },

      measure() {
        const y = window.scrollY;
        const max = document.documentElement.scrollHeight - window.innerHeight;
        this.progress = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
        if (y <= HEADER_REVEAL_OFFSET || y < this.lastY - 4) this.hidden = false;
        else if (y > this.lastY + 4) this.hidden = true;
        this.lastY = y;
      },
    }));

    Alpine.data('viewSwitch', () => ({
      view: VIEWS[0],

      onKey(event) {
        const index = VIEWS.indexOf(this.view);
        const moves = {
          ArrowRight: (index + 1) % VIEWS.length,
          ArrowLeft: (index + VIEWS.length - 1) % VIEWS.length,
          Home: 0,
          End: VIEWS.length - 1,
        };
        if (!(event.key in moves)) return;
        event.preventDefault();
        this.view = VIEWS[moves[event.key]];
        this.$nextTick(() => this.$refs[`tab-${this.view}`].focus());
      },
    }));

    Alpine.data('copyButton', () => ({
      state: 'idle',
      timer: 0,

      async copy() {
        const text = (this.$refs.source?.textContent ?? '').replace(/^\$ /gm, '').trim();
        try {
          await navigator.clipboard.writeText(text);
          this.state = 'copied';
        } catch (error) {
          this.state = 'failed';
        }
        clearTimeout(this.timer);
        this.timer = setTimeout(() => {
          this.state = 'idle';
        }, COPY_RESET_MS);
      },
    }));

    // Methods page: the detection model applied to invented inputs. The rules mirror the page text;
    // nothing is stored or sent, and no conclusion ever exceeds low confidence.
    Alpine.data('detector', () => ({
      config: { inputs: [] },
      values: {},
      cause: false,

      init() {
        this.config = JSON.parse(this.$el.dataset.config);
        this.reset();
      },

      reset() {
        this.values = Object.fromEntries(this.config.inputs.map((input) => [input.id, input.value]));
        this.cause = false;
      },

      get activationScore() {
        const clamp = (value) => Math.min(1, Math.max(0, value));
        const heart = clamp((this.values.heart_rate ?? 0) / DETECTOR_HEART_RANGE);
        const skin = clamp((this.values.eda ?? 0) / DETECTOR_EDA_RANGE);
        return (heart + skin) / 2;
      },

      get activation() {
        const score = this.activationScore;
        if (score < DETECTOR_LOW) return 'low';
        return score < DETECTOR_HIGH ? 'moderate' : 'high';
      },

      get relieved() {
        return (this.values.relief ?? 0) >= DETECTOR_RELIEF;
      },

      get phase() {
        const level = this.activation;
        if (level === 'low') return this.relieved ? 'recovery' : 'baseline';
        if (level === 'high') return this.relieved ? 'discharge' : 'peak';
        return this.relieved ? 'recovery' : 'activation';
      },

      get synchrony() {
        return (this.values.synchrony ?? 0) >= DETECTOR_SYNCHRONY ? 'high' : 'low';
      },

      get relief() {
        return this.relieved ? 'reported' : 'not_reported';
      },

      get causeState() {
        return this.cause ? 'reported' : 'unknown';
      },

      // Relief without any report that the cause changed is the artwork's case: problem_solved false.
      get problem() {
        return this.relieved && !this.cause ? 'false' : 'unknown';
      },
    }));
  });

  document.addEventListener('alpine:initialized', () => {
    window.__caasAlpineInits = (window.__caasAlpineInits || 0) + 1;
    document.documentElement.setAttribute('data-alpine', 'ready');
  });

  const initViewer = () => {
    const el = document.getElementById('artwork-viewer');
    if (!el || typeof window.Modal !== 'function') return;

    let trigger = null;
    const onKey = (event) => trapFocus(el, event);

    const modal = new window.Modal(
      el,
      {
        placement: 'center',
        backdrop: 'dynamic',
        backdropClasses: 'viewer-backdrop fixed inset-0 z-40',
        closable: true,
        onShow: () => {
          el.addEventListener('keydown', onKey);
          el.querySelector('[data-artwork-close]')?.focus();
        },
        onHide: () => {
          el.removeEventListener('keydown', onKey);
          trigger?.focus({ preventScroll: true });
        },
      },
      { id: 'artwork-viewer', override: true },
    );

    document.querySelectorAll('[data-artwork-open]').forEach((node) => {
      node.addEventListener('click', (event) => {
        event.preventDefault();
        trigger = node;
        modal.show();
      });
    });
    el.querySelectorAll('[data-artwork-close]').forEach((node) => {
      node.addEventListener('click', () => modal.hide());
    });
  };

  const initDrawer = () => {
    const el = document.getElementById('nav-drawer');
    const openers = document.querySelectorAll('[data-drawer-open]');
    if (!el || typeof window.Drawer !== 'function') return;

    let trigger = null;
    let drawer = null;
    const setExpanded = (value) => openers.forEach((node) => node.setAttribute('aria-expanded', value));
    const onKey = (event) => {
      if (event.key === 'Escape') drawer.hide();
      else trapFocus(el, event);
    };

    drawer = new window.Drawer(
      el,
      {
        placement: 'right',
        backdrop: true,
        bodyScrolling: false,
        backdropClasses: 'drawer-backdrop fixed inset-0 z-30',
        onShow: () => {
          el.inert = false;
          setExpanded('true');
          el.addEventListener('keydown', onKey);
          el.querySelector('[data-drawer-close]')?.focus();
        },
        onHide: () => {
          el.inert = true;
          setExpanded('false');
          el.removeEventListener('keydown', onKey);
          trigger?.focus({ preventScroll: true });
        },
      },
      { id: 'nav-drawer', override: true },
    );

    openers.forEach((node) => {
      node.addEventListener('click', () => {
        trigger = node;
        drawer.show();
      });
    });
    el.querySelectorAll('[data-drawer-close], a[href]').forEach((node) => {
      node.addEventListener('click', () => drawer.hide());
    });
  };

  const initLocaleChoice = () => {
    document.querySelectorAll('[data-locale-choice]').forEach((node) => {
      node.addEventListener('click', () => window.caasLocale?.set(node.getAttribute('data-locale-choice')));
    });
  };

  const initReveal = () => {
    const items = document.querySelectorAll('.reveal');
    const showAll = () => items.forEach((item) => item.classList.add('is-visible'));
    if (!items.length) return;
    if (reducedMotion.matches || !('IntersectionObserver' in window)) {
      showAll();
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.05 },
    );
    items.forEach((item) => observer.observe(item));
    window.addEventListener('beforeprint', showAll);
  };

  // Viewport coordinates only: the gradient uses background-attachment: fixed, so no layout reads.
  const initPointerLight = () => {
    const zone = document.querySelector('[data-pointer-light]');
    if (!zone || reducedMotion.matches || !finePointer.matches) return;
    let frame = 0;
    let x = 0;
    let y = 0;
    zone.addEventListener('pointermove', (event) => {
      if (event.pointerType !== 'mouse') return;
      x = event.clientX;
      y = event.clientY;
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        zone.style.setProperty('--px', `${x}px`);
        zone.style.setProperty('--py', `${y}px`);
        zone.classList.add('is-lit');
      });
    });
    zone.addEventListener('pointerleave', () => zone.classList.remove('is-lit'));
  };

  onReady(() => {
    initViewer();
    initDrawer();
    initLocaleChoice();
    initReveal();
    initPointerLight();
  });
})();
