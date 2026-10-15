import {readFile,mkdir} from 'node:fs/promises';
import {openRenderer} from './browser';
const p=JSON.parse(await readFile('projects/voice-quality/project.json','utf8'));
const r=await openRenderer(p,1080,1920);
const dir='reviews/thyroid-reveal-fix';await mkdir(dir,{recursive:true});
try{for(const t of [4.8,4.9,5,5.1,5.2,5.3,5.4,5.5,5.6]){await r.page.evaluate(t=>window.seek(t),t);await r.page.screenshot({path:`${dir}/${t.toFixed(1)}.png`});}}finally{await r.close();}
