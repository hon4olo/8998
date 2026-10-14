export type Format='vertical'|'wide'|'square'|'animatic';
export const formats:Record<Format,[number,number]>={vertical:[1080,1920],wide:[1920,1080],square:[1080,1080],animatic:[960,540]};
export type Scene={id:string;start:number;end:number;initialState:string;finalState:string;action:string;purpose:string;camera:string;transition:string;voiceCue:string|null};
export type Project={id:string;composition?:string;mode:'smoke'|'production';topic:string;duration:number;fps:number;format:Format;seed:number;revision:number;loop:boolean;voiceover:string|null;transcript?:{word:string;start:number;end:number}[];accents:{time:number;cue:string;word?:string}[];scenes:Scene[];approvals:{gate1:boolean;gate2:boolean;gate3:boolean;gate4:boolean;gate5:boolean};materials:{references:string[];approvedGraphics:string[];claims:{text:string;source:string;approved:boolean}[]};};
export function validate(p:Project){
 if(!formats[p.format]||p.duration<=0||!Number.isFinite(p.duration)||!Number.isInteger(p.fps)||p.fps<1||p.fps>120)throw Error('invalid format/duration/fps');
 let end=0;for(const s of p.scenes){if(Math.abs(s.start-end)>1e-6||s.end<=s.start||s.end>p.duration)throw Error('scene gap/overlap/range');end=s.end;}
 if(Math.abs(end-p.duration)>1e-6)throw Error('timeline must cover duration');
 for(const a of p.accents)if(a.time<0||a.time>=p.duration)throw Error('accent out of range');
 for(const w of p.transcript??[])if(w.start<0||w.end<w.start||w.end>p.duration)throw Error('word timestamps out of range');
 if(p.mode==='production' && p.materials.claims.some(c=>!c.source||!c.approved))throw Error('unverified scientific claim');
}
export function gate(p:Project,n:number){validate(p);if(p.mode==='smoke')return; if(!p.composition)throw Error('Production composition required'); if(!p.voiceover)throw Error('Gate 1: supplied voiceover required');if(!p.materials.references.length)throw Error('Gate 1: supplied references required');for(let i=1;i<n;i++)if(!p.approvals[`gate${i}` as keyof Project['approvals']])throw Error(`Gate ${i}: explicit approval required`);}
