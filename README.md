# ES98C Active Learning for Offshore Wind-Farm Optimisation

Active-learning pipeline that cuts multi-hour CFD cost by steering simulations toward under explored turbine positions. We fit a Gaussian surrogate of the wind field, use Particle Swarm Optimization (PSO) to pick the next high-value points (max uncertainty / coverage), run CFD there, and iterate until targets are met.

> TL;DR — Stop simulating near-duplicates. Simulate where information gain is highest.

---

## Why
Full CFD sweeps over layout space are expensive and repetitive. This project:
- **Avoids redundant runs** (near-duplicate locations/flows)
- **Improves coverage** of the wind field / layout design space
- **Shrinks wall-clock time** to actionable results

---

## Pipeline
1.  Fit/update a Gaussian Process on current (layout -> wind-field metric) data.
2.  Optimize an acquisition (e.g., predictive variance, MI) to propose the **next batch** of layouts/flow.
