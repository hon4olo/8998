#!/usr/bin/env python3
"""Mandatory evidence builder and objective checks, separate from model visual judgment."""
import argparse,json,pathlib,subprocess,math,hashlib,statistics
from PIL import Image,ImageDraw,ImageStat

def run(args):return subprocess.check_output(args)
def frame(video,t,width):
 raw=run(['ffmpeg','-v','error','-ss',f'{max(t,0):.9f}','-i',str(video),'-frames:v','1','-vf',f'scale={width}:-1','-f','image2pipe','-vcodec','png','pipe:1'])
 import io
 return Image.open(io.BytesIO(raw)).convert('RGB')
def sheet(images,path,cols=6,labels=None):
 cw,ch=images[0].size;im=Image.new('RGB',(cw*cols,(ch+24)*math.ceil(len(images)/cols)),'#111827');d=ImageDraw.Draw(im)
 for i,pic in enumerate(images):
  x=i%cols*cw;y=i//cols*(ch+24);im.paste(pic,(x,y));d.text((x+5,y+ch+4),labels[i] if labels else str(i),fill='white')
 im.save(path)
def review(video,project,directory,start=0):
 out=pathlib.Path(directory);out.mkdir(parents=True,exist_ok=True);p=json.load(open(project));probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]));dur=float(probe['format']['duration']);v=next(s for s in probe['streams'] if s['codec_type']=='video');fps=eval_rate(v['avg_frame_rate']);
 times=[i*.5 for i in range(math.ceil(dur*2)) if i*.5<dur];images=[frame(video,t,240) for t in times];sheet(images,out/'contact-sheet.png',labels=[f'{t+start:.2f}s' for t in times]);
 phones=[frame(video,t,360) for t in times];sheet(phones,out/'phone-sheet.png',3,labels=[f'{t+start:.2f}s' for t in times]);
 first=frame(video,0,360);last=frame(video,max(0,dur-1/fps),360);first.save(out/'first.png');last.save(out/'last.png');sheet([first,last],out/'endpoints.png',2,['first','last encoded frame']);
 for a in p['accents']:
  center=a['time']-start
  if 0<=center<dur:
   stamps=[max(0,min(dur-1/fps,center+(i-6)/fps)) for i in range(12)]
   sheet([frame(video,t,240) for t in stamps],out/f"transition-{a['cue']}.png",6,[f'{t+start:.3f}s' for t in stamps])
 stats=[ImageStat.Stat(im).stddev for im in images];nonblank=all(max(s)>8 for s in stats)
 sync={'status':'no supplied voiceover; not applicable','passed':None}
 if p['voiceover']:
  from audio import decode
  ref=decode(p['voiceover']);audio=decode(video);offset=int(start*16000);ref=ref[offset*4:offset*4+len(audio)]
  import struct
  n=min(len(ref),len(audio))//4;x=struct.unpack('<%df'%n,ref[:n*4]);y=struct.unpack('<%df'%n,audio[:n*4]);dot=sum(a*b for a,b in zip(x,y));den=math.sqrt(sum(a*a for a in x)*sum(b*b for b in y));corr=dot/den if den else 0
  checks=[]
  for a in p['accents']:
   if 'word' in a:
    word=next((w for w in p.get('transcript',[]) if w['word']==a['word'] and abs(w['start']-a['time'])<=.1),None);checks.append({'cue':a['cue'],'matched':bool(word)})
  sync={'status':'decoded original vs AAC, same clock/no time stretching','zeroLagCorrelation':corr,'wordCueChecks':checks,'passed':corr>.97 and all(c['matched'] for c in checks),'note':'Correlation checks timing preservation; semantic alignment requires supplied timestamps and visual/listening review.'}
 loop={'required':p['loop'],'status':'not requested'}
 if p['loop']:
  from PIL import ImageChops
  err=sum(ImageStat.Stat(ImageChops.difference(first,last)).mean)/3;loop.update({'endpointMeanAbsoluteError':err,'status':'candidate pass' if err<3 else 'needs review'})
  subprocess.run(['ffmpeg','-y','-v','error','-stream_loop','1','-i',str(video),'-c','copy',str(out/'loop-twice.mp4')],check=True)
 meta=json.load(open(out/'frames.json')) if (out/'frames.json').exists() else []
 minimum=min((m['minTextPhonePx'] for m in meta),default=None)
 overlaps=[m['time'] for m in meta if m.get('subtitleBounds') and m['titleBounds']['y']+m['titleBounds']['height']>m['subtitleBounds']['y']]
 horizontalOverflow=[m['time'] for m in meta if m['titleBounds']['x']+m['titleBounds']['width']>v['width']]
 result={'video':str(video),'duration':dur,'width':v['width'],'height':v['height'],'fps':fps,'samples':len(images),'nonblank':nonblank,'minimumDeclaredTextPhonePx':minimum,'readabilityHeuristicPass':minimum is None or minimum>=10,'titleSubtitleOverlapTimes':overlaps,'titleHorizontalOverflowTimes':horizontalOverflow,'sync':sync,'loop':loop,'determinism':json.load(open(out/'determinism.json')) if (out/'determinism.json').exists() else None,'visualReview':'pending: agent must open actual evidence; no automatic aesthetic scores'}
 (out/'automated-checks.json').write_text(json.dumps(result,indent=2));return result

def eval_rate(rate):
 a,b=rate.split('/');return float(a)/float(b)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--project',required=True);p.add_argument('--directory',required=True);p.add_argument('--start',type=float,default=0);a=p.parse_args();print(json.dumps(review(a.video,a.project,a.directory,a.start)))
