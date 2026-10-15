# ZNAYA — thyroid quality scene, structural revision5

One existing12.4s scene,1080×1920/30fps, original voice excerpt28.72–41.12s. No music or SFX. This is a quality test, not the full95s film.

## Latest deliverables

- `out/znaya-thyroid-structure-final.mp4` — final structural/cinematic revision.
- `reviews/znaya-thyroid-structure-final/` — contact2fps/6columns, phone360px, transitions, endpoints, ffprobe and automated checks.
- `reviews/thyroid-structure-critique.md` — two substantive correction rounds and final assessment.
- `reviews/znaya-thyroid-structure-final-benchmark.json` — process-tree timing/RAM.
- `out/thyroid-structure-v3.mp4` — first structural preview,540×960.
- `out/znaya-thyroid-quality.mp4` — prior Canvas version, retained for comparison.

## Reproduce

```bash
npm ci                         # only in a fresh checkout / after dependency changes
npm run check
python3 scripts/prepare-thyroid-structures.py
npm run typecheck
npm test
npx tsx scripts/preview.ts --project projects/voice-quality/project.json --out reviews/thyroid-keyframes
python3 scripts/benchmark.py --out reviews/thyroid-benchmark.json -- npx tsx scripts/render.ts --project projects/voice-quality/project.json --name znaya-thyroid-structure-final
python3 scripts/quality-gate.py reviews/znaya-thyroid-structure-final
```

No tool reinstall was required in the existing environment. Added pinned Three.js0.180.0/types and retained the existing renderer/export APIs. WebGL runs through CPU SwiftShader with the existing Chromium flags. First context/shader initialization may take several seconds. No network calls, animations or timers run during frame painting. Raw structural sources and derived geometry are in the repository; ASR/redownload is unnecessary for rendering.

Source: `scenes/thyroid-quality.ts` (composition, tissue and typography), `src/components/thyroid-3d.ts` (real3D ligands/protein, lights, camera and idealized DNA), `scripts/prepare-thyroid-structures.py` (auditable extraction), `project.json` (same timeline/audio and six word cues). Test: `tests/thyroid-structure.test.ts` verifies source hashes, chemical graph preservation and geometric fidelity to PDB. `tests/thyroid-quality.test.ts` verifies independent-browser/out-of-order frame equality.

## Real structures and artistic boundaries

Read [STRUCTURAL_REFERENCES.md](docs/STRUCTURAL_REFERENCES.md). Ligands use CCDT3/T44 topology; receptor is actual human TRα ligand-binding domain2H77. Original T4→T3 reaction interpolation, ligand approach and graphical cutaway are explanatory art, not observed dynamics. The final DNA shot is a distinct idealized illustration, not an invented receptor-DNA binding pose. Tissue anatomy is stylized. Palette/typography are a proposed direction, not approved brand assets.

The selected supplied WAV is included for reproduction. Full95s source MP3 and full raw ASR transcript remain local; selected word timestamps and source SHA/offsets are retained. No speed, pitch or gain change. Final AAC is lossy encoding. Manual audio audition is not claimed.

The user authorized this continuation, iterative critique and GitHub publication. Final artistic acceptance remains with the user. Earlier documentation/snapshots describe historical revisions; current structural source notes take precedence.

Partial corrections use `--patch --ranges 4.85:5.6,10.26:12.4` with the existing full frame cache and reviews/NAME/frames.json. The patch path now reuses metadata for untouched frames rather than repainting them; the existing real MP4 patch test was rerun successfully.
