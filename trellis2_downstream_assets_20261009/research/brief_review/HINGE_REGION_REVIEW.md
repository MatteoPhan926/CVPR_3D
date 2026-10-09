# A: target door region and hinge review

Parent-requested follow-up, 2026-10-09. I opened existing files with `view_image`; no new render, asset import or edit was performed. This is an independent inspection of the parent's saved images, not validation of a finished authored result.

## Evidence actually viewed

- `artifacts/presentation_controls/A/side_native.png`
- `artifacts/presentation_controls/A/side_basecolor.png`
- `artifacts/presentation_controls/A/side_clay.png`
- `artifacts/presentation_controls/A/q1_basecolor.png`
- `artifacts/presentation_controls/A/q1_clay.png`
- `inputs/original_intended_reference.jpg`

Read `artifacts/presentation_controls/A/controls.json`, `artifacts/raw_inspection/A_v2/inspection.json`, `source/presentation_controls.py`, and the initial proposed `config/door_A.json` / `source/author_door.py`. Parent selected A by filename order before authoring; B remains a raw/presentation/roundtrip comparison. Conclusions about completed articulation will therefore apply to A only.

## Direct observations

The front of A is +X (screen right in the exact side view); the inspected target side is -Y; Z is up. The intended front door consists of the front side-window region and body panel immediately below it, between the B-pillar and cowl. It does not include the rear side window, hood, front fender or running board. The native/base-color views support the same location despite different apparent shading.

At 900×600 side-image resolution, the rear edge is around image x=410–420, the cowl boundary around x=535–545, the upper window-frame edge around y=214–220, and the intended lower panel around y=358–363. These are manual approximate observations, not segmentation labels. The exact seam is weak in places; the clay view supports an approximate surface cut rather than an already separated semantic door.

The front side window contains an actual opening in the clay as well as native views, with irregular internal/behind-window geometry visible. Its black appearance cannot be treated as only a painted dark texture. Existing glass semantics or a coherent transparent pane are not established. New opaque lining must not accidentally fill that opening. If a glass plane is authored later, report it as added and retain the original appearance for comparison.

The original photo confirms the intended door by its relationship to the windshield and rear door. It does not resolve exact hinge hardware or a measured physical pivot. A rear-edge hinge is a plausible authoring assumption for the identified Traction Avant, but this review has not established its location from external historical/mechanical documentation. Do not label the resulting axis recovered ground truth.

## Proposed geometry guidance, not an edited configuration

The parent's initial polygon was:

```
[[-0.070, -0.112], [0.148, -0.112], [0.151, 0.018],
 [0.115, 0.098], [0.077, 0.137], [-0.052, 0.136]]
```

The upper/front outline is broadly consistent with the target region in the reviewed images. The initial lower edge at Z=-0.112 maps to side-image y≈371, overlapping the fixed running-board/sill band. A lower edge around **Z=-0.096 to -0.100** (image y≈360–363) is the safer starting cut to keep that band fixed. This is a specific, asset-derived refinement to the proposed selection; it is not a guarantee of semantic accuracy. The outer door edge should follow the visible local boundary if later views justify a curved/local correction.

The image/world mapping follows the saved exact-side orthographic camera: center X=0.00047418, center Z=-0.00043282, width=900, height=600, ortho scale=1.42251372. With landscape horizontal camera fit, image pixels per unit ≈632.68:

```
world_X ≈ 0.00047418 + (image_x - 450) / 632.68
world_Z ≈ -0.00043282 - (image_y - 300) / 632.68
```

This mapping is consistent with the reported ~1.002 unit length spanning roughly 630 pixels. A side image alone does not determine the hinge Y coordinate; it must come from the actual local mesh surface. Treat `hinge_xyz=[-0.061,-0.153,0]` as a provisional authored pivot, not verified mechanical position.

For a rear-edge pivot and front edge in +X, a **negative rotation about +Z** moves the front edge toward -Y, outward on the intended side. The parent's negative rotation sign is therefore consistent with the declared coordinate frame. Stop and revise the pivot only if the saved trajectory exposes visible gross interference; this is not a physical clearance certification.

## Source-level confound to avoid

In the initial `source/author_door.py`, `boundary_edges` is computed from **all** open boundaries of the selected door. The same array feeds moving door thickness and fixed aperture jamb strips. It includes the pre-existing front-window opening, so indiscriminately applying a fixed jamb there can leave stationary strips around the window when the door opens.

Moving edge thickness can use appropriate door/window boundaries. **Fixed jamb strips should use only the newly cut outer body aperture**, identified using clipping-plane provenance or distance to the actual cut boundaries, and should exclude pre-existing window-hole boundaries. This is a prospective source review, not a claim that the failure has appeared in an executed render. It matters because an artifact from this implementation must not be attributed to the generator.

## Completion and stop rule

The review supports trying this local conventional door operation. It does not establish that A already meets convincing-CGI appearance or that the proposed cut will pass. Inspect the exported, reopened 0/30/60° states, reverse trajectory, fixed running board/fender/roof/body, and exposed cabin/edge before judging success. Parent's single bounded local correction is sufficient for this screen; if further broad remodeling or repeated speculative repair becomes necessary, retain the useful partial result and state the actual unmet criterion.

No A/B resolution claim, human labor saving, artist acceptance or topology-necessity conclusion follows from this review.
