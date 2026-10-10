"""Read-only same-camera image differences and recorded trajectory diagnostics."""
from pathlib import Path
import numpy as np,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'research/final_validation/control_measurements.json'
assert not out.exists()
pairs=[('raw_vs_partition_closed','raw_same_camera_A/hero.png','authoring_A_v1/partition_only_closed.png'),('partition_vs_completed_closed','authoring_A_v1/partition_only_closed.png','authoring_A_v1/hero_00.png')]
for view in ['hero','side']:
 for angle in ['00','30','60']:
  pairs.append((f'authored_vs_reopened_{view}_{angle}',f'authoring_A_v1/{view}_{angle}.png',f'reopened_A_v1/{view}_{angle}.png'))
rows=[]
for name,a,b in pairs:
 x=np.asarray(Image.open(ROOT/'artifacts'/a).convert('RGB'),dtype=float)/255
 y=np.asarray(Image.open(ROOT/'artifacts'/b).convert('RGB'),dtype=float)/255
 assert x.shape==y.shape==(960,1440,3)
 error=np.abs(x-y);bg=x[0,0]
 mask=(np.abs(x-bg).max(axis=2)>2/255)|(np.abs(y-bg).max(axis=2)>2/255)
 rows.append({'name':name,'a':a,'b':b,'shape':list(x.shape),'full_image_rgb_mae_0_1':float(error.mean()),'max_channel_error':float(error.max()),'foreground_rgb_mae_0_1':float(error[mask].mean()),'foreground_pixels':int(mask.sum()),'fraction_foreground_pixels_mean_error_gt_8_of_255':float((error.mean(axis=2)[mask]>8/255).mean())})
motion=json.loads((ROOT/'artifacts/reopened_A_v1/motion_verification.json').read_text())
hs=np.array([r['hinge_matrix'] for r in motion['trajectory']]);ds=np.array([r['door_matrix'] for r in motion['trajectory']])
rel=np.linalg.inv(hs)@ds
rot=hs[:,:3,:3]@hs[0,:3,:3].T
angles=-np.degrees(np.arctan2(rot[:,1,0],rot[:,0,0]))
expected=np.r_[np.arange(61),np.arange(59,-1,-1)]
metrics={'checked_samples':len(angles),'angles_deg':angles.tolist(),'max_error_from_linear_1_degree_per_frame':float(np.abs(angles-expected).max()),'opening_monotonic':bool(np.all(np.diff(angles[:61])>0)),'closing_monotonic':bool(np.all(np.diff(angles[60:])<0)),'max_door_local_transform_error_relative_to_hinge':float(np.abs(rel-rel[0]).max()),'fixed_body_scope':'Original fresh import probe asserts every sampled body matrix within1e-7. Its reported0 is a literal and is not treated here as measured bitwise equality.'}
assert metrics['opening_monotonic'] and metrics['closing_monotonic']
assert metrics['max_error_from_linear_1_degree_per_frame']<1e-4
assert metrics['max_door_local_transform_error_relative_to_hinge']<1e-6
result={'image_controls':rows,'trajectory_derived_metrics':metrics,'interpretation_limits':'Image differences measure preservation under these fixed renders, not visual target achievement or artist preference. Foreground uses a simple uniform-background mask; stochastic rendering and interpolated normals can cause differences. Motion is discrete samples plus exported animation, not collision certification.'}
out.write_text(json.dumps(result,indent=2))
print(json.dumps({'image_controls':rows,'trajectory':{k:v for k,v in metrics.items() if k!='angles_deg'}},indent=2))
