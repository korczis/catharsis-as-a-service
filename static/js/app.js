/*
 * Progressive enhancement for Catharsis as a Service.
 * Content never depends on this file. Ownership is split so no DOM state has two owners:
 *   Alpine.js — header state, diagnostic view switch, copy feedback
 *   Flowbite  — artwork viewer and screen previews (Modal), mobile navigation (Drawer), tooltip
 *   vanilla   — locale choice persistence, reveal-on-scroll, pointer light
 */
(() => {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const VIEWS = ['experience', 'diagnostic', 'raw'];
  const COPY_RESET_MS = 1800;
  const HEADER_REVEAL_OFFSET = 200;
  const SWIPE_MIN_PX = 50;
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

  // Concept screen previews: one Modal per figure, moved to <body> so no transformed ancestor
  // (.reveal) can clip a fixed-position dialog. Modified clicks keep the link's own behaviour.
  const initScreens = () => {
    if (typeof window.Modal !== 'function') return;
    document.querySelectorAll('[data-screen-viewer]').forEach((el) => {
      const figure = document.getElementById(el.getAttribute('data-screen-viewer'));
      const triggers = figure ? [...figure.querySelectorAll('[data-screen-open]')] : [];
      if (!triggers.length) return;
      document.body.append(el);

      const image = el.querySelector('[data-screen-image]');
      const title = el.querySelector('[data-screen-title]');
      const caption = el.querySelector('[data-screen-caption]');
      const original = el.querySelector('[data-screen-original]');
      const count = el.querySelector('[data-screen-count]');
      const prev = el.querySelector('[data-screen-prev]');
      const next = el.querySelector('[data-screen-next]');
      const paged = triggers.length > 1;
      let index = 0;
      let trigger = null;

      // A single screen has nothing to page through; disabled also keeps the buttons out of the focus trap.
      [prev, next].forEach((node) => {
        node.hidden = !paged;
        node.disabled = !paged;
      });
      count.hidden = !paged;

      const show = (position) => {
        index = (position + triggers.length) % triggers.length;
        const node = triggers[index];
        image.src = node.dataset.full;
        image.width = Number(node.dataset.width);
        image.height = Number(node.dataset.height);
        image.alt = node.querySelector('img')?.alt ?? '';
        title.textContent = node.dataset.title;
        caption.textContent = node.dataset.caption;
        original.href = node.href;
        count.textContent = `${index + 1} / ${triggers.length}`;
        if (paged) [index + 1, index - 1].forEach(preload);
      };

      // Warm the neighbours so paging shows the next screen without waiting for the network.
      const preloaded = new Set();
      const preload = (position) => {
        const url = triggers[(position + triggers.length) % triggers.length].dataset.full;
        if (preloaded.has(url)) return;
        preloaded.add(url);
        const warm = new Image();
        warm.decoding = 'async';
        warm.src = url;
      };

      const PAGING_KEYS = {
        ArrowRight: () => index + 1,
        ArrowLeft: () => index - 1,
        Home: () => 0,
        End: () => triggers.length - 1,
      };
      const onKey = (event) => {
        if (paged && event.key in PAGING_KEYS) {
          event.preventDefault();
          show(PAGING_KEYS[event.key]());
        } else {
          trapFocus(el, event);
        }
      };

      // Touch and pen swipe on the image: a mostly horizontal stroke longer than SWIPE_MIN_PX pages.
      let stroke = null;
      image.addEventListener('pointerdown', (event) => {
        stroke = event.pointerType === 'mouse' ? null : { x: event.clientX, y: event.clientY };
      });
      image.addEventListener('pointercancel', () => {
        stroke = null;
      });
      image.addEventListener('pointerup', (event) => {
        if (!stroke || !paged) return;
        const dx = event.clientX - stroke.x;
        const dy = event.clientY - stroke.y;
        stroke = null;
        if (Math.abs(dx) < SWIPE_MIN_PX || Math.abs(dx) <= Math.abs(dy)) return;
        show(index + (dx < 0 ? 1 : -1));
      });

      const modal = new window.Modal(
        el,
        {
          placement: 'center',
          backdrop: 'dynamic',
          backdropClasses: 'viewer-backdrop fixed inset-0 z-40',
          closable: true,
          onShow: () => {
            el.addEventListener('keydown', onKey);
            el.querySelector('[data-screen-close]')?.focus();
          },
          onHide: () => {
            el.removeEventListener('keydown', onKey);
            trigger?.focus({ preventScroll: true });
          },
        },
        { id: el.id, override: true },
      );

      triggers.forEach((node, position) => {
        node.addEventListener('click', (event) => {
          if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
          event.preventDefault();
          trigger = node;
          show(position);
          modal.show();
        });
      });
      prev.addEventListener('click', () => show(index - 1));
      next.addEventListener('click', () => show(index + 1));
      el.querySelector('[data-screen-close]')?.addEventListener('click', () => modal.hide());
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
    initScreens();
    initDrawer();
    initLocaleChoice();
    initReveal();
    initPointerLight();
  });
})();
