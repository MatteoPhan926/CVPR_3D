"""Quantify paired diagnostic renders and assemble scientific contact sheets."""
from pathlib import Path
import json, hashlib, numpy as np
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parents[1]
design=json.loads((OUT/'measurements/design.json').read_text())
variants=[v[0] for v in design['variants']]
images={}
for path in sorted((OUT/'renders').glob('*.png')):
    images[path.stem]=np.asarray(Image.open(path).convert('RGBA'),float)/255
def metrics(a,b):
    both=(a[...,3]>.98)&(b[...,3]>.98)
    amask=a[...,3]>.5;bmask=b[...,3]>.5
    delta=np.abs(a[...,:3]-b[...,:3])
    lum=np.array([.2126,.7152,.0722])
    return {'common_opaque_pixels':int(both.sum()),'RGB_MAE_display_0_1':float(delta[both].mean()),
      'RGB_RMSE_display_0_1':float(np.sqrt((delta[both]**2).mean())),
      'fraction_common_pixels_max_channel_difference_over_0.03':float((delta.max(2)[both]>.03).mean()),
      'mean_luma_a':float((a[...,:3]@lum)[both].mean()),'mean_luma_b':float((b[...,:3]@lum)[both].mean()),
      'silhouette_IoU':float((amask&bmask).sum()/max(1,(amask|bmask).sum())),
      'silhouette_xor_pixels':int((amask^bmask).sum())}
pairs=[('A','B','sidedness'),('B','C','raw_normals'),('B','D','prior_display_material'),
 ('B','E','flat_partition'),('C','F','smooth_partition'),('F','G','closed_additions'),
 ('I','H','open_additions'),('A','G','complete_closed_pipeline')]
result={'metric_space':'PNG display-encoded RGB, 0..1; common alpha>.98 foreground. Luma is display luma, not radiometric luminance.',
 'caution':'24-sample stochastic Cycles render, identical seed, no denoising; small differences include sampling and quantization, not a perceptual quality score.',
 'pairs':{}}
for aa,bb,label in pairs:
    a=next(v for v in variants if v.startswith(aa+'_'));b=next(v for v in variants if v.startswith(bb+'_'))
    result['pairs'][label]={view:metrics(images[a+'_'+view],images[b+'_'+view]) for view in design['views']}
(OUT/'measurements/pixel_metrics.json').write_text(json.dumps(result,indent=2)+'\n')

fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontpath,19)
small=ImageFont.truetype(fontpath,16)
def tile(stem,title):
    ar=images[stem];alpha=ar[...,3:4];rgb=ar[...,:3]*alpha+.76*(1-alpha)
    im=Image.fromarray(np.uint8(np.clip(rgb*255,0,255)))
    panel=Image.new('RGB',(720,522),'white');panel.paste(im,(0,42))
    ImageDraw.Draw(panel).text((12,11),title,font=font,fill='black');return panel
def sheet(filename,rows,heading):
    canvas=Image.new('RGB',(1440,len(rows)*522+46),'white');draw=ImageDraw.Draw(canvas)
    draw.text((12,13),heading,font=font,fill='black')
    for row,cells in enumerate(rows):
        for col,(stem,title) in enumerate(cells):canvas.paste(tile(stem,title),(col*720,46+row*522))
    canvas.save(OUT/filename)
sheet('appearance_controls.png',[
 [('A_raw_flat_single_side','A | Raw, flat, single-sided, glTF defaults'),('B_raw_flat_double_side','B | Same raw, double-sided')],
 [('C_raw_smooth_double_side','C | Same raw, smooth normals'),('D_prior_raw_display_side','D | Prior raw-display material (M=0, R=.8)')],
 [('E_partition_flat_side','E | Partition, flat, no additions'),('F_partition_authored_normals_side','F | Partition, authored normals, no additions')],
 [('G_full_authored_closed_side','G | Full saved authored GLB, closed'),('H_full_authored_open_side','H | Full saved authored GLB, open 60°')],
], 'SAME SOURCE / CAMERA / LIGHTS | material, normals, sidedness, partition and additions')
sheet('selection_and_additions.png',[
 [('J_selection_closed_side','Actual moving selection (red), closed'),('J_selection_closed_hero','Actual moving selection (red), closed')],
 [('K_selection_open_side','Actual moving selection (red), 60°'),('K_selection_open_hero','Actual moving selection (red), 60°')],
 [('I_partition_open_no_additions_side','Open, all added geometry hidden'),('H_full_authored_open_side','Open, saved additions enabled')],
 [('I_partition_open_no_additions_hero','Open, all added geometry hidden'),('H_full_authored_open_hero','Open, saved additions enabled')],
], 'SAVED SELECTION + EXPORTED MOTION | red mask is a diagnostic, not a replacement model')
sheet('hero_controls.png',[
 [('A_raw_flat_single_hero','Raw semantic baseline'),('D_prior_raw_display_hero','Prior raw-display material')],
 [('C_raw_smooth_double_hero','Raw, smooth normals'),('F_partition_authored_normals_hero','Partition, authored normals, no additions')],
 [('G_full_authored_closed_hero','Full authored, closed'),('H_full_authored_open_hero','Full authored, open 60°')],
], 'SHARED OBLIQUE VIEW | matched rendering conditions')
# Scientific mask overlay to inspect anatomical scope against the same raw pixels.
overlay=Image.new('RGB',(1440,1088),'white')
draw=ImageDraw.Draw(overlay);draw.text((12,12),'EXACT MOVING MASK OVER RAW SOURCE | 30% red overlay; same camera, no shape edits',font=font,fill='black')
for row,view in enumerate(['side','hero']):
    base=images['D_prior_raw_display_'+view].copy()
    mask=images['J_selection_closed_'+view]
    selected=(mask[...,0]>.8)&(mask[...,1]<.4)&(mask[...,3]>.98)
    overlay.paste(tile('D_prior_raw_display_'+view,'Raw display | '+view),(0,44+row*522))
    rgb=base[...,:3].copy();rgb[selected]=.7*rgb[selected]+.3*np.array([1,0,0])
    alpha=base[...,3:4];rgb=rgb*alpha+.76*(1-alpha)
    panel=Image.new('RGB',(720,522),'white')
    panel.paste(Image.fromarray(np.uint8(np.clip(rgb*255,0,255))),(0,42))
    ImageDraw.Draw(panel).text((12,11),'Actual moving patch | '+view,font=font,fill='black')
    overlay.paste(panel,(720,44+row*522))
overlay.save(OUT/'selection_overlay.png')
hashes={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
(OUT/'SHA256SUMS.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps(result['pairs'],indent=2))
