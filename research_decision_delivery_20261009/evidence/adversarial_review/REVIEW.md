# Adversarial review of the 8 October 2026 research decision

**Provisional allocation: keep the empirical corrections; do not yet promote a CVPR/ICCV method.** The strongest present explanation for the conspicuously pale car display is a conventional appearance-transfer mismatch. The authoring evidence separately exposes a weak selection/completion recipe. Neither explains away all shape deficits, and neither supports a general impossibility claim about useful generated assets.

This review first inspected the new numerical results, diagnostic code, controlled car render sheet and open-door subtraction pair, together with the historical reproduction/allocation records. It read the external execution audit only afterward. It executed small arithmetic over existing JSON and an independent direct GLB accessor comparison. It did not run inference, repair assets, survey literature, change historical workspaces, or measure artist acceptance. Browser holdout and root-refinement results remain pending at this version; the allocation below is explicitly conditional on those results.

## Evidence identities and limits

- The audited Citroën car is the historical TripoSR CPU fallback, raw SHA-256 `5bd4ab3776084c5586201abd0d3be36416b3331cb28295d8d066ac7ac7beac3d`. Saved-latent diagnostics are not another car generation.
- A separately mentioned car experiment has **UNKNOWN metadata/status** here. It must not be counted as this car, a replicate, or a result supporting any conclusion.
- The non-car revision trial is **proposed, not verified running**. It is distinct from the current teapot/hamburger static-export controls.
- Current `holdouts/*/execution.json` records exactly one generation for each of teapot and hamburger. Both are pinned official example images. They are new outputs, not recovered historical non-car evidence.
- Bentley supports supplied-asset authoring and preservation; its image-generation provenance is missing. Particulate's amended chair reproduction supports successful execution/export after compatible chunking, not correct articulation. Its original OOM has no quality implication. TRELLIS.2 produced no candidate in the audited car attempt.

The historical `NO_DEFENSIBLE_CANDIDATE` decision is evidence about its formulations. It is neither a novelty oracle nor a reason to reject a new, task-linked observation.

## What the new measurements actually establish

| New evidence | Supported conclusion | Attractive but unsupported extension |
|---|---|---|
| Saved latent reproduces every raw vertex exactly under a bijection, triangle sets match, corresponding quantized RGB matches exactly | The retained raw mesh is consistent with this extraction pipeline and saved latent; array ordering initially hid this | The original encoder/preprocessing is independently validated, or the candidate is an accurate reconstruction |
| Native field and direct vertex-RGB renders are dark; applying linear-to-sRGB makes the same geometry pale | Interpretation of numeric RGB explains a large display difference without a different generated object | The output is physical albedo, or unlit export recovers relightable material |
| Prior raw-display material changes common-foreground RGB MAE by 0.138–0.146 | A material choice is a major confound in screenshot comparisons | Material settings can fix all shape/texture errors |
| Same-material flat partition has MAE about 0.000011–0.000016, silhouette IoU 1.0 in the two tested closed views | The source partition itself essentially preserves these rest-pose renders | The selected region is the correct door, or arbitrary articulation/completion is solved |
| Smooth partition differs by about 0.000120–0.000202 from smooth raw | The partition's closed-pose shading contribution is small here | The exported normal policy is universally adequate |
| Open additions affect 5.07%/7.24% of common opaque pixels by more than 0.03 and change the silhouette | The supplied additions produce local visible changes; the inspected hero pair gains conspicuous patchiness | A pixel difference is an acceptance score, all differences are harmful, or completion generally harms opening |
| Car grid-edge endpoints agree exactly with queried endpoint density, bracket the threshold, and linearly interpolate to about 25 | The extraction convention is internally consistent | A large nonlinear density residual itself identifies a consequential geometric error |

The direct-mesh versus native-field RGB MAE is **0.06027 averaged across six views**, ranging **0.04932–0.07349**, on the mesh mask. This is not negligible numerical identity. It mixes volumetric versus hard-surface appearance, color sampling/interpolation, rasterization and silhouette/coverage effects. It is not photographic reconstruction error, a same-surface export error, or evidence that a novel method is needed. The existing mask includes edge pixels and is defined by the mesh rather than an independently agreed common field/mesh support.

An independent GLB check closes a small loophole in the initial order-invariant proof: comparing unordered triangle sets alone would ignore winding and duplicate multiplicity. `verify_oriented_reproduction.py` directly reads both retained GLBs, verifies identity scene transforms, builds the exact vertex bijection, and compares **oriented triangle multisets** and corresponding RGBA. All match; every raw oriented triangle has multiplicity one. Results are in `oriented_reproduction.json`. This strengthens extraction consistency without extending it to encoder correctness or photographic fidelity.

The measured secondary moving component is **14.39% of selected source area**, and **96.12% of that component's area has |normal-z| > 0.8**. This strongly motivates checking semantic ownership: it is predominantly a horizontal lower surface, not merely another vertical door fragment. Disconnected components alone cannot establish incorrect ownership. Crucially, the no-additions open render already exposes an incoherent opening. Completion subtraction therefore does not turn this into a valid door or isolate a general completion bottleneck.

## Attribution attacks that should survive into the final decision

1. **The causal endpoint changes between stages.** Same-mesh renderer agreement, native-field agreement, similarity to the photograph, usable scene placement, semantic editing and plausible hidden geometry are different targets. A success on the first cannot be sold as the others. A failure on the last cannot invalidate a static-prop use.
2. **The three-axis color story must remain explicit.** Neural RGB is saved to display images by the producer; glTF vertex colors have linear interpretation; PBR applies a lighting/material model. An appearance-preserving unlit mapping can be correct for that task while providing no independent light response. That limitation follows from the chosen task and material definition; it is not itself a novel discovered trade-off.
3. **Conversion and interpolation do not commute.** For barycentric weights, output-sRGB of interpolated inverse-sRGB vertex colors generally differs from directly interpolated display RGB. Residuals after corrected unlit export can come from this, quantization, edge coverage and rasterization. Do not label every residual an unsolved representation-transfer mechanism.
4. **Density residual is in arbitrary density units.** At current car vertices, the median nonlinear threshold residual is about 2.281, but its local first-order normal-displacement estimate is about 0.000335 world units, against cell width 0.006824. The 99th percentile displacement estimate is about 0.005566. Large tail estimates can reflect small gradients and a failed linear approximation. Root refinement must report actual displacement, geometry validity, image/normal changes and cost. Reducing the scalar residual mechanically validates the root solver, not useful extraction quality.
5. **The authoring controls are valuable but narrow.** Two exterior views and one open pose are not a collision check, ownership assessment or trajectory evaluation. Common-opaque-pixel errors deliberately omit newly visible regions, so they cannot alone characterize a completion whose purpose is to cover exposed regions. Sidedness having no effect in these views cannot establish irrelevance for every view or pose.
6. **Execution correctness and model adequacy remain separable.** Exact saved-latent reproduction largely closes a specific extraction/provenance concern. It does not test historical CPU/GPU parity, the unmodified encoder output, the consequence of double-alpha preprocessing, or generative quality. Current holdout preprocessing is deliberately frozen, so the new results will not answer the alpha question either.
7. **Two released examples are diagnostic holdouts, not an independent benchmark.** Their choice before output inspection and one-output limit prevent cherry-picking within this screen. Their published-example origin, one generator and sample size preclude prevalence or cross-generator generalization claims. Six cameras on one asset are not six independent assets.

## Stronger eligible comparators

These are comparators a later claim would need, not instructions to run every baseline now or a requirement that every conventional method fail before any prototype can be tried.

| Intended claim | Comparator that must be eligible | Why it matters |
|---|---|---|
| Preserve exported appearance | Correct inverse-sRGB transfer, explicit unlit material, real browser rendering, a simple color fixture | This may solve the claimed problem by standard file/material semantics |
| Preserve field detail at practical mesh cost | The pinned TripoSR `--bake-texture` route; its documented default atlas is 2048 pixels | Vertex-color interpolation is an optional representation choice, not the model's only supplied export route |
| Improve field-to-surface extraction | Ordinary edge root finding plus resampled colors; resolution/threshold and normal-policy controls at disclosed cost | A new solver must improve a useful endpoint beyond reducing the equation it directly optimizes |
| Useful short camera preview | Source-image alpha card, and native-field rendering with measured delivery/runtime cost | If a picture or the field already satisfies the task, a mesh-specific method has not earned its extra complexity |
| Useful supplied rigid edit | Verified selection/hinge, source-surface partition and conventional local completion by a competent operator | The current spatial crop, global-axis lining offset and cabin boxes are not a representative upper bound on ordinary authoring |
| Independent local appearance edits | Direct surface/texture editing or constrained fitting with all eligible variables | Spatially local target edits do not require artificially restricting the optimizer to local latent tokens |
| Broad image-to-usable-3D quality | A relevant successful contemporary generator under the stated budget, if the claim concerns broad model capability | A quota-blocked service has no quality result, and this fallback cannot stand in for all generators |

The texture-baking comparator is confirmed in the retained pinned TripoSR `README.md` and `run.py`; it has not been executed by this review. Its OpenGL dependency is an implementation requirement, not evidence of failure. Native-field rendering is eligible for preview tasks but not an automatic replacement for downstream tools that explicitly require a mesh; such a requirement must come from the actual use.

## Strongest remaining alternative and one worthwhile next decision

**Strongest alternative explanation:** much of the historical apparent failure comes from ordinary interface conventions and one weak authoring recipe, while remaining quality loss depends on the particular task. This explains the new evidence with fewer unsupported assumptions than a general topology/representation failure.

**Strongest still-live research possibility:** a consequential residual in preserving an already accepted generated appearance while enabling a specified downstream operation at useful cost. This is a question, not a nominated method. Examples such as a root solver, local editing or texture baking do not become research contributions just by being attached to it. A small consistent quality–cost improvement can justify a prototype; it need not defeat every baseline or establish field-wide impossibility first. It must predict an improvement on the actual operation against a competent comparator.

**Next decision:** after the current browser/root-refinement checks, decide whether there is any task-relevant residual worth one downstream comparison, or whether to close this diagnostic thread with an engineering correction. Do not respond to a successful export correction by expanding into another generator or repair campaign.

If a downstream comparison is warranted, use the already generated teapot and hamburger and one predeclared scene-preview task: fixed intended screen size, angular camera excursion and scene occlusion/placement requirement. Compare corrected GLB, source alpha card and native-field preview, recording preparation actions/time, runtime or delivery constraints, visible defects and acceptance for that task. Choose the requirement before inspecting comparative results. If only an assistant reviews it, call it a technical screen; artist acceptance remains unmeasured. This uses the retained outputs and does not duplicate the proposed non-car revision trial or any separately mentioned car experiment.

Predeclare the branching result:

- **Standard export matches the same-mesh reference, and the useful task is satisfied:** retain the engineering baseline; close export-as-method. A useful workflow result is worth retaining without calling it a CVPR contribution.
- **Image card or native field satisfies the same task as well at comparable cost:** the chosen task has not demonstrated value for a mesh-specific intervention. Close this formulation or change the task openly; do not manufacture a mesh requirement after seeing the result.
- **Corrected mesh fails where native field succeeds, and a bounded surface/extraction intervention predicts a useful improvement:** this is a candidate for one focused prototype against ordinary baking/root-finding controls, with held-out evidence and a cost budget. A native-field/mesh difference alone is insufficient.
- **Field and mesh both fail the intended use:** this experiment identifies a reconstruction limitation for these candidates. It does not motivate export research; a different generation capability would be a separate, explicitly scoped investigation.
- **Only arbitrary light changes or a newly exposed car interior cause failure:** the target has changed to material inference or completion. Establish its actual use and competent baseline before allocating that project.

Pending results could change which branch applies. They cannot retroactively create artist evidence, semantic labels, or novelty evidence that this screen did not collect.

## Evidence locations

- `generation_execution/provenance_results.json`, `field_results.json`, `interpolation_results.json`, `field_diagnostics.py`, and `controlled_comparison.png`.
- `authoring_attribution/measurements/{design,inventory,pixel_metrics,selection_components}.json`; independently inspected `H_full_authored_open_hero.png` and `I_partition_open_no_additions_hero.png`.
- `history_opportunities/{HISTORY_OPPORTUNITIES.md,artifact_contract_measurements.json}`; historical `REFERENCE_REPRODUCTION_REPORT.md` and `CVPR_DISCOVERY_DECISION_2026-10-05 (1).md`.
- `root_analysis/holdout_contract.json` and each `holdouts/*/execution.json`.
- External `inputs/IMAGE_TO_USABLE_CAR_EXECUTION_AUDIT_2026-10-08.md`, read after independent inspection and used for corroboration rather than as the decision authority.
