import {clamp,mix,morph,noise,spring,springs,track} from '../src/animation/math';
import type {Project} from '../src/types';
export function draw(ctx:CanvasRenderingContext2D,w:number,h:number,t:number,p:Project){
 ctx.resetTransform();ctx.clearRect(0,0,w,h);ctx.fillStyle='#080f19';ctx.fillRect(0,0,w,h);
 const wide=w/h>1.4,vertical=h/w>1.4;const unit=Math.min(w,h),margin=unit*.075;
 const scene=p.scenes.find(s=>t>=s.start&&t<s.end)??p.scenes.at(-1)!;
 const index=p.scenes.indexOf(scene),local=t-scene.start;
 // Format-specific composition: wide gives spatial context, vertical stacks typography above object.
 const cx=wide?w*.68:w*.5,cy=vertical?h*.56:h*.57;
 const auxiliary=wide?1.8:1;const titleX=margin,titleY=vertical?h*.19:h*.22;
 const titles=['FORM','TRANSFORM','CONNECT'];
 const subtitles=['TECHNICAL COMPOSITION','ONE SHAPE · MANY STATES','DIRECT TIME → EXACT FRAME'];
 const titleSize=unit*(p.revision===1?.095:.125);
 const land=spring(local,springs.text),offset=p.revision===1?0:-(1-land)*unit*.07;
 ctx.fillStyle='#edf4f7';ctx.font=`700 ${titleSize}px Studio`;ctx.fillText(titles[Math.min(index,2)],titleX,titleY+offset);const titleWidth=ctx.measureText(titles[Math.min(index,2)]).width;
 ctx.font=`500 ${unit*(p.revision===1?.017:.032)*auxiliary}px Studio`;ctx.fillStyle='#93a6b9';
 const subY=titleY+unit*(wide?.085:.065);
 if(wide){const lines=index===2?['DIRECT TIME →','EXACT FRAME']:subtitles[index].split(' · ');lines.forEach((line,i)=>ctx.fillText(line,titleX,subY+i*unit*.065));}else ctx.fillText(subtitles[index],titleX,subY);
 ctx.save();ctx.translate(cx,cy);
 const camera=track(t,1,[{time:2.1,value:1.12},{time:4.9,value:.86}],springs.camera);
 const entry=p.revision===1?1:mix(.8,1,spring(t,springs.object));ctx.scale(camera*entry,camera*entry);ctx.rotate(.08*Math.sin(t*.65));
 const n=96,r=unit*.255;
 const circle=Array.from({length:n},(_,i)=>{const a=i/n*Math.PI*2;return [Math.cos(a)*r,Math.sin(a)*r];});
 const polygon=Array.from({length:n},(_,i)=>{const a=i/n*Math.PI*2;const rr=r*(.72+.28*Math.cos(3*a));return [Math.cos(a)*rr,Math.sin(a)*rr];});
 const amount=clamp(track(t,0,[{time:2.1,value:1},{time:4.9,value:.35}],springs.diagram));
 const points=morph(circle,polygon,amount);
 ctx.lineWidth=unit*.007;ctx.strokeStyle='#56d8c4';ctx.fillStyle='#102d36';ctx.beginPath();points.forEach((pt,i)=>i?ctx.lineTo(pt[0],pt[1]):ctx.moveTo(pt[0],pt[1]));ctx.closePath();ctx.fill();ctx.stroke();
 const reveal=clamp(spring(t-4.9,springs.ui));
 // Connected graph, not decoration: nodes describe geometry samples of the same contour.
 for(let i=0;i<6;i++){const a=i/6*Math.PI*2+t*.12;const k=(i*16)%n;const x=p.revision===1?Math.cos(a)*r*.66:points[k][0]*.68,y=p.revision===1?Math.sin(a)*r*.66:points[k][1]*.68;
 ctx.globalAlpha=.3+.7*reveal;ctx.strokeStyle='#6c8298';ctx.lineWidth=unit*.002;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(x,y);ctx.stroke();
 ctx.fillStyle=i===0?'#f5b66b':'#edf4f7';ctx.beginPath();ctx.arc(x,y,unit*(.009+.006*noise(p.seed,i)),0,Math.PI*2);ctx.fill();}
 ctx.globalAlpha=1;ctx.fillStyle='#f5b66b';ctx.beginPath();ctx.arc(0,0,unit*.02*(1+.08*Math.sin(t*2)),0,Math.PI*2);ctx.fill();ctx.restore();
 // Meaningful wipe: contour transformation hands off to connection state.
 if(index>0 && local<.25){ctx.fillStyle='#56d8c4';const x=w*clamp(local/.25);ctx.fillRect(x,p.revision===1?0:titleY+unit*.14,unit*.012,p.revision===1?h:h-margin-titleY-unit*.22);}
 ctx.font=`500 ${unit*.03*auxiliary}px Studio`;ctx.fillStyle='#93a6b9';ctx.fillText('ABSTRACT TEST / NO SCIENTIFIC CLAIMS',margin,h-margin);
 const lineW=w-2*margin;ctx.fillStyle='#253544';ctx.fillRect(margin,h-margin-unit*.06,lineW,unit*.004);
 ctx.fillStyle='#56d8c4';ctx.fillRect(margin,h-margin-unit*.06,lineW*clamp(t/p.duration),unit*.004);
 return {time:t,scene:scene.id,title:titles[index],titleBounds:{x:titleX,y:titleY+offset-titleSize,width:titleWidth,height:titleSize},subtitleBounds:{x:titleX,y:subY-unit*(p.revision===1?.017:.032)*auxiliary,height:unit*(p.revision===1?.017:.032)*auxiliary},minTextPhonePx:unit*Math.min(.03,p.revision===1?.017:.032)*auxiliary*360/w,camera,morph:amount};
}
