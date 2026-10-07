# Bounded authoring revisions

1. One contour cut and pivot were derived from the new raw car. Added opaque door inner skin/edges, jamb and four cabin proxy boxes. Explicit COLOR_0 PBR material uses raw glTF defaults metallic=1 and roughness=1; authored exterior normals are smoothed (raw GLTFLoader uses flatShading when normals are absent). No base color correction.
2. Reopening the first export revealed cabin box protrusions beyond the windshield and lower silhouette, visible in the retained v1 renders. One local correction reduced/repositioned the four proxy boxes within the cabin. Cut, hinge, generated geometry and generation candidate did not change. No global remodeling attempted.
3. Viewer verification caught a timeline mapping error: the exported clip includes opening and closing. Viewer config selects only its 1/30–61/30-second opening interval for the 0–60 slider. Failed run is retained. This is a playback correction, not an asset or generator retry.

Raw inspection initially lacked a Blender vertex-color material, then was corrected for inspection only. Those early Blender renders use metallic=0/roughness=.8 and flat faces, unlike browser raw default metallic=1/roughness=1. Use matching browser raw/authored evidence for comparisons; color difference in the earlier display is not solely a generator result.
