#!/usr/bin/env python3
"""Keep original speech timing and video, add an optional pre-timed accent track; never music."""
import argparse,subprocess,json
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('sfx');p.add_argument('--output',required=True);p.add_argument('--gain',type=float,default=.3);a=p.parse_args()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',a.video]));dur=probe['format']['duration'];has=any(s['codec_type']=='audio' for s in probe['streams']);args=['ffmpeg','-y','-v','error','-i',a.video,'-i',a.sfx]
if has:args+=['-filter_complex',f'[1:a]volume={a.gain}[s];[0:a][s]amix=inputs=2:duration=first:normalize=0[a]','-map','0:v','-map','[a]']
else:args+=['-map','0:v','-map','1:a','-af',f'volume={a.gain}']
args+=['-c:v','copy','-c:a','aac','-b:a','192k','-t',dur,'-movflags','+faststart',a.output];subprocess.run(args,check=True);print(a.output)
