import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import d from '../projects/voice-quality/assets/structures/geometry.json';
test('retained official coordinate sources match provenance SHA256',async()=>{
 for(const [file,hash] of Object.entries(d.source.sha256))assert.equal(createHash('sha256').update(await readFile('projects/voice-quality/assets/structures/'+file)).digest('hex'),hash);
});
test('T4 to T3 retains chemical graph after outer ring iodine removal',()=>{
 assert.equal(d.t3.atoms.length,23);assert.equal(d.t4.atoms.length,24);
 assert.equal(d.t3.atoms.filter(a=>a.e==='I').length,3);assert.equal(d.t4.atoms.filter(a=>a.e==='I').length,4);
 const edges=(b:string[][])=>b.map(([a,b,order])=>[...[a,b].sort(),order].join(':')).sort();
 assert.deepEqual(edges(d.t4.bonds.filter(([a,b])=>a!=="I5'"&&b!=="I5'")),edges(d.t3.bonds));
});
test('rendered receptor trace is the deposited 2H77 CA geometry up to rigid transform',async()=>{
 const pdb=await readFile('projects/voice-quality/assets/structures/2H77.pdb','utf8');
 const ca=pdb.split('\n').filter(l=>/^(ATOM  |HETATM)/.test(l)&&l[21]==='A'&&[' ','A'].includes(l[16])&&l.slice(12,16).trim()==='CA'&&l.slice(17,20).trim()!=='T3').map(l=>({res:Number(l.slice(22,26)),p:[Number(l.slice(30,38)),Number(l.slice(38,46)),Number(l.slice(46,54))]}));
 assert.equal(d.backbone.length,255);assert.equal(ca.length,255);
 for(let i=1;i<ca.length;i++){
  assert.equal(ca[i].res,d.backbone[i].res);
  const distance=(a:number[],b:number[])=>Math.hypot(...a.map((x,k)=>x-b[k]));
  for(let j=0;j<i;j++)assert.ok(Math.abs(distance(ca[i].p,ca[j].p)-distance(d.backbone[i].p,d.backbone[j].p))<.00003);
 }
});
