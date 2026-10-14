#!/usr/bin/env python3
import subprocess,json,pathlib,platform,os
commands={'os':['cat','/etc/os-release'],'architecture':['uname','-m'],'glibc':['getconf','GNU_LIBC_VERSION'],'cpu':['lscpu'],'affinityCPU':['nproc'],'cpuQuota':['cat','/sys/fs/cgroup/cpu.max'],'memoryQuota':['cat','/sys/fs/cgroup/memory.max'],'memory':['free','-h'],'node':['node','--version'],'python':['python3','--version'],'ffmpeg':['ffmpeg','-version'],'encoders':['ffmpeg','-hide_banner','-encoders'],'gpuDevices':['sh','-c','ls -l /dev/dri /dev/nvidia* 2>/dev/null'],'github':['curl','-I','https://github.com'],'npm':['curl','-I','https://registry.npmjs.org'],'pypi':['curl','-I','https://pypi.org']}
report={}
for name,cmd in commands.items():
 p=subprocess.run(cmd,capture_output=True,text=True);text=p.stdout+p.stderr
 if name=='encoders':text='\n'.join(l for l in text.splitlines() if 'libx264' in l or ' aac ' in l)
 report[name]={'exitCode':p.returncode,'output':text}
pathlib.Path('docs/environment_raw.json').write_text(json.dumps(report,indent=2))
pathlib.Path('docs/environment_report.md').write_text('# Measured cloud environment\n\n'+ '\n\n'.join(f'## {k}\n\n```text\n{v["output"]}\n```\nexit={v["exitCode"]}' for k,v in report.items())+'\n\nNo hardware GPU exposed. Browser Canvas uses CPU; Tesseract uses Vulkan Mesa lavapipe (CPU). See reviews/*benchmark.json for measured process-tree memory and CPU. Native runtime and browser caches are ephemeral; run scripts/setup.sh in a new instance.\n')
