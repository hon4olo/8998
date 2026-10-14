#!/usr/bin/env python3
"""Linux /proc process-tree sampler including Chromium and FFmpeg, 100 ms interval."""
import argparse,subprocess,time,pathlib,json,os
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args();cmd=a.command[1:] if a.command[:1]==['--'] else a.command
begin=time.monotonic();proc=subprocess.Popen(cmd);peak=0;cpu=0;records={};samples=0;hz=os.sysconf('SC_CLK_TCK')
while True:
 entries={}
 for path in pathlib.Path('/proc').glob('[0-9]*/stat'):
  try:
   raw=path.read_text();pid=int(path.parent.name);parts=raw[raw.rfind(')')+2:].split();entries[pid]=(int(parts[1]),int(parts[11])+int(parts[12]),int(parts[21])*os.sysconf('SC_PAGE_SIZE'))
  except (OSError,ValueError,IndexError):continue
 descendants={proc.pid};changed=True
 while changed:
  old=len(descendants);descendants.update(pid for pid,(ppid,_,_) in entries.items() if ppid in descendants);changed=len(descendants)!=old
 rss=0
 for pid in descendants:
  if pid in entries:ppid,ticks,mem=entries[pid];records[pid]=max(records.get(pid,0),ticks);rss+=mem
 peak=max(peak,rss);cpu=sum(records.values())/hz;samples+=1
 if proc.poll() is not None:break
 time.sleep(.1)
data={'command':cmd,'exitCode':proc.returncode,'wallSeconds':time.monotonic()-begin,'sampledProcessTreeCpuSeconds':cpu,'peakProcessTreeRSSMiB':peak/1048576,'samples':samples,'gpu':False,'method':'/proc 100ms; summed RSS may double-count shared pages; short-lived children CPU may be missed'}
pathlib.Path(a.out).parent.mkdir(parents=True,exist_ok=True);pathlib.Path(a.out).write_text(json.dumps(data,indent=2));print(json.dumps(data));raise SystemExit(proc.returncode)
