#!/usr/bin/env python3
"""Optional short deterministic accents; never music or invented narration."""
import argparse,json,wave,math,struct,pathlib
p=argparse.ArgumentParser();p.add_argument('--project',required=True);p.add_argument('--output',default='assets/audio/technical-sfx.wav');a=p.parse_args();cfg=json.load(open(a.project));rate=48000;x=[0.0]*round(cfg['duration']*rate)
for cue in cfg['accents']:
 offset=round(cue['time']*rate)
 for i in range(round(.08*rate)):
  if offset+i<len(x):
   t=i/rate;env=math.exp(-t*65)*min(1,t/.002);x[offset+i]+=.13*env*math.sin(2*math.pi*(1000*t-4000*t*t))
pathlib.Path(a.output).parent.mkdir(parents=True,exist_ok=True)
with wave.open(a.output,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,v))*32767)) for v in x))
print(a.output)
