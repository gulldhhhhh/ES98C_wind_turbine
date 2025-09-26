# ES98C Active Learning for Offshore Wind-Farm Optimisation
We use PSO to steer new simulations toward under-explored turbine positions, skipping near-duplicates and cutting multi-hour runs. The loop auto-identifies coverage gaps, proposes the next batch, and preserves accuracy while improving the computational efficiency.

Pipeline:
- Fit/refresh a Gaussian (GP) model of the wind field from current simulations.
- Use PSO to propose turbine layouts/flow regimes that maximize uncertainty/coverage (i.e., where data is most needed).
- Run CFD at the proposed points and append results to the dataset.
- Update the GP with new data and repeat until a coverage/uncertainty threshold (or compute budget) is met.
