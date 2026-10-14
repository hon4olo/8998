import {mkdir,writeFile,readFile,cp} from 'node:fs/promises';import {resolve,basename,relative} from 'node:path';import {spawnSync} from 'node:child_process';import type {Project} from '../src/types';
const args=process.argv.slice(2);const get=(n:string)=>args.includes(n)?args[args.indexOf(n)+1]:undefined;
const topic=args[0],voice=get('--voiceover'),ref=get('--reference'),name=get('--id')??'new-film';
if(get('--format')&&!['vertical','wide','square'].includes(get('--format')!))throw Error('invalid format');
if(!topic||!voice||!ref)throw Error('Usage: npm run new -- "topic-or-script" --voiceover file --format vertical --reference path --id name');
if(!/^[a-z0-9-]+$/.test(name))throw Error('id must contain lowercase letters/digits/hyphens');
const root=resolve('projects',name);await mkdir(root); // atomic claim; never overwrite an existing project
for(const dir of ['docs','assets/audio','assets/references','reviews'])await mkdir(`${root}/${dir}`,{recursive:true});
const vp=`${root}/assets/audio/${basename(voice)}`;await cp(resolve(voice),vp);const rp=`${root}/assets/references/${basename(ref)}`;await cp(resolve(ref),rp,{recursive:true});
const run=(cmd:string,a:string[])=>{const r=spawnSync(cmd,a,{encoding:'utf8'});if(r.status!==0)throw Error(r.stderr);return r.stdout;};
const dur=Number(run('ffprobe',['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',vp]));
run('python3',['scripts/audio.py',vp,'--out',`${root}/reviews/audio`]);run('python3',['scripts/references.py',rp,'--out',`${root}/reviews/references`]);
const p:Project={id:name,mode:'production',topic,duration:dur,fps:30,format:(get('--format')??'vertical') as Project['format'],seed:777,revision:1,loop:false,voiceover:relative(resolve('.'),vp),accents:[],scenes:[],approvals:{gate1:false,gate2:false,gate3:false,gate4:false,gate5:false},materials:{references:[relative(resolve('.'),rp)],approvedGraphics:[],claims:[]}};
await writeFile(`${root}/project.json`,JSON.stringify(p,null,2));
for(const f of ['brief.md','storyboard.md','style_guide.md','shotlist.md','claims.json','words.json'])await cp(`templates/${f}`,`${root}/docs/${f}`);
await writeFile(`${root}/docs/intake.md`,`# Project intake\n\nTopic/script: ${topic}\n\nOriginal voiceover duration: ${dur}s. Ready for Gate 1 review. Nothing has been approved. Source files preserved, no music.\n`);
console.log(root+' — STOP at Gate 1: inspect materials, write brief and verify claims.');
