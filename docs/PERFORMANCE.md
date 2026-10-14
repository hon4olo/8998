# Measured cloud performance

Debian13 x86_64, effective cgroup quota 2 CPU / 8 GiB (3 affinity CPUs, ~9.7GiB host-reported RAM), no exposed GPU, Vulkan Mesa lavapipe CPU. Browser fixtures: 8 seconds at 30fps (240 frames). Native: 2s/60 frames. Both paths perform actual rendering and FFmpeg encoding.

| Run | Wall seconds | Sampled process-tree CPU seconds | Peak summed RSS MiB | CPU / wall (100% = one core) |
|---|---:|---:|---:|---:|
| Vertical full | 37.60 | 46.23 | 740.0 | 123% |
| Wide full final | 33.16 | 41.57 | 754.6 | 125% |
| Square full | 23.89 | 25.64 | 663.7 | 107% |
| Animatic full final | 17.18 | 13.07 | 627.6 | 76% |
| Vertical local patch+full rebuild | 32.41 | 35.37 | 749.7 | 109% |
| Tesseract native | 1.72 | 0.83 | 228.1 | 48% |
| Tesseract browser adapter re-export | 11.24 | 20.89 | 462.4 | 186% |

Wall time includes browser launch, fonts, frame capture, encoding and complete evidence generation (contact/phone/strips, endpoint checks). The critic currently launches FFmpeg per sampled image: evidence rebuilding can dominate short local patches. A patch saves frame capture but still encodes the whole timeline and regenerates full review. Test/installation work overlapped some measurements, so these are observed session timings, not isolated laboratory throughput.

Method: scripts/benchmark.py samples /proc every 100ms, follows process descendants including Chromium and FFmpeg, sums RSS and observed CPU tick maxima. Summed RSS can double-count shared pages; short-lived/reparented children can be missed. CPU values are approximate. Node-only per-export counters are separately stored and explicitly exclude child resources. No GPU acceleration was used. Raw JSONs under reviews/.

At this load all fixtures fit well below available memory. No performance guarantee for heavy 3D, photoreal footage, complex scientific scenes or long videos is inferred from this smoke test.


Container limits measured from /sys/fs/cgroup: cpu.max = 200000 100000 (2 CPU quota), memory.max = 8589934592 (8 GiB). nproc reports 3 available affinity CPUs and free reports ~9.7 GiB host-visible memory; effective container capacity is 2 CPU / 8 GiB, not those larger host/affinity figures. FFmpeg uses 3 threads within that quota.
