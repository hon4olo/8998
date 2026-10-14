#!/usr/bin/env python3
"""Mechanical quality gate; aesthetic/semantic acceptance always needs reviewed evidence."""
import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('review');p.add_argument('--require-visual',action='store_true');a=p.parse_args();root=pathlib.Path(a.review);r=json.load(open(root/'automated-checks.json'));problems=[]
if not r['nonblank']:problems.append('blank image evidence')
if not r['readabilityHeuristicPass']:problems.append('declared phone text too small')
if r.get('titleSubtitleOverlapTimes'):problems.append('title/subtitle overlap')
if r.get('titleHorizontalOverflowTimes'):problems.append('title overflow')
if not r.get('determinism',{}).get('pass'):problems.append('no successful determinism evidence')
if r['sync'].get('passed') is False:problems.append('audio clock/cue check failed')
if r['loop']['required'] and r['loop']['status']!='candidate pass':problems.append('loop discontinuity')
if a.require_visual:
 critique=root/'visual-critique.json'
 if not critique.exists():problems.append('actual visual review missing')
 else:
  v=json.load(open(critique));
  if not v.get('inspectedFiles'):problems.append('visual evidence not inspected')
  if not v.get('independentAcceptance'):problems.append('independent acceptance missing; model score alone cannot certify ≥8')
  if any(x is None or x<8 for x in v.get('scores',{}).values()):problems.append('unassessed criterion or score below 8')
print(json.dumps({'mechanicalPass':not problems,'problems':problems,'scope':'This gate cannot measure hook quality or scientific/narration fidelity.'},indent=2));raise SystemExit(bool(problems))
