import {activeWords,type Word} from '../utilities/time';
// Draw only supplied timed text, no invented transcript. Caller controls phone-safe placement.
export function drawTimedCaption(ctx:CanvasRenderingContext2D,words:Word[],t:number,box:{x:number;y:number;width:number;fontSize:number;color:string}){
 const text=activeWords(words,t).map(w=>w.word).join(' ');if(!text)return null;
 ctx.save();ctx.font=`500 ${box.fontSize}px Studio`;ctx.fillStyle=box.color;
 const lines:string[]=[];let current='';for(const word of text.split(' ')){const candidate=current?`${current} ${word}`:word;if(ctx.measureText(candidate).width>box.width&&current){lines.push(current);current=word;}else current=candidate;}if(current)lines.push(current);
 lines.forEach((line,i)=>ctx.fillText(line,box.x,box.y+i*box.fontSize*1.25));ctx.restore();return {text,lines,bounds:{...box,height:lines.length*box.fontSize*1.25}};
}
