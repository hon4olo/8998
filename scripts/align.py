#!/usr/bin/env python3
"""Adapter ABI: external executable receives audio/transcript/output flags; never an obligatory API."""
import argparse,json,subprocess,pathlib
p=argparse.ArgumentParser();p.add_argument('--audio',required=True);p.add_argument('--transcript',required=True);p.add_argument('--output',required=True);p.add_argument('--command');p.add_argument('--manual');a=p.parse_args()
if a.manual:words=json.load(open(a.manual))
elif a.command:
 subprocess.run([a.command,'--audio',a.audio,'--transcript',a.transcript,'--output',a.output],check=True);words=json.load(open(a.output))
else:raise SystemExit('No aligner installed. Supply --manual words.json; speech timings will not be inferred from energy.')
previous=0
for w in words:
 assert isinstance(w['word'],str) and previous<=w['start']<=w['end'];previous=w['end']
pathlib.Path(a.output).write_text(json.dumps(words,indent=2));print(a.output)
