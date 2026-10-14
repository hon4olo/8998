export const clamp=(x:number,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const mix=(a:number,b:number,u:number)=>a+(b-a)*u;
export function noise(seed:number,index:number):number { let x=(seed ^ Math.imul(index+1,0x9e3779b9))>>>0; x=Math.imul(x^(x>>>16),0x21f0aaad); x=Math.imul(x^(x>>>15),0x735a2d97); return ((x^(x>>>15))>>>0)/4294967296; }
export type Spring={frequency:number; damping:number};
export const springs:Record<string,Spring>={text:{frequency:2.8,damping:.68},ui:{frequency:4,damping:.88},camera:{frequency:.7,damping:1},object:{frequency:2,damping:.56},diagram:{frequency:2.5,damping:.95}};
// Unit step response of x'' + 2 ζ ω x' + ω² x = ω². Zero displacement/velocity before event.
export function spring(t:number,p:Spring=springs.object):number {
 if(p.frequency<=0 || p.damping<=0) throw Error('positive spring parameters required');
 if(t<=0)return 0; const w=p.frequency*2*Math.PI,z=p.damping;
 if(Math.abs(z-1)<1e-7)return 1-Math.exp(-w*t)*(1+w*t);
 if(z<1){const d=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*t)*(Math.cos(d*t)+z*w/d*Math.sin(d*t));}
 const a=-w*(z-Math.sqrt(z*z-1)),b=-w*(z+Math.sqrt(z*z-1));return 1+(b*Math.exp(a*t)-a*Math.exp(b*t))/(a-b);
}
export type Target={time:number;value:number;spring?:Spring};
export function track(t:number,initial:number,events:Target[],preset=springs.object):number {
 let prev=initial,result=initial,last=-Infinity;
 for(const e of events){if(e.time<last)throw Error('target events must be sorted');result+=(e.value-prev)*spring(t-e.time,e.spring??preset);prev=e.value;last=e.time;}return result;
}
export function morph(a:number[][],b:number[][],u:number):number[][] {if(a.length!==b.length)throw Error('morph requires equal point counts');return a.map((p,i)=>[mix(p[0],b[i][0],u),mix(p[1],b[i][1],u)]);}
