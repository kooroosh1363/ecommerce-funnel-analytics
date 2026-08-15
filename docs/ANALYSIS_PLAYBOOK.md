# Analysis Playbook

## Analytical grain

The raw table is **event-level**: one row per event. The analytical session matrix is **one row per session**, with binary indicators showing which funnel stages were reached.

## Funnel definition

The canonical ordered funnel is:

`visit → product_view → add_to_cart → checkout → purchase`

A later stage can only occur after all earlier stages in the synthetic generator. The validation layer explicitly checks ordering.

## Core metrics

- **Step conversion**: sessions reaching current stage / sessions reaching previous stage.
- **Step drop-off**: 1 - step conversion.
- **Visit-to-stage conversion**: sessions reaching a stage / sessions that started the funnel.
- **Journey outcome**: the furthest stage reached by a session.

## Interpretation guardrails

This project uses deterministic synthetic data to demonstrate funnel methodology. Differences by channel/device are intentionally encoded so diagnostics have meaningful patterns. They are not claims about a real business.

A funnel identifies **where** users leave, not automatically **why**. Real causal diagnosis would combine event instrumentation with UX research, experiments, performance telemetry, and qualitative evidence.

## Business actions

- High product-view → cart drop-off can motivate merchandising, pricing, or CTA investigation.
- High cart → checkout drop-off can motivate cart UX, shipping-cost, or trust-friction analysis.
- High checkout → purchase drop-off can motivate payment-failure and checkout-form diagnostics.
- Segment differences should trigger hypotheses and experiments, not causal claims by themselves.
