# Передача ZNAYA Motion Studio для GPT-6 Astra

## Состояние проекта

Репозиторий: https://github.com/hon4olo/8998. Рабочая папка текущего cloud-сеанса: `/workspace/777`. Это готовая техническая инфраструктура, а не настоящий ролик ZNAYA. Не повторяй установку в этой среде, если `npm run check` проходит. Для новой машины — `bash scripts/setup.sh`, инструкции в CODEX_CLOUD.md. Системные runtime/cache не становятся постоянными от публикации в GitHub.

Озвучка, настоящие референсы ZNAYA, логотипы, научные изображения и готовые утверждения пока не предоставлены. Все текущие формы/тексты — абстрактный smoke test. `assets/audio/diagnostic-pulses.wav` содержит проверочные импульсы, не дикторскую речь. Фоновая музыка не создана и не подключается. Не превращай технический пример в готовый научный ролик.

## Быстрый старт с реальными материалами

Положи supplied audio в `assets/audio/voiceover.mp3`, изображения/видео или папку образцов в `assets/references/my-reference`, утверждённую графику в `assets/approved`, настоящие logos в `assets/logos`. Проверь происхождение/лицензии, не выдумывай недостающие файлы.

```bash
npm run check
npm run new -- "Тема или готовый сценарий" --voiceover assets/audio/voiceover.mp3 --format vertical --reference assets/references/my-reference --id first-film
```

В Codex поддерживаемое обращение к project-local skill: `$znaya-motion-studio "Тема или сценарий" --voiceover assets/audio/voiceover.mp3 --format vertical --reference assets/references/my-reference`. Skill discovery: `.agents/skills/znaya-motion-studio/SKILL.md`; canonical copy — `skills/znaya-motion-studio/SKILL.md`. Собственная slash-команда `/znaya-motion-studio` не зарегистрирована; не обещай её работу. Этот skill задаёт процесс агенту, а shell intake лишь подготавливает материалы/документы, не генерирует фильм из текста автоматически.

Intake атомарно создаёт `projects/first-film`, копирует реальное audio/reference, определяет длительность, строит waveform и извлекает кадры reference каждые 0.5 секунды. Заполняй `projects/first-film/docs/brief.md`, claims.json, style_guide.md, shotlist.md, storyboard.md, words.json. Не перезаписывай существующий проект; продолжай его только при явном намерении пользователя.

## Все восемь компонентов

| Компонент статьи | Реальная адаптация под Codex |
|---|---|
| Frame Function | `src/renderer/browser.ts`, `scripts/browser.ts`, `scripts/render.ts`: configure/ready/seek(t), Canvas и Playwright PNG; FFmpeg MP4 |
| Rig | Debian 13, Node/TS/Python/FFmpeg/Chromium, pinned Tesseract 0.3.1 и CPU Vulkan lavapipe; setup/startup/diagnosis scripts |
| Brief | templates/ и project.json: цели, аудитория, материалы, audio, transcript, verified claims, таймлайн, approvals |
| Reference | references.py: image/video/folder, кадры 0.5s, палитра/cut candidates; обязательный реальный просмотр Astra и style/shot docs |
| State Lists | переменные start/end, initial/final states, action, purpose, camera, transition, voice cue; matched-point morph |
| Springs & Sound | аналитическая spring/track библиотека; исходное audio, 20ms RMS/waveform, ручные word marks, future aligner ABI, optional short SFX; без музыки |
| Critic | обязательные sheets/strips/phone/endpoints, determinism, text bounds/clock/loop checks, фактический просмотр и timecoded local fixes |
| Skill | project-local znaya-motion-studio, AGENTS.md, production gates, saved toolchain/recovery/API/docs |

Статья используется как технический референс. Заявления о релизах/популярности/доходах не являются проверенными данными проекта и не используются в научном содержании. Claude/Opus не запускаются.

## Production gates и approvals

1. Проверить и получить утверждение референсов, исходной озвучки и реальных материалов. Сверить текст, длительность, лицензии, источники научных утверждений. Missing assets блокируют зависимую работу.
2. Из фактически просмотренных reference frames написать style guide и shotlist; получить утверждение обоих. Автоматическая палитра/scene detection не являются завершённым визуальным анализом.
3. Написать композицию и получить утверждение просмотренных ключевых изображений всех сцен. `npm run preview -- --project projects/first-film/project.json` создаёт entry/hold/exit каждого состояния. Исправить три худших дефекта, повторить review.
4. `npm run render -- --project projects/first-film/project.json --format animatic --name first-film-animatic --gate 4`: независимый 960×540 animatic с исходной озвучкой. Проверить/утвердить pacing и смысл.
5. Полный vertical render и полировка, sync по словам/фразам, реальное evidence review. Получить утверждение готовой проходки.
6. Экспорт независимых vertical/wide/square layouts; ffprobe, contact sheets, endpoint/loop/audio checks, poster, README и source handoff.

`project.approvals.gate1..gate5` фиксируй только после действительного пользовательского утверждения. В project docs записывай actor, timestamp, scope и точный revision. Не устанавливай approvals на основании молчания или самооценки. `mode=smoke` допускает автоматическое прохождение только явно нейтральных тестовых данных. Renderer требует gates 1–4 для full export; animatic требует 1–3. Аргумент --gate не снижает этап.

## Как написать первый фильм

1. Прочитай AGENTS.md, TOOLS_API.md, заполненный brief и одобренный style guide. Научные факты проверяй по cited sources; реалистичная научная схема должна опираться на утверждённые материалы.
2. Создай `scenes/first-film.ts` с чистой `draw(ctx,w,h,t,project)`. Добавь её в registry `scenes/index.ts`, задай `project.composition='first-film'`. Production без зарегистрированной композиции не должен использовать technical fixture. Дополни `project.scenes` переменными интервалами, покрывающими duration без gaps/overlaps.
3. Для каждого scene: initial/final state, action, purpose, camera, motivated transition, word/phrase cue и acceptance. Для continuous brain→neuron→synapse→molecule подготовь проверенные контуры и координатные преобразования; это поддерживаемый паттерн, не уже нарисованная в инфраструктуре анатомия.
4. Используй `spring`, `track`, `morph`, `noise` из src/animation/math.ts. Все значения зависят от t/seed; никаких timers, Math.random, CSS transitions, wall clock или накопленных frames. Озвучка остаётся на исходной скорости; разрешено создавать short SFX по событийным timestamp, музыка запрещена.
5. Разметь реальные слова вручную, если нет local aligner. `scripts/align.py` принимает `--manual words.json` или подключаемый executable ABI. Транскрипцию и forced alignment здесь не изображают установленным AI-сервисом. Energy не заменяет смысловой sync.
6. Для каждого aspect ratio вычисляй собственную композицию. Vertical — крупнее type и меньше объектов, wide — больше пространственного контекста, square — компактные holds. Ни один экспорт не обрезается из другого. В wide smoke typography пришлось увеличить для реальной читаемости на 360px — этот опыт не потеряй.
7. Выполни approved gates, рендер и review. Все previews автоматически строят evidence. Открывай изображения, оценивай hook первых 2s, phone readability, composition, motion, scene variety, brand/voice fidelity. Scores с реальными timecodes, три worst defects и local fixes. Цель ≥8/10; модельные оценки сами по себе не сертифицируют качество. Если не можешь слушать/проиграть видео или смотреть картинки, явно оставь этот review pending.

## Рендер, локальные исправления и тесты

```bash
npm run typecheck
npm test
npm run render -- --project projects/first-film/project.json --format vertical --name first-film-vertical
npm run render -- --project projects/first-film/project.json --format wide --name first-film-wide
npm run render -- --project projects/first-film/project.json --format square --name first-film-square
python3 scripts/quality-gate.py reviews/first-film-vertical
```

Фрагмент: `npm run render -- --project P --start 2 --end 3 --name changed-segment`. Локальная пересборка: `npm run render -- --project P --name EXISTING_EXPORT --patch --ranges 0:0.4,2.1:2.5`. Нужен полный совместимый cache кадра; cache не коммитится и создаётся full render. Выбирай все затронутые интервалы; global edits требуют полного рендера. Partial pipeline проверен тестом, сравнивающим SHA неизменных кадров и обновлённых кадров, затем ffprobe полного MP4.

Каждый экспорт: MP4 в out/, real images и JSON reports в reviews/NAME/. Contact sheet 2fps/6 cols; phone 360px; 12 consecutive frames around semantic transitions; first/last actual encoded frames; random-order seek hashes; declared type sizes/overlaps; source-vs-AAC zero-lag correlation и word accents, если supplied. Raster nonblank проверяется отдельно от эстетики. Loop flag дополнительно создаёт double playback и endpoint difference; inspect actual join, низкая mean pixel error не доказывает seamless motion.

## Tesseract: реально работающий второй путь

Официальные sources: github.com/mirage-hq/Tesseract, skills/tesseract-video/references/installation.md, dev.mirage.app/tesseract/linux. Использован закреплённый official skill runtime 0.3.1, SHA-256 проверен, tsrct --version совпал. Official skills сохранены из релизного commit fbc9458. Main уже 0.4.0; не обновляй runtime отдельно от skills.

```bash
source scripts/tesseract-env.sh
"$TSRCT" --version
npm run tesseract
python3 scripts/adapter.py out/first-film-vertical.mp4 --output out/first-film-edit.tsrct
"$TSRCT" export --project out/first-film-edit.tsrct --resolution 1080p --fps 30 --encoder-backend external-ffmpeg-command --ffmpeg-path /usr/bin/ffmpeg --output out/first-film-native.mp4
```

`out/native-smoke.tsrct`: genuine native editable typography, geometric panel, analytic JS spring and native rotation keyframes. `out/native-smoke.mp4`: actual official-runtime export. `out/browser-adapter.tsrct`: actual imported full Canvas MP4; `out/browser-adapter.mp4`: actual runtime re-export. Adapter сохраняет browser content как flattened Video, исходная Canvas-геометрия редактируется в TypeScript; добавленные native Text/Shape/Audio/animation layers редактируются в .tsrct. Прямой Canvas/DOM→native слой translator не реализован и не заявлен. Перед authoring запрашивай actual CLI schema; 0.3.1 не поддерживает некоторые флаги из нового 0.4 guide.

Linux без /dev/dri, Vulkan через Mesa lavapipe с local ICD/library path. GPU hardware acceleration нет. External FFmpeg libx264/AAC выбран явно; установка FFmpeg сама не добавляет encoder в bundled runtime. `.tsrct` не редактируется как текст/ZIP; checkout→commit, project apply и import commands.

## Evidence, результаты и ограничения

- Реальные 8s/30fps/240-frame MP4: out/demo-vertical.mp4 (1080×1920), demo-wide.mp4 (1920×1080), demo-square.mp4 (1080×1080), demo-animatic.mp4 (960×540).
- Native smoke — 2s/30fps/60 frames, 426×240 actual export; native source author canvas 640×360. Native filmstrip и preview реально просмотрены.
- Первоначальный vertical 540×960 retained; две critique итерации и последующее исправление wide readability. Read docs/TESTING.md, PERFORMANCE.md и reviews/iteration-*.md. Final scores не изображают независимую production acceptance.
- Облачная диагностика: Debian13/x86_64/glibc2.41, 3 CPU, ~9.7GiB RAM, без hardware GPU; benchmark wall/CPU/process-tree RSS сохранён с оговорками метода.
- Нет реальной narration/brand assets, поэтому faithful scientific/voice review и audio audition настоящей речи ещё не выполнены. Автотест source/AAC использует явно обозначенный pulse WAV, не выдуманную speech.
- Нет обязательных платных API, transcription/forced alignment модели и 3D-зависимости не добавлялись. Сложные одобренные сцены пишутся Astra на готовом renderer, либо native Tesseract; footage при необходимости импортируется реально.
- Ресурсы текущей среды ephemeral. Setup/startup scripts и dependency lockfiles сохранены; host package requirements и Cloud UI setup/maintenance commands в CODEX_CLOUD.md. Мы не можем утверждать, что интерфейс конфигурации Codex Cloud уже изменён.

Следующее необходимое действие: получить настоящие озвучку и референсы, провести Gate 1, затем создать пользовательский фильм на этой инфраструктуре. Повторная установка в текущем сеансе не нужна, если startup checks проходят.


Container limits measured from /sys/fs/cgroup: cpu.max = 200000 100000 (2 CPU quota), memory.max = 8589934592 (8 GiB). nproc reports 3 available affinity CPUs and free reports ~9.7 GiB host-visible memory; effective container capacity is 2 CPU / 8 GiB, not those larger host/affinity figures. FFmpeg uses 3 threads within that quota.

Финальная верификация: 13 тестов passed/0 failed; полная setup-команда выполнена end-to-end, повторный startup прошёл. Все четыре delivery format прошли mechanical quality gates. Видеофайлы и review evidence сохранены в Git вместе с `.tsrct`; cache frames и runtime downloads исключены. Отдельный `out/demo-sfx.mp4` — реально смонтированные короткие диагностические SFX, не музыка и не дикторская речь.
