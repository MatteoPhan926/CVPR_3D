import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'artifacts'/'raw_same_camera_A';out.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/raw_inspection/A_v2/native_import.blend'))
s=bpy.context.scene;s.render.threads=2;s.render.resolution_x=1440;s.render.resolution_y=960;s.cycles.samples=32
center=Vector((.000474,-.003251,-.000433));cam=s.camera;cam.data.ortho_scale=1.42
for name,offset in [('hero',(1,-1,.4)),('side',(0,-1,.12))]:
 cam.location=center+Vector(offset)*2;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 # Presentation-only exposure control, geometry/UV/PBR unchanged.
 s.view_settings.exposure=-1.5
 s.render.filepath=str(out/(name+'_exposure_minus1p5.png'));bpy.ops.render.render(write_still=True)
 s.view_settings.exposure=0
(out/'control.json').write_text(json.dumps({'camera_match':'Identical hero and side camera/lighting/resolution/samples to authoring_A_v1','exposure_control_stops':-1.5,'material_geometry_changes':False,'interpretation':'Presentation sensitivity control; no photometric fit or proof of artist acceptance.'},indent=2))
