import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {openRenderer} from '../scripts/browser';
test('thyroid composition: arbitrary seeks repeat across fresh browser sessions',async()=>{
 const p=JSON.parse(await readFile('projects/voice-quality/project.json','utf8'));
 const times=[.8,3.96,5.2,6.9,10.26,11.7];const hashes:Record<string,string[]>={};
 for(let session=0;session<2;session++){
  const r=await openRenderer(p,1080,1920);
  try{for(const t of [...times,0,...times.slice().reverse()]){
   await r.page.evaluate(t=>window.seek(t),t);
   if(times.includes(t))(hashes[t]??=[]).push(createHash('sha256').update(await r.page.screenshot()).digest('hex'));
  }}finally{await r.close();}
 }
 for(const values of Object.values(hashes))assert.equal(new Set(values).size,1);
 await mkdir('reviews/voice-quality-tests',{recursive:true});
 await writeFile('reviews/voice-quality-tests/determinism.json',JSON.stringify({resolution:[1080,1920],hashes,pass:true},null,2));
});
