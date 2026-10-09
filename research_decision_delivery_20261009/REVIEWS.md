# Final independent reviews — 9 October 2026

Two separate agents inspected actual retained files. They made no file changes, model calls, renders or repairs. This record summarizes their findings and the corrections incorporated into the final decision.

## Independent evidence review

- Saved-forward replay completed with exact latent equality; reproduction starts from the retained processed input, not necessarily optimal preprocessing.
- Grid endpoints agree with direct field queries and all threshold brackets are valid. Linear-interpolation residual is about 0.000377 in mean, whereas direct field evaluation at raw vertices has mean residual 4.193 for the car. This isolates nonlinear interpolation error rather than a coordinate mismatch.
- Bisection plus RGB resampling yields joint MAE reductions of 11.0%, 6.8%, 18.4% on the three explored objects. Displacements are small relative to a grid cell. No ground-truth geometric improvement or artist benefit follows.
- Original geometry with refined RGB recovers roughly 88.0%, 80.5%, 87.1% of the joint reduction. Those ratios are sensitivity descriptions, not additive causal attribution; refined positions were used to obtain the RGB.
- The actual pinned model config specifies `exp`; the attempted log baseline's `trunc_exp` assertion is wrong. No comparator result was produced. Log transformation removes the final exponential but does not linearize the SiLU decoder.
- Recommendation: retain reproducibility and conventional baselines; do not promote density residual or bisection itself as the method contribution.

## Adversarial decision review

The reviewer was asked to challenge the proposed no-method-commitment decision, identify overlooked positive evidence and test whether the next allocation was justified.

- Export correction must remain partially validated: positions/indices checks passed, browser validation did not.
- Color resampling carries most measured MAE gain; geometry-only movement slightly worsens the car score.
- Common-mask support is the intersection of two mesh rasters, not ground truth. Full-image MAE also improves, so masking alone does not explain the result.
- Native-field agreement can be a legitimate appearance-preservation endpoint for an already accepted field. It does not by itself demonstrate reconstruction accuracy or a useful artist operation.
- Non-watertight mesh `volume` fields must be described as signed mesh integrals or omitted. Fixed faces/no negative normal-dot pairs do not certify geometric validity.
- The preserved Graphics Gems source contains ten-step edge convergence; no new-solver claim follows.
- Close the current method claim, not the broader objective. A downstream preview screen must earn its relevance through an actual use contract and competent image/mesh/field alternatives. “Loads and rotates” would repeat the current limitation.
- A modest reproducible quality–cost benefit can motivate one prototype; a dramatic gap or failure of every conventional method is not required.

## How the final report changed

The final synthesis now includes the completed forward replay, copied actual checkpoint configuration, corrected activation attribution, crossed geometry/RGB table, qualified mask/volume endpoints, explicit failed-test status and a conditional downstream allocation with stop rules.

This review is evidence assessment, not a publication endorsement or an independent rerun. See [DERIVED_SUMMARY.json](DERIVED_SUMMARY.json), the linked original records in [RESEARCH_DECISION.md](RESEARCH_DECISION.md), and [SOURCE_FILES_SHA256.json](SOURCE_FILES_SHA256.json).


A final read-only audit of the completed report/handoff found no material factual correction. Its allocation-rule clarification was incorporated: baseline quality passing alone does not close useful efficiency research; closure requires no consequential remaining quality–cost residual.
