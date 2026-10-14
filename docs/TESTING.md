# Actual validation and repaired failures

Commands actually executed: npm ci through scripts/setup.sh, pinned Pillow setup, Playwright Chromium installation, official Tesseract SHA-256 install and version check, local Mesa checksum/extraction/ldd check, npm run typecheck, npm test, startup checks multiple times, native preview/filmstrip/export, adapter import/preview/export, all-format real browser export, local partial patches, real reference extraction/intake, mandatory evidence builders, optional SFX creation/mux.

Retained results: reviews/tests-output.txt, startup-checks.txt, startup-repeated.txt, installation-test.txt, setup-end-to-end.txt, native-smoke-test.txt, per-export ffprobe/determinism/automated-checks/benchmarks, references analysis, iteration-01/02/03.md. Test count is taken from the final captured run, not asserted from an unrun plan.

Tests cover: analytic under/critical/overdamped spring start/settling; overshoot vs monotonic camera response; target-event continuity and superposition; indexed seeded noise; morph endpoints; variable scene coverage/gaps/overlaps; real production gates and claims; actual Chromium raster; out-of-order seek hashes across two fresh browsers; real segment PNG→H264 MP4 and frame count; real supplied pulse WAV→AAC clock preservation and waveform energy; 0.5s reference video extraction; selected-range cached-frame replacement with before/after SHA and full MP4 reassembly; supplied word/phrase caption cue boundaries.

Full delivered clips: 240 actual frames/8s/30fps at vertical1080×1920, wide1920×1080, square1080×1080, animatic960×540. Native smoke:60 frames/2s, authored640×360, exported426×240 with runtime0.3.1 --resolution720p. Browser adapter native export:240 frames/8s at720×1280. Inspect ffprobe JSON instead of assuming a resolution label normalizes arbitrary canvas sizes. No runtime GPU device is available: Vulkan adapter is local software lavapipe.

Repaired reproducible failures:

- Browser bundle initialized Canvas before document.body existed: explicit body before script, then real browser/determinism/export tests passed.
- FFmpeg timestamp formatting received floating-point `8.326e-17` in dense segment sampling: fixed decimal formatting; real segment E2E test passed.
- Benchmark writer was incorrectly inside sample loop: fixed indentation, reran actual process-tree measurements. Failed preliminary results were not called successful measurements.
- Startup tried to create an existing .tsrct on second run: fresh temporary native project now used; repeated startup passed. Native fixture rerun retains previous source before creating a fresh test document.
- Phone subtitle too small, nodes outside contour, wipe through text: real review, local patches and new exports.
- Dense strips revealed spring entrance crossing subtitle: moved entrance above final baseline, bounds checks and selective frame rebuild verified.
- Wide/animatic auxiliary type too small in360px preview: 1.8× size and separate multiline layout, full re-render and mechanical gate passed.
- First patch attempt lacked newly introduced cache manifest: rejected rather than falsely patching; original retained frames verified and manifest initialized, then actual patch ran. Future full renders write this cache themselves.

Aesthetic/semantic review is separate: actual rendered images were opened and assessed, but full video/audio audition of real narration cannot be claimed (none supplied). Final technical scores include hook7 and variety6; brand/voice=N/A. Production quality ≥8 and independent approval are deliberately not claimed. `quality-gate.py --require-visual` correctly rejects this smoke as a production acceptance; its retained report is an expected unmet artistic gate, not a renderer failure.

Loops are optional and absent in the delivered non-looping technical film. The loop evidence builder handles project.loop=true by endpoint pixel error plus actual double-play MP4. Endpoint mean error is only a heuristic; motion continuity requires actual join review. Do not relabel this fixture as seamless.

Original-audio correlation in reviews/e2e-audio/automated-checks.json measures actual decoded pulse waveform before/after AAC on the same clock (~0.99999); it does not demonstrate word alignment or audition. Manual timestamps/local aligner remain required for real speech. No background music or speech generation.

Final test suite captured 13 passed / 0 failed (reviews/tests-output.txt). Four delivery-format mechanical quality gates passed. Native out-of-order preview SHA-256 comparison also passed at1s with an intervening0s seek. Source-Canvas determinism is inherited explicitly in flattened adapter/SFX evidence, never represented as a newly proven independent native scene-function equivalence.

Fresh GitHub checkout validation: cloned hon4olo/8998 into a newly created /workspace/znaya-restore-check, ran the full setup script (npm ci, pinned runtime/checksum install, new local Mesa extraction and actual Chromium/Vulkan startup), then all13 tests passed again. All9 delivered artifact SHA-256 hashes matched docs/artifacts.json. This is a new checkout on the same Debian13 cloud machine, sharing system libraries/browser cache; it is not claimed as proof on a separately provisioned host. Logs: reviews/fresh-checkout-setup.txt and fresh-checkout-tests.txt.
