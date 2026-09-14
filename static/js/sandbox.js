/*
 * Detection sandbox: what a set of signals does and does not settle.
 *
 * The point of this file is not to infer an emotion. It is to show that the same signals
 * support several readings at once, that the reading changes with the context while the
 * signals do not, and that the things a person most wants to know — what this means to
 * whoever is being watched, and whether anything was resolved — are not in the signals at
 * all. Every number here is illustrative: the weights were chosen to make the structure of
 * the inference visible, not fitted to any dataset, and nothing is recorded or sent.
 *
 * The computation is pure and deterministic and lives on window.caasSandbox so the tests can
 * call it without a DOM: derive(signals) and hypotheses(derived, context) are functions of
 * their arguments alone. The Alpine component below only holds state and asks them.
 */
(() => {
  'use strict';

  const clamp = (value, low, high) => Math.min(high, Math.max(low, value));
  const round = (value, places = 0) => Number(value.toFixed(places));

  /* The inputs a reader sets, with the range each is read on. Heart rate is beats per
     minute; the rest are unitless 0–100 scales, because an invented scale that pretends to
     be a unit is worse than one that admits it. */
  const SIGNALS = {
    heart: { min: 50, max: 190, step: 1, fallback: 120 },
    movement: { min: 0, max: 100, step: 1, fallback: 60 },
    vocal: { min: 0, max: 100, step: 1, fallback: 45 },
    alignment: { min: 0, max: 100, step: 1, fallback: 70 },
    reported: { min: 0, max: 100, step: 1, fallback: 65 },
  };

  /* Illustrative priors: how common each reading is taken to be in each setting, before any
     signal is looked at. They are the part of the inference that comes from knowing where
     you are rather than from the sensors, which is exactly what the sandbox is for. */
  const CONTEXTS = {
    concert: { collective: 0.3, positive: 0.35, exertion: 0.15, anger: 0.1, fear: 0.1 },
    protest: { collective: 0.3, positive: 0.15, exertion: 0.05, anger: 0.35, fear: 0.15 },
    sport: { collective: 0.3, positive: 0.25, exertion: 0.2, anger: 0.2, fear: 0.05 },
    emergency: { collective: 0.2, positive: 0.05, exertion: 0.05, anger: 0.2, fear: 0.5 },
    ritual: { collective: 0.35, positive: 0.3, exertion: 0.2, anger: 0.05, fear: 0.1 },
  };

  /* Illustrative likelihoods: how well each reading fits the derived features. Each returns
     0–1 and is written as one legible expression, so a reader can see what drives it. */
  const FIT = {
    collective: (d) => (d.arousal / 100) * (d.synchrony / 100),
    positive: (d) => (d.synchrony / 100) * (1 - d.gap / 100) * (0.4 + (0.6 * d.voice) / 100),
    anger: (d) => (d.arousal / 100) * (d.voice / 100) * (1 - d.synchrony / 100),
    fear: (d) => (d.arousal / 100) * (1 - d.synchrony / 100) * (1 - d.voice / 100),
    exertion: (d) => (d.effort / 100) * (1 - d.voice / 100),
  };

  /* Derived from the signals by stated rules, adding no knowledge: every value below is a
     restatement of the inputs, and each one says which inputs it restates. */
  const derive = (signals) => {
    const s = {};
    for (const [key, spec] of Object.entries(SIGNALS)) {
      const value = Number(signals?.[key]);
      s[key] = clamp(Number.isFinite(value) ? value : spec.fallback, spec.min, spec.max);
    }
    // heart rate on its own 50–190 scale, mapped to 0–100 so it can be averaged with the rest
    const heartScaled = ((s.heart - SIGNALS.heart.min) / (SIGNALS.heart.max - SIGNALS.heart.min)) * 100;
    const arousal = (heartScaled + s.movement + s.vocal) / 3;
    return {
      arousal: round(arousal, 1),
      synchrony: round(s.alignment, 1),
      effort: round((heartScaled + s.movement) / 2, 1),
      voice: round(s.vocal, 1),
      // how far the body and the person's own account disagree: large means the two
      // channels are telling different stories, which is information about the measurement
      // rather than about the person
      gap: round(Math.abs(arousal - s.reported), 1),
      signals: s,
      heartScaled: round(heartScaled, 1),
    };
  };

  /* The readings, ranked. Posterior ∝ prior × fit, normalised, with every term kept so the
     page can show the arithmetic rather than only its result. A reading is never returned
     alone: the list is the answer, and its spread is the point. */
  const hypotheses = (derived, context) => {
    const priors = CONTEXTS[context] || CONTEXTS.concert;
    const scored = Object.keys(FIT).map((id) => {
      const prior = priors[id] ?? 0;
      const fit = clamp(FIT[id](derived), 0, 1);
      return { id, prior, fit, weight: prior * fit };
    });
    const total = scored.reduce((sum, h) => sum + h.weight, 0);
    return scored
      .map((h) => ({ ...h, share: total > 0 ? round((h.weight / total) * 100, 1) : 0 }))
      .sort((a, b) => b.share - a.share || a.id.localeCompare(b.id));
  };

  /* The same signals read under every other setting. This is the demonstration: the inputs
     do not move, the ranking does. */
  const alternatives = (derived, context) =>
    Object.keys(CONTEXTS)
      .filter((id) => id !== context)
      .map((id) => ({ context: id, leading: hypotheses(derived, id)[0] }));

  window.caasSandbox = { SIGNALS, CONTEXTS, derive, hypotheses, alternatives };

  document.addEventListener('alpine:init', () => {
    const { Alpine } = window;

    Alpine.data('detectionSandbox', () => ({
      context: 'concert',
      heart: SIGNALS.heart.fallback,
      movement: SIGNALS.movement.fallback,
      vocal: SIGNALS.vocal.fallback,
      alignment: SIGNALS.alignment.fallback,
      reported: SIGNALS.reported.fallback,

      init() {
        this.labels = JSON.parse(this.$el.dataset.labels || '{}');
        const state = window.caasUrlState;
        if (!state) return;
        Object.assign(this, state.read('ds', this.defaults()));
        window.Alpine.effect(() => {
          const current = {
            context: this.context,
            heart: this.heart,
            movement: this.movement,
            vocal: this.vocal,
            alignment: this.alignment,
            reported: this.reported,
          };
          state.write('ds', current, this.defaults());
        });
      },

      defaults() {
        return {
          context: 'concert',
          heart: SIGNALS.heart.fallback,
          movement: SIGNALS.movement.fallback,
          vocal: SIGNALS.vocal.fallback,
          alignment: SIGNALS.alignment.fallback,
          reported: SIGNALS.reported.fallback,
        };
      },

      reset() {
        Object.assign(this, this.defaults());
      },

      get derived() {
        return derive({
          heart: this.heart,
          movement: this.movement,
          vocal: this.vocal,
          alignment: this.alignment,
          reported: this.reported,
        });
      },

      get readings() {
        return hypotheses(this.derived, this.context);
      },

      get others() {
        return alternatives(this.derived, this.context);
      },

      /* Two readings within ten points of each other are not a conclusion. The sandbox says
         so in words rather than leaving a bar chart to imply a winner. */
      get separation() {
        const [first, second] = this.readings;
        return second ? round(first.share - second.share, 1) : 0;
      },

      get undecided() {
        return this.separation < 10;
      },

      label(key) {
        return (this.labels && this.labels[key]) || key;
      },
    }));
  });
})();
