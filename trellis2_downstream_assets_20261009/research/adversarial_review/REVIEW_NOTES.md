# Independent adversarial review notes

Status: provisional evidence record. Final assessment awaits the parent's completed authoring, fresh reimport verification, and matched raw control. Reviewed 2026-10-09. No rendering, editing of assets, generation, or experiments were performed by this reviewer.

## Scope and claim discipline

The declared target remains a recognizable whole vehicle with its camera-facing front door continuously opening 0–60 degrees, coherent frame/glass/handle/lining, fixed other parts, a reversible slider, and convincing whole-car and close edge/cabin views. Conventional local selection, repair, completion and pivot authoring are allowed. Coarse blocking potential cannot replace this target. A mechanical/export pass cannot establish artist acceptance.

A is the earlier supplied filename and was chosen by filename order, not favorable appearance. B is descriptive only. User-reported 512/1536 trials do not identify file mapping, seed, decimation, or original/background-removed input linkage. No controlled resolution or generator-general claim is available.

## Evidence directly inspected

- `config/INHERITED_AUTHORING_INTENT.md`, `config/BOUNDED_INVESTIGATION.md`, `config/door_A.json`, `inputs/PROVENANCE.json`, `README.md`, `research/EXECUTION_NOTES.md`.
- `research/integrity/REPORT.md`; `research/brief_review/INDEPENDENT_BRIEF_REVIEW.md` and `HINGE_REGION_REVIEW.md`. Their probe outcomes remain attributed evidence, distinct from this reviewer's image inspection.
- `source/author_door.py`, `source/presentation_controls.py`, `source/inspect_render.py`; A native inspection metadata and both presentation-control metadata files.
- Opened with `view_image`: original reference JPEG; all five A presentation controls; all four A raw orbit views; all five B presentation controls and B raw q2/q3/q4; v1 partition-only closed/open60; v1 hero 0/30/60 and side 0/30/60.

## Provisional visual observations

Both raw assets are recognizable as the intended class of vintage Citroen, with the upright cabin, tall narrow grille, round lamps, separate fenders and bright bumper visible. Their textures supply considerable identity. This is a visual recognition finding, not proof of photorealism or task utility. A has visibly uneven panels/fenders/tires, a sparse open front side-window region, and a small detached piece below the cabin. Its front-window opening persists in clay. B has a different, more closed-looking window region; no downstream operation has been tested on B.

Base-color emission is substantially darker than the native studio view. It supports presentation/material interaction as an explanation for a pale/silver appearance. Because emission bypasses PBR lighting and still uses AgX, it is a diagnostic, not a demonstrated lighting/material repair or fidelity metric. The native maps can contain illumination-like features; this does not by itself assign a model defect. B's files named `side_*` are frontal views because the cameras use world coordinates and the assets have different orientations.

The v1 closed result broadly retains A's exterior; a same-camera raw/partition comparison is still required to isolate cutting effects. At 30 and 60 degrees the front-door region visibly moves and an aperture appears, while the visible rest of the car remains in place. Open hero and side views show layered, irregular leading-edge/frame surfaces and a crude exposed cabin. Similar edge irregularity appears in partition-only open60, before lining, thickness, fixed jamb and cabin additions. It cannot be attributed solely to those additions. These images alone do not distinguish source internal surfaces from the projected/depth-limited selection, clipping effects, or their interaction.

## Source-level alternatives and limitations

- `author_door.py:23–28` defines a hand-authored convex projected polygon and `Y <= -0.100` halfspace. These encode a selection policy, not recovered semantic membership. A correct rigid transform can move incidental sheets along with the intended exterior.
- Lines 58–60 preserve total surface area and face provenance. Area preservation alone does not certify correct selection, cut-boundary continuity, absence of holes/overlap, or rendering equivalence.
- Lines 61–74 carry per-corner UVs/normals and reuse the original material. This is materially stronger than a vertex-color-only reconstruction, but executed export/reimport checks are still required.
- Lines 109–127 offset the entire selected surface in fixed +Y for lining and edge strips, rather than constructing a coherent custom panel. Irregular source surfaces can therefore be duplicated. Fixed jamb edges are restricted to clipping planes, avoiding the known original-window-boundary confound.
- Lines 134–137 add simple floor/seat/dashboard proxies. They are not recovered cabin geometry; their quality cannot represent the ceiling of conventional completion.
- Lines 142–156 keyframe a custom slider and request sampled GLB export. Only actual channel/reimport inspection can demonstrate that the exported artifact plays the intended door motion. The Blender custom property and a portable GLB animation are separate capabilities.

## Cheap discriminating controls

1. Complete fresh reimport tests for generated exterior preservation, UV/decoded texture/material retention, animation interval/trajectory/return, fixed-body behavior, and saved 0/30/60 views. A validator pass alone is insufficient.
2. Match raw versus partition-only closed camera, dimensions, lighting, exposure and material. Keep exposure-only appearance changes distinct from cuts.
3. For the jagged door edge, use retained face provenance to mark wholly-inside original faces versus clipped triangle descendants and mark new boundary segments by plane, especially the Y cutoff. Inspect the isolated native moving panel with additions hidden. A read-only depth/normal-area summary can accompany this but is not a semantic rule: legitimate frame faces have tangent/inward normals.
4. If a further experiment is justified after this bounded screen, a targeted local face-selection/contour or lining correction is a stronger discriminator than regeneration or global retopology. Preserve the exterior/UVs and matched views. It tests this preparation recipe, not a broad conventional-workflow limit.

No final pass/fail or publication contribution is selected in these notes.
