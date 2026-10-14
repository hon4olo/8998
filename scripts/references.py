#!/usr/bin/env python3
"""Extract reference evidence and measurable palette/cuts; leave semantic analysis to actual visual review."""
import argparse,pathlib,json,subprocess,re,shutil
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('reference');p.add_argument('--out',default='reviews/references');a=p.parse_args();root=pathlib.Path(a.reference);out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
files=sorted(root.rglob('*')) if root.is_dir() else [root];report=[]
for i,f in enumerate(files):
 if not f.is_file():continue
 folder=out/f'{i:03d}-{f.stem}';folder.mkdir(exist_ok=True)
 if f.suffix.lower() in ['.mp4','.mov','.mkv','.webm']:
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(f),'-vf','fps=2,scale=360:-1',str(folder/'frame-%05d.png')],check=True)
  cuts=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf',"select='gt(scene,0.3)',showinfo",'-an','-f','null','-'],capture_output=True,text=True,check=True).stderr
  cutTimes=[float(t) for t in re.findall(r'pts_time:([\d.]+)',cuts)]
 else:
  try:Image.open(f).convert('RGB').save(folder/'frame-00001.png')
  except Exception:continue
  cutTimes=[]
 palettes=[]
 for img in sorted(folder.glob('*.png')):
  im=Image.open(img).convert('RGB').resize((100,100)).quantize(colors=5);pal=im.getpalette();colors=sorted(im.getcolors(),reverse=True);palettes.append({'frame':str(img),'colors':['#%02x%02x%02x'%tuple(pal[idx*3:idx*3+3]) for _,idx in colors]})
 report.append({'source':str(f),'frames':palettes,'candidateCuts':cutTimes,'candidateShotLengths':[b-a for a,b in zip([0]+cutTimes,cutTimes)],'copyright':'Study grammar only; no logos, characters or copied content.'})
(out/'analysis.json').write_text(json.dumps(report,indent=2))
from review import sheet
imgs=[Image.open(x).convert('RGB').resize((240,240)) for x in out.glob('*/frame-*.png')][:36]
if imgs:sheet(imgs,out/'reference-sheet.png')
for name in ['style_guide','shotlist']:
 (out/f'{name}.md').write_text(f'# {name}: reference review pending\n\nSource: {root}\n\nOpen extracted images before recording composition, type, rhythm, transitions and camera. Palette/cuts in analysis.json are measurements, not a completed semantic review. Copy reviewed conclusions to project docs/{name}.md; obtain Gate 2 approval.\n')
print(out)
