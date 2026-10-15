"""Optional isolated CPU ASR for the supplied quality-test voiceover; no external speech API."""
import json,time,pathlib,subprocess
import numpy as np
from faster_whisper import WhisperModel
start=time.monotonic()
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2,download_root='.runtime/asr-models')
pcm=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i','projects/voice-quality/assets/voiceover-original.mp3','-ar','16000','-ac','1','-f','f32le','pipe:1']),dtype=np.float32)
segments,info=model.transcribe(pcm,language='ru',beam_size=5,word_timestamps=True,vad_filter=True)
rows=[]
for s in segments:
 row={'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word.strip(),'start':w.start,'end':w.end,'probability':w.probability} for w in s.words or []]};rows.append(row);print(f'{s.start:.2f}–{s.end:.2f}: {s.text}',flush=True)
pathlib.Path('projects/voice-quality/docs/transcript-asr.json').write_text(json.dumps({'model':'faster-whisper small int8 CPU','language':info.language,'languageProbability':info.language_probability,'duration':info.duration,'wallSeconds':time.monotonic()-start,'segments':rows,'status':'machine transcript; scientific spelling and chosen excerpt require contextual review'},ensure_ascii=False,indent=2))
