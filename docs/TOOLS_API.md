# Tools and APIs

## Browser/frame contract

`window.ready: Promise<void>` waits for packaged font. `window.configure(project,width,height)` configures a fresh Canvas. `window.seek(t)` accepts finite seconds 0..duration and paints without timers/history; it returns review metadata. Render exports frames at `i/fps`, `i=0..N-1` (never duration itself). `src/types.ts` describes project and scene data; `validate` checks gap/overlap and ranges. `scenes/index.ts` registers composition functions; add a production implementation explicitly. No script-to-video generative service is faked.

`spring(t,{frequency,damping})`: analytic zero-velocity unit step for underdamped, critical and overdamped response; t≤0 returns 0. `track(t,initial,events,preset)` superposes target deltas directly, preserving history-independent sampling. `noise(seed,index)` yields deterministic [0,1). `morph(a,b,u)` linearly interpolates equal-size point lists; author point correspondence before use. Presets: text/ui/camera/object/diagram.

`npm run render -- --project P --format vertical|wide|square|animatic --name NAME`: encode real frames. `--scale 0.5` reduces resolution; `--start 2 --end 3` renders a real independent segment. Times round to nearest frame. `--patch --ranges 0:0.4,2.1:2.5 --name EXISTING_NAME`: requires complete compatible frame cache, re-renders selected intervals, recomputes all metadata, encodes whole timeline and regenerates reviews. Choose ranges covering all affected state; global edits require full render. Frame cache is deliberately excluded from Git; regenerate it after fresh checkout. `--gate` may select only the actual production stage, never circumvent approvals.

FFmpeg: installed 7.1.5; browser pipeline uses libx264, fast preset, CRF 18, yuv420p, 3 encoder threads, +faststart, 30 fps fixture. Audio supplied via `project.voiceover`; no atempo or normalization, AAC 192k. Source duration must cover export end, or renderer fails. Fractional tail shorter than one frame is rounded; report this and review endpoint. New production projects derive duration from original audio. No music.

## References and narration

`python3 scripts/references.py PATH --out REVIEWS`: image/video/folder, video frames every 0.5s, quantized palette, heuristic scene-change candidates. Generated style/shot documents are marked pending until a model actually opens images and interprets composition/type/rhythm/camera. No automatic font recognition, scientific inference or aesthetic score. For production copy reviewed conclusions into project docs/style_guide.md and shotlist.md.

`python3 scripts/audio.py AUDIO --out REVIEWS --words words.json`: FFmpeg PCM decoding, duration, 20ms RMS structure and real waveform PNG; optional validated manual word timestamps. No transcription model installed. `python3 scripts/align.py --audio AUDIO --transcript TEXT --manual words.json --output aligned.json`; or `--command /path/to/local-aligner` (ABI: executable accepts --audio, --transcript, --output; emits [{word,start,end}], seconds). The repository does not silently call paid APIs. Put reviewed word marks in project.transcript and accents `{time,cue,word}`. Repeated-word cues match by time. Energy alone never supplies word meanings.

Optional SFX: `python3 scripts/sfx.py --project P --output accents.wav`; amplitude-limited 80ms chirps at project accents, no melody/music. `python3 scripts/mix-sfx.py video.mp4 accents.wav --output mix.mp4 --gain 0.3` keeps video stream and speech time intact; audition/review speech intelligibility and clipping before acceptance. The main test exports are silent; the WAV/AAC tests use clearly labeled diagnostic pulses.

## Native Tesseract 0.3.1

Official skills snapshot commit fbc9458 (full commit in docs/toolchain.json), same pin 0.3.1 in installed plugin and snapshot. Official GitHub main has since moved to 0.4.0, intentionally not substituted. Runtime source release and checksum in scripts/install-tesseract.sh. Use `source scripts/tesseract-env.sh` then quoted `$TSRCT` absolute executable. Linux Vulkan lavapipe runs on CPU. No native installation is assumed permanent.

Actual commands: `project create`, `project inspect`, `project schema [--document]`, `project checkout --output`, `project commit --file`, `project apply --actions`, `project import-font`, `project import-video`, `project import-asset --kind audio|image`, `preview --time`, `filmstrip --start-ms --duration-ms --interval-ms`, `export --encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg`.

Version-specific official documentation lives in skills/tesseract-motion and skills/tesseract-video. Query actual installed schemas into .runtime before authoring fields. Document duration = seconds; layer activeRange/playback/sourceRange = ms; `layers[0]` frontmost; transforms pixels/percent; JS animation reads `input.time.seconds` and explicitly returns a value. Keep media source and edit clocks distinct. 0.3.1 export FPS supports 24/30/60 and exposed resolutions 720p/1080p/4k; no guessed 0.4 flags or arbitrary FPS/segment export.

`python3 scripts/adapter.py browser.mp4 --output out/edit.tsrct`: packages browser MP4 as actual native Video layer with source/edit mapping. Browser geometry/text are flattened pixels within Video; editable source remains TypeScript. Native titles/shapes/audio/keyframes/scripts added in Tesseract stay editable. See out/native-smoke.tsrct for real native layers, out/native-editable.json for checked-out native schema, out/browser-adapter.tsrct for actual import. This is not a DOM→native layer translator.

## Critic

Every render invokes scripts/review.py: real sampled images, contact/phone sheets, dense 12-frame strips, endpoints, nonblank raster checks, declared text bounds/overlap, determinism, original-vs-AAC zero-lag correlation and timestamped word anchors where supplied. Loop projects additionally get endpoint error and doubled playback MP4. Dense strips cannot replace playback/eye and ear review. Correlation measures preservation, not semantic alignment; AAC can lower exact sample correlation. scores stay pending until actual visual evaluation. Retain reports per iteration and use reviewed fixes, never fabricate automatic 8/10.

Observed 0.3.1 custom-canvas resolution behavior: native-smoke authored 640×360, `--resolution 720p` exported 426×240 (not 1280×720); browser-adapter authored 1080×1920 exported 720×1280. Inspect actual ffprobe dimensions; use delivery-size author canvas/1080p when exact output size is required.

Supplied narration helper APIs: `wordCue(words,word,occurrence)` anchors repeated words by occurrence; `phraseWindow(words,first,last)` returns reviewed phrase time range; `activeWords(words,t)` uses half-open intervals. `src/components/captions.ts` draws only supplied timed words with wrapping and explicit safe-area box, never invented speech.
