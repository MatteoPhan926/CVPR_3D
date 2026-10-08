"""Controlled rendering/extraction of existing latent, no new car generation.

Axes: original256 threshold25; same256 thresholds10/50; resolution128
threshold25. Flat image values are direct decoder/vertex numeric RGB, not PBR.
"""
import os
os.environ['OMP_NUM_THREADS']='2'
os.environ['MKL_NUM_THREADS']='2'
os.environ['NUMBA_NUM_THREADS']='2'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import json, time, math
import numpy as np
import torch
import trimesh
from PIL import Image,ImageDraw
from numba import njit
from scipy.spatial import cKDTree
from provenance_check import ROOT,OUT,load_field,summary
from tsr.models.isosurface import MarchingCubeHelper
from tsr.utils import get_spherical_cameras

@njit
def raster(verts,faces,colors,cam,right,up,look,size,focal):
    rgb=np.ones((size,size,3),np.float32)
    depth=np.full((size,size),np.inf,np.float32)
    normal=np.zeros((size,size,3),np.float32)
    p=(verts-cam)@np.stack((right,up,look)).T
    xy=np.empty((len(verts),2),np.float64)
    xy[:,0]=p[:,0]/p[:,2]*focal+size/2
    xy[:,1]=-p[:,1]/p[:,2]*focal+size/2
    for f in faces:
        a,b,c=f
        if min(p[a,2],p[b,2],p[c,2])<=0:continue
        x0,y0=xy[a];x1,y1=xy[b];x2,y2=xy[c]
        xmin=max(0,int(math.floor(min(x0,x1,x2))))
        xmax=min(size-1,int(math.ceil(max(x0,x1,x2))))
        ymin=max(0,int(math.floor(min(y0,y1,y2))))
        ymax=min(size-1,int(math.ceil(max(y0,y1,y2))))
        det=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
        if abs(det)<1e-15:continue
        n=np.cross(verts[b]-verts[a],verts[c]-verts[a]);n=n/(np.linalg.norm(n)+1e-20)
        for yy in range(ymin,ymax+1):
            for xx in range(xmin,xmax+1):
                x=xx+.5;y=yy+.5
                u=((y1-y2)*(x-x2)+(x2-x1)*(y-y2))/det
                v=((y2-y0)*(x-x2)+(x0-x2)*(y-y2))/det
                w=1-u-v
                if min(u,v,w)<-1e-10:continue
                invz=u/p[a,2]+v/p[b,2]+w/p[c,2]
                z=1/invz
                if z>=depth[yy,xx]:continue
                depth[yy,xx]=z
                rgb[yy,xx]=(u*colors[a]/p[a,2]+v*colors[b]/p[b,2]+w*colors[c]/p[c,2])*z
                normal[yy,xx]=n
    return rgb,depth,normal

def save_rgb(name,rgb):
    Image.fromarray(np.round(np.clip(rgb,0,1)*255).astype(np.uint8)).save(OUT/name)

def camera(az,elev=20,distance=1.9,size=160,fov=40):
    az,elev=np.deg2rad([az,elev])
    cam=distance*np.array([np.cos(elev)*np.cos(az),np.cos(elev)*np.sin(az),np.sin(elev)])
    look=-cam/np.linalg.norm(cam);right=np.cross(look,[0,0,1]);right/=np.linalg.norm(right)
    up=np.cross(right,look)
    return cam,right,up,look,size,.5*size/np.tan(np.deg2rad(fov)/2)

def field_grid(renderer,decoder,latent,resolution):
    path=OUT/f'density_grid_{resolution}.npy'
    if path.exists():return np.load(path)
    radius=renderer.cfg.radius
    # Match upstream linspace(0,1), then scale_tensor arithmetic exactly.
    coords=torch.linspace(0,1,resolution)*(2*radius)-radius
    density=np.empty((resolution,resolution,resolution),np.float32)
    for start in range(0,resolution,8):
        points=torch.stack(torch.meshgrid(coords[start:start+8],coords,coords,indexing='ij'),dim=-1).reshape(-1,3)
        with torch.no_grad():q=renderer.query_triplane(decoder,points,latent)
        density[start:start+8]=q['density_act'].numpy().reshape(-1,resolution,resolution)
    np.save(path,density)
    return density

def extract(renderer,decoder,latent,grid,resolution,threshold):
    helper=MarchingCubeHelper(resolution)
    with torch.no_grad():
        v,f=helper(-(torch.from_numpy(grid)-threshold))
        v=v*2*renderer.cfg.radius-renderer.cfg.radius
        q=renderer.query_triplane(decoder,v,latent)
    colors=q['color'].numpy()
    # Match upstream trimesh constructor, including its default processing.
    mesh=trimesh.Trimesh(vertices=v.numpy(),faces=f.numpy(),vertex_colors=colors)
    key=f'r{resolution}_t{threshold}'
    mesh.export(OUT/f'{key}.glb')
    queried_density=renderer.query_triplane(decoder,torch.tensor(mesh.vertices,dtype=torch.float32),latent)['density_act'].detach().numpy()
    # Count graph components without Trimesh.split's default hole repair.
    components=trimesh.graph.connected_components(mesh.face_adjacency,nodes=np.arange(len(mesh.faces)),min_len=1)
    metrics={'vertices':len(mesh.vertices),'faces':len(mesh.faces),'area':float(mesh.area),
             'signed_volume':float(mesh.volume),'body_count':int(mesh.body_count),
             'euler_number':int(mesh.euler_number),'watertight':bool(mesh.is_watertight),
             'bounds':mesh.bounds.tolist(),'component_faces_desc':sorted([len(c) for c in components],reverse=True),
             'density_at_vertices':summary(queried_density)}
    return key,mesh,metrics

def main():
    started=time.monotonic()
    decoder,renderer,latent=load_field()
    report={'encoder_inference_calls':0,'threads':2,'fixed_cameras':{'azimuths':[0,60,120,180,240,300],'elevation':20,'distance':1.9,'fovy':40,'pixels':160},'meshes':{},'comparisons':{}}
    raw=trimesh.load(ROOT/'raw/car_raw.glb',force='mesh',process=False)
    variants={'original_r256_t25':raw}
    for resolution in [256,128]:
        grid=field_grid(renderer,decoder,latent,resolution)
        print(json.dumps({'stage':'grid_finished','resolution':resolution,'elapsed':time.monotonic()-started}),flush=True)
        for threshold in ([10,25,50] if resolution==256 else [25]):
            key,mesh,metrics=extract(renderer,decoder,latent,grid,resolution,threshold)
            variants[key]=mesh;report['meshes'][key]=metrics
            print(json.dumps({'stage':'extraction_finished','variant':key,'elapsed':time.monotonic()-started}),flush=True)
    reproduced=variants['r256_t25']
    report['reproduction_array_order_only']={
        'vertices_exact':bool(np.array_equal(reproduced.vertices,raw.vertices)),
        'faces_exact':bool(np.array_equal(reproduced.faces,raw.faces)),
        'colors_exact':bool(np.array_equal(reproduced.visual.vertex_colors,raw.visual.vertex_colors)),
        'max_vertex_abs_error':float(np.max(np.abs(reproduced.vertices-raw.vertices))) if reproduced.vertices.shape==raw.vertices.shape else None,
    }
    distances,mapping=cKDTree(raw.vertices).query(reproduced.vertices)
    report['reproduction_order_invariant']={
        'vertex_nearest_distance':summary(distances),
        'bijective_nearest_vertex_mapping':len(set(mapping.tolist()))==len(raw.vertices),
        'triangle_sets_equal_under_mapping':{tuple(sorted(f)) for f in raw.faces}=={tuple(sorted(f)) for f in mapping[reproduced.faces]},
        'corresponding_rgb_exact_fraction':float(np.mean(np.all(reproduced.visual.vertex_colors==raw.visual.vertex_colors[mapping],axis=1))),
    }
    # Ray chunks bound live positions and MLP outputs for volume rendering.
    rays_o,rays_d=get_spherical_cameras(6,20,1.9,40,160,160)
    row_names=['native_field','original_r256_t25','linear_rgb_display','clay_original','r256_t10','r256_t50','r128_t25']
    native_images=[]
    comparison_rows={name:[] for name in row_names}
    for i,az in enumerate([0,60,120,180,240,300]):
        ro,rd=rays_o[i].reshape(-1,3),rays_d[i].reshape(-1,3)
        rendered=[]
        with torch.no_grad():
            for start in range(0,len(ro),1024):
                rendered.append(renderer(decoder,latent,ro[start:start+1024],rd[start:start+1024]))
        native=torch.cat(rendered).reshape(160,160,3).numpy()
        save_rgb(f'native_field_az{az:03}.png',native)
        comparison_rows['native_field'].append(native)
        rawrgb=None;rawmask=None
        for key in ['original_r256_t25','r256_t10','r256_t50','r128_t25']:
            mesh=variants[key]
            rgb,depth,normal=raster(np.asarray(mesh.vertices).astype(np.float64),np.asarray(mesh.faces),np.asarray(mesh.visual.vertex_colors)[:,:3].astype(np.float64)/255,*camera(az))
            save_rgb(f'{key}_flat_az{az:03}.png',rgb)
            comparison_rows[key].append(rgb)
            mask=np.isfinite(depth)
            if key=='original_r256_t25':
                rawrgb,rawmask=rgb,mask
                srgb=np.where(rgb<=.0031308,12.92*rgb,1.055*np.power(rgb,1/2.4)-.055)
                comparison_rows['linear_rgb_display'].append(srgb)
                save_rgb(f'linear_rgb_display_az{az:03}.png',srgb)
                # Symmetric neutral directional normal shading, no RGB or PBR.
                cam_dir=-camera(az)[3]
                shade=.25+.7*np.abs(normal@cam_dir)
                clay=np.ones_like(rgb);clay[mask]=shade[mask,None]*np.array([.7,.7,.7])
                comparison_rows['clay_original'].append(clay)
                save_rgb(f'clay_original_az{az:03}.png',clay)
                report['comparisons'][f'az{az:03}']={'flat_vs_native_MAE_on_mesh_mask':float(np.mean(np.abs(rgb[mask]-native[mask]))),'mesh_mask_pixels':int(mask.sum()),'native_mean_rgb_on_mesh_mask':native[mask].mean(axis=0).tolist(),'mesh_mean_rgb_on_mask':rgb[mask].mean(axis=0).tolist(),'linear_vertex_to_srgb_mean_rgb_on_mask':srgb[mask].mean(axis=0).tolist()}
            else:
                intersect=mask&rawmask;union=mask|rawmask
                report['comparisons'][f'az{az:03}'][key]={'silhouette_IoU_vs_original':float(intersect.sum()/union.sum()),'flat_rgb_MAE_intersection':float(np.mean(np.abs(rgb[intersect]-rawrgb[intersect]))),'depth_MAE_intersection':float(np.mean(np.abs(depth[intersect]-rawdepth[intersect])))}
            if key=='original_r256_t25':rawdepth=depth
        print(json.dumps({'stage':'view_finished','azimuth':az,'elapsed':time.monotonic()-started}),flush=True)
    labelwidth=200;tile=240;header=35
    sheet=Image.new('RGB',(labelwidth+6*tile,header+len(row_names)*tile),'white')
    d=ImageDraw.Draw(sheet)
    for i,az in enumerate([0,60,120,180,240,300]):d.text((labelwidth+i*tile+80,10),f'azimuth {az}',fill='black')
    labels={'native_field':'Saved field volume RGB','original_r256_t25':'Original mesh direct RGB','linear_rgb_display':'Same RGB linear -> sRGB','clay_original':'Original geometry, clay','r256_t10':'Same 256 grid; threshold10','r256_t50':'Same 256 grid; threshold50','r128_t25':'128 grid; threshold25'}
    for j,name in enumerate(row_names):
        d.text((8,header+j*tile+90),labels[name],fill='black')
        for i,rgb in enumerate(comparison_rows[name]):
            im=Image.fromarray(np.round(np.clip(rgb,0,1)*255).astype(np.uint8)).resize((tile,tile))
            sheet.paste(im,(labelwidth+i*tile,header+j*tile))
    sheet.save(OUT/'controlled_comparison.png')
    report['elapsed_seconds']=time.monotonic()-started
    (OUT/'field_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'stage':'done','elapsed':report['elapsed_seconds'],'reproduction':report['reproduction_order_invariant']}),flush=True)

if __name__=='__main__':main()
