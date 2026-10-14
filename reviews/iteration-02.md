# Iteration 02 — dense-strip review catches an entrance collision

Opened actual demo-vertical/phone-sheet.png and transition-morph.png, with frame-by-frame stamps 1.900–2.267s. First pass fixes improved contour/node placement, subtitle size and transition confinement. Dense samples exposed a new defect missed at 2 fps: spring title moved downward through its subtitle during the first ~0.1s of each scene (0.0s, 2.1s, 4.9s).

Local fix: move the entrance above the final baseline rather than below it. Keep subtitle still and title's readable hold unchanged. Add actual title/subtitle bounding-box overlap and horizontal overflow diagnostics to the evidence report. Patch only 0–0.4, 2.1–2.5 and 4.9–5.3s, then reassemble original cached frames and rebuild all evidence. Original revision-2 evidence retained under iteration02-vertical/.

Subjective provisional review: hook 7, phone readability 7, composition 7, motion 6 (collision), scene variety 6 (deliberately simple fixture), brand/voice fidelity N/A. Does not certify production quality.
