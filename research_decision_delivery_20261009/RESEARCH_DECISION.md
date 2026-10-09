# Research decision: from generated appearance to a useful downstream asset

**Decision date:** 9 October 2026, Asia/Bangkok.  
**Disposition:** **REFRAME; no current CVPR/ICCV method commitment.** Close the claim that ordinary color/material conversion or ten-step edge bisection is itself the contribution. Retain the measured engineering gains and the broad 2D → generated 3D → useful-workflow objective.

This is the final decision synthesis for the completed investigation, not a claim that every planned diagnostic passed. The next study below is a proposal, not a running job. No experiment was rerun while recovering or preparing this delivery; the new work here is source/result inspection, arithmetic over retained JSON, and two independent read-only reviews.

## What evidence was obtained, and why it changes the decision

The investigation went beyond the external audit: separate investigators checked actual execution, authoring/display attribution and historical assets before combining findings; later work generated two non-car controls, tested numerical extraction and challenged the interpretation. Primary graphics/specification sources were used to resolve specific questions, not as a substitute for available measurements.

| Evidence | Observed result | Research implication |
|---|---|---|
| Actual generation provenance | The completed audited car is one TripoSR CPU candidate. Hosted TRELLIS.2 was quota-blocked before output. | The car says nothing about TRELLIS.2 quality or a best-available generator frontier. |
| Reproduction from retained processed input | One saved CPU forward replay gives exact latent equality, maximum error 0.0. Decoder replay matches all 53,904 quantized vertex colors; re-extraction reproduces geometry/RGBA under reordering, including oriented triangle multiplicity. | Strong execution provenance; neither the source photograph's reconstruction accuracy nor preprocessing optimality is thereby established. |
| Controlled material/display comparison | Changing only the prior display material gives RGB MAE 0.1383/0.1459 and display-luma changes of about +50.9%/+42.0% in side/hero views. | A conspicuous visual discrepancy can arise without a different generated object. Do not attribute it all to model paint or topology. |
| Controlled source partition | Same-material flat raw/partitioned closed renders have MAE 0.0000109/0.0000164 and silhouette IoU 1.0 in those two views. | Cutting the retained exterior is not the principal closed-pose appearance loss in this case. This does not certify semantic door selection. |
| Moving-region audit | The selection has a 7,264-face main component plus a detached 1,115-face lower component; the latter is 14.39% of selected area and predominantly horizontal. | A weak selection/completion recipe remains a competing explanation for opening failure. No accurate door-boundary label or competent-operator ceiling was measured. |
| Two prospective export controls | One teapot and one hamburger inference, fixed choices/seed, retained raw meshes and latents. Export variants preserve positions/indices. | These establish new non-car evidence. They were prospective for the export question, not unseen validation for the later extraction hypothesis. |
| Numerical extraction control | Ten safeguarded bisections on existing grid edges, followed by refreshed RGB, improve agreement with the same model's native rendering on all three explored objects. | A useful conventional baseline exists; the endpoint and attribution must remain narrow. |
| Historical successes | Bentley preserves 24 texture payloads and eight untouched geometries. The historical Particulate OOM was solved by compatible chunking. | Useful authoring and successful execution were overlooked by stronger negative framings; neither establishes a new complete image-to-useful-asset result. Bentley upstream image/model provenance and original chair artifacts remain missing. |

The audited car did achieve reversible controlled motion in the prior mechanical checks, but failed its convincing-CGI target. No artist acceptance or measured human labor saving was established. A supplied Bentley GLB cannot be counted as a demonstrated image-generation chain without the missing upstream provenance.

## Quantified extraction result and its competing explanation

Pixel-weighted RGB MAE against native-field rendering, using the shared original/refined mesh mask over three 160×160 views per object:

| Object | Original geometry + original RGB | Refined geometry + original RGB | Original geometry + refined RGB | Refined geometry + refined RGB | Joint relative reduction |
|---|---:|---:|---:|---:|---:|
| Car | 0.064399 | 0.064664 | 0.058161 | 0.057307 | 11.0% |
| Teapot | 0.040552 | 0.040194 | 0.038335 | 0.037797 | 6.8% |
| Hamburger | 0.059224 | 0.058244 | 0.049747 | 0.048341 | 18.4% |

[Original aggregate](evidence/extraction_control/verification_and_aggregate.json), [derived summary](DERIVED_SUMMARY.json), and [arithmetic-only script](build_summary.py) make the table inspectable.

Most of the reduction remains when original geometry is paired with refreshed RGB. Geometry-only movement slightly worsens the car score. These are sensitivity controls, **not additive causal percentages**: the refreshed colors were still sampled at refined positions. “Better agreement after refinement and color resampling” is supported; “better real geometry” is not.

For the car, mean absolute density residual falls from 4.193 to 0.0103; mean displacement is 0.000734 model units, about 0.108 grid cell. Across objects, measured refinement-query/RGB time is 0.49–0.92 seconds; refinement plus export is about 0.92–2.03 seconds. These are scoped CPU timings, not total generation or artist-workflow costs.

Faces remain fixed, edge brackets are verified and no negative original/refined face-normal dot products were recorded. These checks do not establish absence of self-intersections, semantic correctness or a valid solid. The car meshes are non-watertight; logged `volume` values are signed mesh integrals, not physical enclosed volumes.

The common mask intersects two mesh rasters, not independently measured native support. Mesh-to-mesh silhouette IoU exceeds 0.9907 but is not ground-truth agreement. Full-image MAE also improves, so masking alone does not explain the gain. Native volume rendering uses 128 samples per ray and is an internal comparator; volume/surface rendering, sampling and interpolation differ inherently. Three objects and multiple camera views do not form a generalization benchmark.

## Implementation findings and unfinished work

1. **Saved forward replay is complete.** Older drafts calling it pending are superseded by the recovered [result](evidence/root_analysis/saved_forward_reproduction.json). Exact reproduction of the retained processed image does not settle the audit's premultiplied/double-alpha concern, optimal masking or CPU/GPU parity.
2. **The log-density comparator failed before producing a comparison.** The actual pinned [checkpoint configuration](evidence/checkpoint_configuration/checkpoint_config.yaml) says `density_activation: exp`, and [activation code](evidence/checkpoint_configuration/activation_utils.py) dispatches to `torch.exp`. The [attempt](evidence/extraction_control/log_density_control.py) incorrectly asserts `trunc_exp`; its [log](evidence/extraction_control/log_density_run.log) stops there. A class default was mistaken for loaded configuration. This is not a negative result for log interpolation. Taking logs removes the final exponential, while the underlying SiLU decoder remains nonlinear. No fix or new comparator run is claimed.
3. **Browser export validation did not pass.** The geometry-preserving [variant checks](evidence/root_analysis/exports/validation.json) succeeded, but the [browser log](evidence/root_analysis/browser/verification.log) ends in a readiness timeout. A script-before-body bootstrap problem is a source-level suspect, not a validated diagnosis. The earlier missing-SciPy failure is retained. Corrected exports must not be advertised as cross-viewer validated.
4. **The method baseline is old.** The preserved [Graphics Gems source](evidence/adversarial_review/prior_check/graphics_gems_implicit_c.txt) contains ten-step edge bisection. This directly challenges novelty of that mechanism; it is not an exhaustive literature review ruling out all task-level contributions.
5. **Eligible baselines remain unmeasured.** Official TripoSR texture baking, an appropriate competent conventional edit, and a real downstream utility comparison were not completed. Their absence prevents claims of superiority; it does not oblige an indefinite repair campaign.

The original independent [history report](evidence/history_opportunities/HISTORY_OPPORTUNITIES.md) and [adversarial draft](evidence/adversarial_review/REVIEW.md) are preserved verbatim. Their time-dependent pending statuses are superseded here, not silently rewritten.

## Strongest remaining alternative explanation

Ordinary display/material interpretation, nonlinear field interpolation and RGB resampling explain substantial observed differences; a weak door-selection/interior recipe explains additional authoring problems. Residual defects may still reflect generation, preprocessing or incomplete view information. Current data do not isolate those remaining causes.

The positive numerical result is real and could matter for preserving an already accepted generated appearance. What is missing is evidence that the preserved appearance enables a valued operation at useful cost. Reducing disagreement with the model itself does not establish accuracy relative to the photograph, better topology, artist acceptance or saved labor.

## Justified next research decision

**Do not allocate a new representation/model or another car-generation campaign on this evidence.** Keep the diagnostic controls as competent baselines. Close export conversion and generic edge bisection as the current *method claim*, while retaining their practical value. This closes a claim, not the broader project.

The next useful allocation is **one bounded downstream screen, only after an actual use contract is fixed**. A reasonable candidate is scene layout/camera previsualization with the already generated non-car assets. This is distinct from the unconfirmed proposed local-revision study and the separately mentioned car experiment.

The handoff should require:

- A named consumer or a clearly labeled technical-screen substitute; specify deliverable, intended screen size, camera excursion, placement/occlusion needs, and whether a mesh or relighting is actually required **before** comparing outputs.
- The existing teapot/hamburger for a pilot, no new encoder calls or seed search. Predeclare an operator-time/runtime budget; a practical proposed pilot cap is 30 minutes active preparation per method/asset, not an observed cost or a statistical threshold.
- A competent conventional mesh path, including material conversion and eligible official texture baking; an image/alpha-card implementation and native-field delivery wherever they meet the same contract. Do not invent a mesh requirement after seeing results. If refinement is the intervention, keep the original-geometry/refreshed-RGB sensitivity control.
- Record preparation actions/time, import/reopen and continuation in the target workflow, defects along the specified path and acceptance of the actual deliverable. Assistant-only scoring stays a technical screen; artist usefulness remains unmeasured.
- A small consistent quality–cost benefit may warrant a focused prototype; no dramatic gap is required. Advancement then needs a prospective asset split and the cheapest relevant competitor. These three explored objects cannot become retrospective held-outs.

**Stop rules:** if standard baselines satisfy the contract and no consequential quality–cost residual remains, retain the workflow as engineering and close that formulation. If an image card/native field is equally useful at comparable cost, do not promote a mesh-specific intervention. If all outputs fail, classify the failure without blaming export by default. Only a consequential reproducible residual plus an intervention that predicts a useful improvement earns another prototype.

Fixing every pending diagnostic is not a prerequisite for this allocation decision. Browser validation becomes necessary if a corrected GLB is used in the pilot; the log-density comparator becomes necessary if numerical extraction efficiency is claimed. Both remain **not started as follow-up work**.

## Scope, evidence and handoff

The separately proceeding car experiment still has unknown generator, contract, workspace, branch and run ID. It is not equated with the audited car. The non-car revision experiment remains a proposal without verified execution metadata. No duplicate work is assigned.

[RUN_LEDGER.json](RUN_LEDGER.json) separates completed, failed and proposed work. [REVIEWS.md](REVIEWS.md) records the final independent checks. [FULL_EVIDENCE.json](FULL_EVIDENCE.json) identifies immutable archives, manifests and verification receipts for all 813 recovered payload files, including all three latents. This compact delivery contains selected evidence and synthesis; it does not replace those full archives.

[SECRETARY_HANDOFF.md](SECRETARY_HANDOFF.md) is the requested transfer document. No message was sent to a separate secretary account or external channel.

