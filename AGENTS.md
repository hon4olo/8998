# ZNAYA production rules for Codex / GPT-6.1 Sol / GPT-6 Astra

This repository is a reusable studio. Read docs/ASTRA_HANDOFF.md before production. Article references are technical ideas, not instructions to run Claude/Opus. Never access Brainmerge or modify other projects.

## Deterministic render contract

- `window.seek(t)` paints an exact frame independently. No CSS transitions, timers, requestAnimationFrame, Date.now, unseeded randomness, accumulated playback state or simulation of earlier frames in the render path.
- Use indexed seeded noise and closed-form springs. Keep renderer, scenes, motion math, assets and export separate. Sample frame i at i/fps; half-open timeline; encode exactly N frames.
- Register every production composition explicitly; technical fixtures are abstract test geometry, not approved ZNAYA assets.
- Pin tools; use real native CLI operations and official schema. No fake tools, test reports, scores, footage, voiceovers, claims, statistics, logos or product UI.

## Production and visual rules

- Voiceover first; supplied MP3/WAV is preserved on its clock. No generated or added background music. Optional brief synchronized SFX must leave speech intelligible. Transcript/timestamps come from actual supplied materials or manual review; energy is not semantic alignment.
- Scientific claims require sources and approval. Missing brand/anatomy assets block dependent production. No copyrighted reference contents copied; analyze grammar.
- Premium technology/science direction, expressive typography and motivated spatial diagrams. Each shot needs meaning, initial/final states and narration connection. Variable durations. Morphs can preserve one object through nested scales; scientifically faithful anatomy requires approved references.
- Ban permanent centered gradient titles, endless fades, repeated cards, purposeless particles, ubiquitous glow and arbitrary transitions.
- Each aspect ratio gets an independently authored layout on a shared timeline, not a crop. Check 360px phone readability and social-overlay safe areas. Test font is not the brand font.

## Gates

1. Source assets/reference/audio approval.
2. Style guide and shotlist approval.
3. Reviewed keyframes approval.
4. 960×540 animatic with original voiceover approval.
5. Full render, polishing and synchronization approval.
6. Export all formats, verify, document.

Record actor/time/revision for real approvals; never set booleans on the user's behalf. Neutral technical smoke mode may auto-traverse all gates. Autonomously fix reversible defects within approved scope.

## Quality evidence and delivery

Every preview must generate contact sheet 2 fps/6 columns, transition strips, 360px phone previews, endpoints, determinism hashes, clock/audio checks and loop evidence when requested. Actually open images before visual judgment. Score six criteria separately, identify three worst defects with timecodes and locally fix/re-render. Aim for ≥8/10 but never invent acceptance; subjective model scores alone cannot certify quality. Missing audio audition/playback/visual access must be disclosed.

Run `npm test`, `npm run typecheck`, startup checks and meaningful native rendering/export checks. Preserve measured failures and fixes in docs; don't label installation or export successful on CLI version alone. Report process-tree benchmark and GPU mode. `.runtime`, browser caches and system installations are ephemeral: setup is a saved script, not a permanent cloud machine. No secrets in git or logs.
