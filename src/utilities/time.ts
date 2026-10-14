export type Word={word:string;start:number;end:number};
export function wordCue(words:Word[],word:string,occurrence=0):number {const matches=words.filter(w=>w.word===word);if(!matches[occurrence])throw Error('requested word/occurrence not present in supplied timestamps');return matches[occurrence].start;}
export function activeWords(words:Word[],t:number):Word[] {return words.filter(w=>t>=w.start&&t<w.end);}
export function phraseWindow(words:Word[],first:number,last:number):[number,number] {if(first<0||last<first||last>=words.length)throw Error('invalid phrase bounds');return [words[first].start,words[last].end];}
