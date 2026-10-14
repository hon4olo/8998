#!/usr/bin/env python3
"""Local waveform/energy analysis. Speech timestamps are supplied, never guessed."""
import argparse,json,subprocess,struct,math,pathlib
from PIL import Image,ImageDraw

def decode(path):
 return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','1','-ar','16000','pipe:1'])
def analyze(path,output,words=None):
 raw=decode(path);x=struct.unpack('<%df'%(len(raw)//4),raw);step=320
 energy=[math.sqrt(sum(v*v for v in x[i:i+step])/len(x[i:i+step])) for i in range(0,len(x),step)]
 stamps=json.load(open(words)) if words else []
 prev=0
 for w in stamps:
  assert prev<=w['start']<=w['end']<=len(x)/16000+.02,'invalid manual word timestamps'
  prev=w['end']
 out=pathlib.Path(output);out.mkdir(parents=True,exist_ok=True)
 data={'source':str(path),'duration':len(x)/16000,'sampleRate':16000,'windowSeconds':.02,'rms':energy,'words':stamps,'alignment':'manual' if words else 'unavailable','note':'Energy peaks are candidates, not semantic word alignment.'}
 (out/'analysis.json').write_text(json.dumps(data,indent=2))
 im=Image.new('RGB',(1200,240),'#080f19');d=ImageDraw.Draw(im);peak=max(energy,default=1) or 1
 for i,e in enumerate(energy):
  px=int(i/max(len(energy),1)*1199);amp=e/peak*100;d.line((px,120-amp,px,120+amp),fill='#56d8c4')
 im.save(out/'waveform.png');return data
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('audio');p.add_argument('--out',default='reviews/audio');p.add_argument('--words');a=p.parse_args();print(json.dumps({k:v for k,v in analyze(a.audio,a.out,a.words).items() if k!='rms'}))
