/*
 * Interactive models (content/models). Five illustrative simulations rendered as SVG by Alpine.js.
 * Inputs are invented, outputs are computed in the browser, and nothing is stored or sent.
 * Loaded before Alpine on the models page only; every model is described in the page text.
 */
(() => {
  'use strict';

  const WIDTH = 600;
  const HEIGHT = 240;
  const PAD = 28;
  const SEED = 7;

  // Relief loop (negative reinforcement)
  const EPISODES = 30;
  const UNRESOLVED_DISTRESS = 70;
  const RESOLVED_DISTRESS = 20;
  const LEARNING_RATE = 0.15;
  const URGE_DECAY = 0.9;

  // Venting and arousal (illustrative time constants, minutes)
  const MINUTES = 30;
  const START_ANGER = 80;
  const REST_AROUSAL = 20;
  const EXTRA_AROUSAL = 50;
  const TAU = { waiting: 10, calming: 5, venting: 11 };
  const AROUSAL_TAU = { waiting: 12, calming: 5, venting: 12 };
  const VENTING_BUMP = 35;
  const VENTING_BUMP_PEAK = 3;

  // Peak–end
  const PEAK_END_DEFAULT = [2, 4, 6, 8, 7, 5, 4, 6];
  const MILD_ENDING = 3;
  const MIN_MOMENTS = 2;
  const MAX_MOMENTS = 12;

  // Kuramoto synchrony
  const MAX_OSCILLATORS = 40;
  const ORBIT = 100;
  const DT = 0.05;
  const STEPS_PER_FRAME = 2;
  const HISTORY = 160;

  // Allostatic load
  const DAYS = 84;
  const LOAD_PER_STRESSOR = 10;

  // Reduced-motion fallback for the synchrony animation: coarse steps at a slow rate.
  const REDUCED_STEPS = 40;
  const REDUCED_INTERVAL = 1000;

  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const round = (value, digits = 0) => Number(value.toFixed(digits));

  // mulberry32: a small deterministic generator so every reader sees the same run for the same inputs.
  const random = (seed) => {
    let state = seed >>> 0;
    return () => {
      state = (state + 0x6d2b79f5) >>> 0;
      let t = state;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };

  const x = (index, count) => PAD + (index * (WIDTH - 2 * PAD)) / Math.max(1, count - 1);
  const y = (value, max) => HEIGHT - PAD - (clamp(value, 0, max) / max) * (HEIGHT - 2 * PAD);
  const line = (values, max) =>
    values.map((value, index) => `${index ? 'L' : 'M'}${x(index, values.length).toFixed(1)},${y(value, max).toFixed(1)}`).join(' ');

  const labelsOf = (el) => JSON.parse(el.dataset.labels || '{}');

  // Mirror a component's inputs into the query string (static/js/url-state.js) and restore them on load.
  const bookmark = (component, prefix, defaults) => {
    const state = window.caasUrlState;
    if (!state) return;
    Object.assign(component, state.read(prefix, defaults));
    window.Alpine.effect(() => {
      const current = Object.fromEntries(Object.keys(defaults).map((key) => [key, component[key]]));
      state.write(prefix, current, defaults);
    });
  };

  document.addEventListener('alpine:init', () => {
    const { Alpine } = window;

    Alpine.data('reliefLoop', () => ({
      labels: {},
      relief: 30,
      change: 5,

      init() {
        this.labels = labelsOf(this.$el);
        bookmark(this, 'rl', { relief: 30, change: 5 });
        this.relief = clamp(Number(this.relief), 0, 60);
        this.change = clamp(Number(this.change), 0, 30);
      },

      reset() {
        this.relief = 30;
        this.change = 5;
      },

      get run() {
        const next = random(SEED);
        const before = [];
        const after = [];
        const urge = [];
        let habit = 0;
        let resolvedAt = 0;
        for (let episode = 0; episode < EPISODES; episode += 1) {
          const baseline = resolvedAt ? RESOLVED_DISTRESS : UNRESOLVED_DISTRESS;
          const relief = Math.min(this.relief, baseline);
          before.push(baseline);
          after.push(baseline - relief);
          habit = resolvedAt ? habit * URGE_DECAY : habit + LEARNING_RATE * (relief / 100) * (1 - habit);
          urge.push(habit * 100);
          if (!resolvedAt && next() < this.change / 100) resolvedAt = episode + 1;
        }
        return { before, after, urge, resolvedAt };
      },

      get paths() {
        const { before, after, urge } = this.run;
        return { before: line(before, 100), after: line(after, 100), urge: line(urge, 100) };
      },

      get resolvedAt() {
        return this.run.resolvedAt;
      },

      get marker() {
        return this.resolvedAt ? x(this.resolvedAt - 1, EPISODES) : -10;
      },

      get resolvedText() {
        return this.resolvedAt ? `${this.labels.resolved} ${this.resolvedAt}` : this.labels.never;
      },

      get peakUrge() {
        return round(Math.max(...this.run.urge));
      },
    }));

    Alpine.data('ventingArousal', () => ({
      labels: {},
      activity: 'venting',

      init() {
        this.labels = labelsOf(this.$el);
        bookmark(this, 'va', { activity: 'venting' });
        if (!(this.activity in TAU)) this.activity = 'venting';
      },

      series(activity) {
        const anger = [];
        const arousal = [];
        for (let minute = 0; minute <= MINUTES; minute += 1) {
          anger.push(START_ANGER * Math.exp(-minute / TAU[activity]));
          let level = REST_AROUSAL + EXTRA_AROUSAL * Math.exp(-minute / AROUSAL_TAU[activity]);
          if (activity === 'venting') {
            level += VENTING_BUMP * (minute / VENTING_BUMP_PEAK) * Math.exp(1 - minute / VENTING_BUMP_PEAK);
          }
          arousal.push(level);
        }
        return { anger, arousal };
      },

      get paths() {
        const selected = this.series(this.activity);
        return {
          anger: line(selected.anger, 100),
          arousal: line(selected.arousal, 100),
          waiting: line(this.series('waiting').anger, 100),
          calming: line(this.series('calming').anger, 100),
          venting: line(this.series('venting').anger, 100),
        };
      },

      get atTen() {
        return round(this.series(this.activity).anger[10]);
      },
    }));

    Alpine.data('peakEnd', () => ({
      labels: {},
      moments: [...PEAK_END_DEFAULT],

      init() {
        this.labels = labelsOf(this.$el);
        bookmark(this, 'pe', { moments: [...PEAK_END_DEFAULT] });
        this.moments = this.moments.slice(0, MAX_MOMENTS).map((value) => clamp(value, 0, 10));
        if (this.moments.length < MIN_MOMENTS) this.moments = [...PEAK_END_DEFAULT];
      },

      reset() {
        this.moments = [...PEAK_END_DEFAULT];
      },

      add() {
        if (this.moments.length < MAX_MOMENTS) this.moments.push(MILD_ENDING);
      },

      remove() {
        if (this.moments.length > MIN_MOMENTS) this.moments.pop();
      },

      get average() {
        return round(this.moments.reduce((sum, value) => sum + value, 0) / this.moments.length, 1);
      },

      get peakEnd() {
        return round((Math.max(...this.moments) + this.moments[this.moments.length - 1]) / 2, 1);
      },

      get total() {
        return this.moments.reduce((sum, value) => sum + value, 0);
      },

      bar(index) {
        const slot = (WIDTH - 2 * PAD) / MAX_MOMENTS;
        const value = this.moments[index] ?? 0;
        const top = y(value, 10);
        return { x: PAD + index * slot + slot * 0.15, width: slot * 0.7, y: top, height: HEIGHT - PAD - top };
      },

      level(value) {
        return y(value, 10);
      },
    }));

    Alpine.data('synchrony', () => ({
      labels: {},
      coupling: 1.5,
      count: 20,
      spread: 0.5,
      playing: false,
      phases: [],
      tempos: [],
      order: 0,
      angle: 0,
      history: [],
      frame: 0,
      timer: 0,
      announcement: '',

      init() {
        this.labels = labelsOf(this.$el);
        bookmark(this, 'sy', { coupling: 1.5, count: 20, spread: 0.5 });
        this.coupling = clamp(Number(this.coupling), 0, 4);
        this.count = clamp(Number(this.count), 4, MAX_OSCILLATORS);
        this.spread = clamp(Number(this.spread), 0, 1);
        this.seed();
        this.$watch('count', () => this.seed());
        this.$watch('spread', () => this.seed());
      },

      destroy() {
        this.pause();
      },

      seed() {
        const next = random(SEED);
        const count = clamp(Number(this.count), 2, MAX_OSCILLATORS);
        this.phases = Array.from({ length: count }, () => next() * 2 * Math.PI);
        // Natural tempos spread evenly around 1 rad/s, so the same inputs always give the same run.
        this.tempos = Array.from({ length: count }, (_, index) => 1 + Number(this.spread) * ((2 * index) / Math.max(1, count - 1) - 1));
        this.history = [];
        this.measure();
      },

      reset() {
        this.coupling = 1.5;
        this.count = 20;
        this.spread = 0.5;
        this.pause();
        this.seed();
        this.announce();
      },

      measure() {
        const n = this.phases.length;
        const re = this.phases.reduce((sum, phase) => sum + Math.cos(phase), 0) / n;
        const im = this.phases.reduce((sum, phase) => sum + Math.sin(phase), 0) / n;
        this.order = Math.hypot(re, im);
        this.angle = Math.atan2(im, re);
      },

      // Mean-field form of the Kuramoto model: dθi/dt = ωi + K·r·sin(ψ − θi).
      step(times = 1) {
        for (let t = 0; t < times; t += 1) {
          this.measure();
          const k = Number(this.coupling);
          this.phases = this.phases.map((phase, index) => phase + DT * (this.tempos[index] + k * this.order * Math.sin(this.angle - phase)));
        }
        this.measure();
        this.history = [...this.history, this.order].slice(-HISTORY);
      },

      play() {
        this.playing = true;
        // Reduced motion: advance in coarse jumps once a second instead of on every frame.
        if (prefersReducedMotion()) {
          this.timer = setInterval(() => this.step(REDUCED_STEPS), REDUCED_INTERVAL);
          return;
        }
        const tick = () => {
          if (!this.playing) return;
          this.step(STEPS_PER_FRAME);
          this.frame = requestAnimationFrame(tick);
        };
        this.frame = requestAnimationFrame(tick);
      },

      pause() {
        this.playing = false;
        cancelAnimationFrame(this.frame);
        clearInterval(this.timer);
        this.timer = 0;
        this.announce();
      },

      // The live order readout changes every frame, so announce it only when the run stops or steps.
      announce() {
        this.announcement = `${this.labels.order || ''} ${this.orderText}`.trim();
      },

      toggle() {
        if (this.playing) this.pause();
        else this.play();
      },

      dot(index) {
        const phase = this.phases[index];
        if (phase === undefined) return { x: 0, y: 0, visible: false };
        return { x: ORBIT * Math.cos(phase), y: ORBIT * Math.sin(phase), visible: true };
      },

      get vector() {
        return { x: ORBIT * this.order * Math.cos(this.angle), y: ORBIT * this.order * Math.sin(this.angle) };
      },

      get orderText() {
        return this.order.toFixed(2);
      },

      get historyPath() {
        const values = this.history.length > 1 ? this.history : [this.order, this.order];
        return line(values.map((value) => value * 100), 100);
      },
    }));

    Alpine.data('allostaticLoad', () => ({
      labels: {},
      frequency: 5,
      recovery: 10,

      init() {
        this.labels = labelsOf(this.$el);
        bookmark(this, 'al', { frequency: 5, recovery: 10 });
        this.frequency = clamp(Number(this.frequency), 0, 14);
        this.recovery = clamp(Number(this.recovery), 1, 30);
      },

      get series() {
        const values = [];
        let load = 0;
        const daily = (LOAD_PER_STRESSOR * Number(this.frequency)) / 7;
        for (let day = 0; day < DAYS; day += 1) {
          load = load * (1 - Number(this.recovery) / 100) + daily;
          values.push(load);
        }
        return values;
      },

      get max() {
        return Math.max(100, ...this.series);
      },

      get path() {
        return line(this.series, this.max);
      },

      get peak() {
        return round(Math.max(...this.series));
      },
    }));
  });
})();
