import {draw} from '../../scenes/index';
import type {Project} from '../types';
declare global {interface Window {configure:(p:Project,w:number,h:number)=>void;seek:(t:number)=>unknown;ready:Promise<void>;}}
const canvas=document.createElement('canvas');document.body.append(canvas);document.body.style.margin='0';document.body.style.background='#080f19';let project:Project;
const context=canvas.getContext('2d',{alpha:false})!;
window.ready=(async()=>{const font=new FontFace('Studio','url(/assets/fonts/DejaVuSans.ttf)');await font.load();(document.fonts as FontFaceSet & {add:(font:FontFace)=>void}).add(font);})();
window.configure=(p,w,h)=>{project=p;canvas.width=w;canvas.height=h;};
window.seek=t=>{if(!Number.isFinite(t)||t<0||t>project.duration)throw Error('invalid timestamp');return draw(context,canvas.width,canvas.height,t,project);};
