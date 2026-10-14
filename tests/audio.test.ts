import {test} from 'node:test';import assert from 'node:assert/strict';import {spawnSync} from 'node:child_process';import {readFileSync,writeFileSync} from 'node:fs';
test('supplied WAV preservation and accent timing through real AAC mux',()=>{
 const run=(cmd:string,args:string[])=>{const r=spawnSync(cmd,args,{encoding:'utf8'});assert.equal(r.status,0,r.stderr);return r.stdout;};
 run('python3',['scripts/sfx.py','--project','projects/smoke/project.json','--output','assets/audio/diagnostic-pulses.wav']);
 // Explicit test fixture: pulses are not speech and are not music.
 const p=JSON.parse(readFileSync('projects/smoke/project.json','utf8'));p.voiceover='assets/audio/diagnostic-pulses.wav';writeFileSync('out/audio-test-project.json',JSON.stringify(p));
 run('python3',['scripts/audio.py',p.voiceover,'--out','reviews/audio-fixture']);
 const audio=JSON.parse(readFileSync('reviews/audio-fixture/analysis.json','utf8'));assert.equal(audio.duration,8);const peak=audio.rms.indexOf(Math.max(...audio.rms))*.02;assert(Math.min(Math.abs(peak-2.1),Math.abs(peak-4.9))<.04);
 run(process.execPath,['--import','tsx','scripts/render.ts','--project','out/audio-test-project.json','--scale','0.25','--start','2','--end','2.5','--name','e2e-audio']);
 const checks=JSON.parse(readFileSync('reviews/e2e-audio/automated-checks.json','utf8'));assert.equal(checks.sync.passed,true);assert(checks.sync.zeroLagCorrelation>.97);
});
