# Iteration 01 — actual rendered-image review

Evidence opened by the Codex agent: initial-vertical/contact-sheet.png (16 samples, 0–7.5s) and native-filmstrip.png. No narration supplied; no claims about listening or scientific accuracy.

Three highest-impact observed defects:

1. 0–8s: subtitle is effectively unreadable at phone width (~6.1 px). Increase subtitle 0.017→0.032 of short side; fix minimum-text metadata to include actual subtitle size (previous heuristic falsely considered only footer). Increase title hierarchy.
2. 2.5–4.5s: geometric sample nodes fall outside the trilobe contour, undermining the intended connected-contour meaning. Place nodes using the same morphed control points, scaled inward.
3. ~5.0s: transition bar crosses headline and footer. Confine transition sweep to the diagram field, preserving the readable text hold.

Additional local change: spring scale arrival in the first second makes the technical hook demonstrate mass instead of a near-static hold.

Provisional subjective scores based on sampled images only: hook 6, phone readability 5, composition 7, motion 6 (dense-strip review still pending), variety 6, material/voice fidelity N/A. These are not independently verified acceptance scores. This deliberately simple smoke test is not a finished premium ZNAYA film.

Revision 2 implements the local fixes; render changed sections plus full reassembly and inspect new evidence. No automatic 8/10 claim.
