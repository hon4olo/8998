import {draw as technical} from './technical';import type {Project} from '../src/types';
export const compositions:Record<string,typeof technical>={technical};
export function draw(ctx:CanvasRenderingContext2D,w:number,h:number,t:number,p:Project){
 const name=p.composition??(p.mode==='smoke'?'technical':'');const scene=compositions[name];if(!scene)throw Error('No production composition registered. Author approved scenes and set project.composition.');return scene(ctx,w,h,t,p);
}
