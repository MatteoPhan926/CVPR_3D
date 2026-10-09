"""Numerical control: fixed MC256 faces, threshold 25, ten edge bisections.

No encoder inference, dense grid, smoothing, topology change, or authoring repair.
All writes are confined to this script's directory. Original assets are read-only.
"""
import os
from pathlib import Path
OUT = Path(__file__).resolve().parent
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMBA_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key] = '2'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['NUMBA_CACHE_DIR'] = str(OUT/'numba_cache')
if hasattr(os, 'sched_getaffinity'):
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:2])
import sys, time, json, hashlib
import numpy as np
import torch
import trimesh
from PIL import Image, ImageDraw
GEN = OUT.parent/'generation_execution'
sys.path.insert(0, str(GEN))
from provenance_check import ROOT, load_field, summary
from field_diagnostics import raster, camera
from tsr.utils import get_spherical_cameras

THRESHOLD = 25.0
RESOLUTION = 256
ITERATIONS = 10
VIEWS = [0,60,120]
PIXELS = 160

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save_rgb(path, rgb):
    Image.fromarray(np.round(np.clip(rgb,0,1)*255).astype(np.uint8)).save(path)

def finite_summary(x):
    x=np.asarray(x)
    return summary(x) if x.size else None

def query(renderer, decoder, latent, points):
    with torch.no_grad():
        q=renderer.query_triplane(decoder,torch.as_tensor(points,dtype=torch.float32),latent)
    return q['density_act'].numpy().ravel(),q['color'].numpy()

def triangle_stats(vertices, faces):
    cross=np.cross(vertices[faces[:,1]]-vertices[faces[:,0]],vertices[faces[:,2]]-vertices[faces[:,0]])
    twice_area=np.linalg.norm(cross,axis=1)
    normals=cross/np.maximum(twice_area[:,None],1e-30)
    return cross,twice_area*.5,normals

def dihedral(mesh, normals):
    adj=mesh.face_adjacency
    cos=np.clip(np.einsum('ij,ij->i',normals[adj[:,0]],normals[adj[:,1]]),-1,1)
    return np.rad2deg(np.arccos(cos))

def geometry_report(raw, refined):
    c0,a0,n0=triangle_stats(np.asarray(raw.vertices),raw.faces)
    c1,a1,n1=triangle_stats(np.asarray(refined.vertices),refined.faces)
    d0,d1=dihedral(raw,n0),dihedral(raw,n1)
    flip=np.einsum('ij,ij->i',c0,c1)<0
    report={'faces_array_exact':bool(np.array_equal(raw.faces,refined.faces)),
        'negative_original_refined_normal_dot_count':int(flip.sum()),
        'flipped_original_area_fraction':float(a0[flip].sum()/a0.sum()),
        'face_normal_change_degrees':summary(np.rad2deg(np.arccos(np.clip(np.einsum('ij,ij->i',n0,n1),-1,1)))),
        'original_triangle_area':summary(a0),'refined_triangle_area':summary(a1),
        'original_degenerate_area_le_1e_14':int((a0<=1e-14).sum()),
        'refined_degenerate_area_le_1e_14':int((a1<=1e-14).sum()),
        'original_near_degenerate_area_le_1e_12':int((a0<=1e-12).sum()),
        'refined_near_degenerate_area_le_1e_12':int((a1<=1e-12).sum()),
        'original_adjacent_normal_angle_degrees':summary(d0),
        'refined_adjacent_normal_angle_degrees':summary(d1),
        'original_area':float(a0.sum()),'refined_area':float(a1.sum()),
        'original_volume':float(raw.volume),'refined_volume':float(refined.volume),
        'original_bounds':raw.bounds.tolist(),'refined_bounds':refined.bounds.tolist()}
    return report,flip

def refine(name, mesh_path, latent_path, decoder, renderer, latent):
    out=OUT/name;out.mkdir(exist_ok=True)
    started=time.monotonic()
    raw=trimesh.load(mesh_path,force='mesh',process=False)
    v=np.asarray(raw.vertices).copy();f=np.asarray(raw.faces).copy()
    radius=float(renderer.cfg.radius)
    coords=(torch.linspace(0,1,RESOLUTION)*(2*radius)-radius).numpy()
    lattice=(v+radius)/(2*radius)*(RESOLUTION-1)
    fraction=np.abs(lattice-np.round(lattice));axis=fraction.argmax(axis=1)
    rows=np.arange(len(v));lo_index=np.round(lattice).astype(int)
    lo_index[rows,axis]=np.floor(lattice[rows,axis]).astype(int)
    hi_index=lo_index.copy();hi_index[rows,axis]+=1
    assert lo_index.min()>=0 and hi_index.max()<RESOLUTION, 'Vertex outside extraction grid'
    p0,p1=coords[lo_index],coords[hi_index]
    d0,_=query(renderer,decoder,latent,p0);d1,_=query(renderer,decoder,latent,p1)
    draw,craw=query(renderer,decoder,latent,v)
    bracket=(d0-THRESHOLD)*(d1-THRESHOLD)<=0
    finite=np.isfinite(d0)&np.isfinite(d1)
    on_grid=np.max(np.sort(fraction,axis=1)[:,:2],axis=1)<5e-5
    valid=bracket&finite&on_grid
    original_rgb=np.asarray(raw.visual.vertex_colors)[:,:3]
    exact_color=np.all(np.round(craw*255).astype(np.uint8)==original_rgb,axis=1)
    t=(v[rows,axis]-p0[rows,axis])/(p1[rows,axis]-p0[rows,axis])
    linear_density=d0*(1-t)+d1*t
    report={'name':name,'source_mesh':str(mesh_path),'source_latent':str(latent_path),
        'source_mesh_sha256':digest(mesh_path),'source_latent_sha256':digest(latent_path),
        'vertices':len(v),'faces':len(f),'resolution':RESOLUTION,'threshold':THRESHOLD,
        'iterations':ITERATIONS,'radius':radius,'cell_width':float(coords[1]-coords[0]),
        'convention':{'vertices_inside_radius_cube':bool(np.max(np.abs(v))<=radius),
            'orthogonal_axes_lattice_roundoff':summary(np.sort(fraction,axis=1)[:,:2]),
            'bracketed_vertices':int(bracket.sum()),'valid_vertices':int(valid.sum()),
            'invalid_vertices_retained_original':int((~valid).sum()),
            'exact_original_rgb_quantization_fraction':float(exact_color.mean()),
            'linear_interpolation_threshold_abs_residual':summary(np.abs(linear_density-THRESHOLD))},
        'original_density':summary(draw),'original_density_abs_residual':summary(np.abs(draw-THRESHOLD))}
    assert exact_color.mean()>.999, 'Latent or coordinate RGB convention mismatch'
    assert valid.mean()>.999, 'Unverified grid-edge convention'
    # Safeguards: finite evaluations, verified sign brackets, exact roots frozen,
    # original vertices retained for invalid edges. No step leaves its grid edge.
    lo=p0.copy();hi=p1.copy();flo=d0-THRESHOLD;fhi=d1-THRESHOLD
    live=valid.copy();trace=[]
    root=np.zeros_like(lo);root_found=np.zeros(len(v),bool)
    for endpoint,density in [(p0,d0),(p1,d1)]:
        exact=valid&(density==THRESHOLD)
        root[exact]=endpoint[exact];root_found|=exact;live&=~exact
    refinement_started=time.monotonic()
    for iteration in range(ITERATIONS):
        ids=np.flatnonzero(live)
        mid=(lo[ids]+hi[ids])*.5
        density,_=query(renderer,decoder,latent,mid)
        assert np.isfinite(density).all(), 'Nonfinite midpoint field value'
        fm=density-THRESHOLD
        exact=fm==0
        root[ids[exact]]=mid[exact];root_found[ids[exact]]=True;live[ids[exact]]=False
        take_lower=(np.signbit(flo[ids])==np.signbit(fm))&~exact
        take_upper=~take_lower&~exact
        lo[ids[take_lower]]=mid[take_lower];flo[ids[take_lower]]=fm[take_lower]
        hi[ids[take_upper]]=mid[take_upper];fhi[ids[take_upper]]=fm[take_upper]
        trace.append({'iteration':iteration+1,'evaluated':len(ids),
            'max_abs_density_residual':float(np.max(np.abs(fm))) if len(ids) else 0})
    refined_v=v.copy()
    refined_v[live]=(lo[live].astype(np.float64)+hi[live].astype(np.float64))*.5
    refined_v[root_found]=root[root_found]
    # Exported float32 coordinates are the coordinates used for final RGB/query.
    refined_v=refined_v.astype(np.float32).astype(np.float64)
    dr,cr=query(renderer,decoder,latent,refined_v)
    refinement_seconds=time.monotonic()-refinement_started
    refined=trimesh.Trimesh(vertices=refined_v,faces=f.copy(),vertex_colors=np.round(np.clip(cr,0,1)*255).astype(np.uint8),process=False)
    refined.export(out/'refined.glb')
    # Explicit control uses exact original coordinates and exported original RGB.
    raw.export(out/'original_control.glb')
    disp=np.linalg.norm(refined_v-v,axis=1)
    geometry,flips=geometry_report(raw,refined)
    report.update(refined_density=summary(dr),refined_density_abs_residual=summary(np.abs(dr-THRESHOLD)),
        displacement=summary(disp),displacement_fraction_cell_width=summary(disp/(2*radius/(RESOLUTION-1))),
        original_refreshed_vertex_rgb_abs_difference=summary(np.abs(cr-craw)),
        refinement_query_and_rgb_seconds=refinement_seconds,geometry=geometry,bisection_trace=trace,
        post_bisection_max_bracket_width=float(np.max(np.linalg.norm(hi[live]-lo[live],axis=1))) if live.any() else 0,
        refinement_and_export_elapsed_seconds=time.monotonic()-started)
    np.savez_compressed(out/'edge_refinement.npz',original_vertices=v,refined_vertices=refined_v,faces=f,
        original_rgb=original_rgb,original_queried_rgb=craw,refined_rgb=cr,
        edge_lo_index=lo_index,edge_hi_index=hi_index,edge_start=p0,edge_end=p1,
        density_start=d0,density_end=d1,original_density=draw,refined_density=dr,
        valid=valid,axis=axis,original_t=t,displacement=disp,flipped_faces=flips)
    (out/'refinement.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'stage':'refined','case':name,'valid_fraction':float(valid.mean()),
        'raw_residual_mean':report['original_density_abs_residual']['mean'],
        'refined_residual_mean':report['refined_density_abs_residual']['mean'],
        'displacement_mean':float(disp.mean()),'flips':geometry['negative_original_refined_normal_dot_count'],
        'elapsed_seconds':time.monotonic()-started}),flush=True)
    return out,raw,refined,report

def image_metrics(a,b,mask):
    e=np.abs(a[mask]-b[mask])
    return {'MAE':float(e.mean()),'RMSE':float(np.sqrt(np.mean(e**2))),
        'max_abs_difference':float(e.max()),'pixels':int(mask.sum())}

def clay(rgb,depth,normal,az):
    mask=np.isfinite(depth)
    shade=.25+.7*np.abs(normal@(-camera(az)[3]))
    out=np.ones_like(rgb);out[mask]=shade[mask,None]*.7
    return out

def render_views(out,raw,refined,report,decoder,renderer,latent):
    rays_o,rays_d=get_spherical_cameras(6,20,1.9,40,PIXELS,PIXELS)
    rows={k:[] for k in ['Native field','Original mesh RGB','Refined mesh RGB','RGB difference x10','Original geometry','Refined geometry']}
    comparisons={}
    for i,az in enumerate(VIEWS):
        started=time.monotonic()
        ro,rd=rays_o[i].reshape(-1,3),rays_d[i].reshape(-1,3)
        chunks=[]
        with torch.no_grad():
            for start in range(0,len(ro),1024):
                chunks.append(renderer(decoder,latent,ro[start:start+1024],rd[start:start+1024]))
        native=torch.cat(chunks).reshape(PIXELS,PIXELS,3).numpy()
        renders=[]
        for name,mesh in [('original',raw),('refined',refined)]:
            rgb,depth,normal=raster(np.asarray(mesh.vertices),mesh.faces,mesh.visual.vertex_colors[:,:3].astype(np.float64)/255,*camera(az,size=PIXELS))
            shaded=clay(rgb,depth,normal,az)
            save_rgb(out/f'{name}_rgb_az{az:03}.png',rgb)
            save_rgb(out/f'{name}_clay_az{az:03}.png',shaded)
            renders.append((rgb,depth,normal,shaded))
            # High-resolution geometry-only view to expose small corrugation.
            hrgb,hdepth,hnorm=raster(np.asarray(mesh.vertices),mesh.faces,np.full((len(mesh.vertices),3),.7),*camera(az,size=480))
            save_rgb(out/f'{name}_clay480_az{az:03}.png',clay(hrgb,hdepth,hnorm,az))
        (a,da,na,ca),(b,db,nb,cb)=renders
        ma,mb=np.isfinite(da),np.isfinite(db);intersect=ma&mb;union=ma|mb
        all_pixels=np.ones(ma.shape,bool)
        m={'original_vs_native_full':image_metrics(a,native,all_pixels),
            'refined_vs_native_full':image_metrics(b,native,all_pixels),
            'original_vs_native_common_mask':image_metrics(a,native,intersect),
            'refined_vs_native_common_mask':image_metrics(b,native,intersect),
            'raw_vs_refined_full':image_metrics(a,b,all_pixels),
            'raw_vs_refined_common_mask':image_metrics(a,b,intersect),
            'clay_raw_vs_refined_common_mask':image_metrics(ca,cb,intersect),
            'depth_raw_vs_refined_common_mask':finite_summary(np.abs(da[intersect]-db[intersect])),
            'normal_raw_vs_refined_common_mask_degrees':summary(np.rad2deg(np.arccos(np.clip(np.einsum('ij,ij->i',na[intersect],nb[intersect]),-1,1)))),
            'silhouette_IoU':float(intersect.sum()/union.sum()),
            'silhouette_changed_pixels':int((ma^mb).sum()),
            'rgb_changed_pixels_gt_1_over_255':int((np.max(np.abs(a-b),axis=2)>1/255).sum()),
            'rgb_changed_pixels_gt_5_over_255':int((np.max(np.abs(a-b),axis=2)>5/255).sum()),
            'rgb_changed_pixels_gt_10_over_255':int((np.max(np.abs(a-b),axis=2)>10/255).sum()),
            'original_mask_pixels':int(ma.sum()),'refined_mask_pixels':int(mb.sum())}
        m['native_common_mask_MAE_relative_change']=(m['refined_vs_native_common_mask']['MAE']/m['original_vs_native_common_mask']['MAE']-1)
        save_rgb(out/f'native_az{az:03}.png',native)
        save_rgb(out/f'difference_x10_az{az:03}.png',np.abs(a-b)*10)
        np.savez_compressed(out/f'render_arrays_az{az:03}.npz',native=native,original_rgb=a,refined_rgb=b,original_depth=da,refined_depth=db,original_normals=na,refined_normals=nb)
        for key,img in zip(rows,[native,a,b,np.abs(a-b)*10,ca,cb]):rows[key].append(img)
        comparisons[f'az{az:03}']=m
        print(json.dumps({'stage':'view','case':report['name'],'azimuth':az,
            'original_native_mae':m['original_vs_native_common_mask']['MAE'],
            'refined_native_mae':m['refined_vs_native_common_mask']['MAE'],
            'raw_refined_mae':m['raw_vs_refined_common_mask']['MAE'],'elapsed_seconds':time.monotonic()-started}),flush=True)
    tile=240;label=185;header=30
    sheet=Image.new('RGB',(label+tile*len(VIEWS),header+tile*len(rows)),'white');draw=ImageDraw.Draw(sheet)
    for i,az in enumerate(VIEWS):draw.text((label+tile*i+75,8),f'azimuth {az}',fill='black')
    for j,(key,images) in enumerate(rows.items()):
        draw.text((8,header+j*tile+100),key,fill='black')
        for i,img in enumerate(images):
            im=Image.fromarray(np.round(np.clip(img,0,1)*255).astype(np.uint8)).resize((tile,tile))
            sheet.paste(im,(label+i*tile,header+j*tile))
    sheet.save(out/'comparison.png')
    report['views']=comparisons
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')

def main():
    started=time.monotonic()
    decoder,renderer,car_latent=load_field()
    cases=[('car',ROOT/'raw/car_raw.glb',ROOT/'raw/cpu-attempt001/scene_codes.pt')]
    for name in ('teapot','hamburger'):
        base=OUT.parent/'root_analysis/holdouts'/name
        cases.append((name,base/'raw.glb',base/'scene_codes.pt'))
    report={'encoder_inference_calls':0,'dense_grid_queries':0,'cpu_threads':2,
        'cpu_affinity':sorted(os.sched_getaffinity(0)),'resolution512_reference_run':False,
        'method':'Ten standard safeguarded per-edge bisections then final midpoint query; original faces, radius and threshold. Refreshed vertex RGB quantized to uint8 exactly as original exporter.',
        'camera':{'azimuths':VIEWS,'elevation':20,'distance':1.9,'fovy':40,'pixels':PIXELS,'clay_detail_pixels':480},
        'interpretation_limit':'Native volume rendering is a matched field comparator, not ground truth. Density residual alone is not a research outcome. Clay highlights changes in triangle normals but supplies no geometry ground truth.',
        'cases':{}}
    for name,mesh_path,latent_path in cases:
        latent=car_latent if name=='car' else torch.load(latent_path,map_location='cpu',weights_only=True)[0]
        out,raw,refined,r=refine(name,mesh_path,latent_path,decoder,renderer,latent)
        render_views(out,raw,refined,r,decoder,renderer,latent)
        report['cases'][name]=r
        (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    report['elapsed_seconds']=time.monotonic()-started
    (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'stage':'done','elapsed_seconds':report['elapsed_seconds']}),flush=True)

if __name__=='__main__':
    main()
