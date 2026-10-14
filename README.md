# ZNAYA Motion Studio

Готовый воспроизводимый Codex-конвейер: TypeScript seek(t), аналитические springs, Playwright → PNG → FFmpeg, voiceover-first, reference/storyboard workflows, обязательные review artifacts и настоящий Mirage Tesseract 0.3.1 на Vulkan lavapipe. Только технические композиции; настоящий ролик ZNAYA не создан. Фоновая музыка отсутствует.

Начните с [инструкции Astra](docs/ASTRA_HANDOFF.md), [API](docs/TOOLS_API.md) и [облачного восстановления](docs/CODEX_CLOUD.md).

```bash
bash scripts/setup.sh         # новая Debian 13 cloud-среда с описанными host dependencies
npm run check                 # текущая среда: реальный Chromium и Vulkan preview
npm run typecheck
npm test                      # включая реальный MP4 и audio-clock тесты
npm run preview               # entry/hold/exit кадры технических сцен
npm run render -- --format vertical --name demo-vertical
npm run render -- --format wide --name demo-wide
npm run render -- --format square --name demo-square
npm run render -- --format animatic --name demo-animatic
npm run tesseract             # настоящий нативный .tsrct и MP4
```

Первый настоящий проект после загрузки ваших материалов:

```bash
npm run new -- "Тема или готовый сценарий" --voiceover assets/audio/voiceover.mp3 --format vertical --reference assets/references/my-reference --id first-film
```

В Codex: `$znaya-motion-studio "Тема или сценарий" --voiceover assets/audio/voiceover.mp3 --format vertical --reference assets/references/my-reference`. Custom slash-команда не зарегистрирована. Intake создаёт проект и останавливает зависимую работу на Gate 1; Astra проверяет реальные материалы, получает необходимые approvals и пишет композицию. Эта команда не выдумывает готовый фильм.

После реализации и утверждения композиции:

```bash
npm run render -- --project projects/first-film/project.json --format vertical --name first-film-vertical
```

Все кадры вычисляются независимо. `--start 2 --end 3` рендерит фрагмент; `--patch --ranges 0:0.4,2.1:2.5 --name demo-vertical` заменяет локальные кадры в существующем cache и пересобирает полный MP4 с новым review. Cache не хранится в Git; его создаёт полный рендеринг.

Реальные результаты: [вертикальный MP4](out/demo-vertical.mp4), [wide](out/demo-wide.mp4), [square](out/demo-square.mp4), [animatic](out/demo-animatic.mp4), [native MP4](out/native-smoke.mp4), [native editable .tsrct](out/native-smoke.tsrct), [browser adapter .tsrct](out/browser-adapter.tsrct), [contact sheet](reviews/demo-vertical/contact-sheet.png), [визуальные итерации](reviews/iteration-01.md), [результаты тестов](reviews/tests-output.txt). Для native browser adapter Canvas-графика остаётся растром; редактируемы добавленные native слои.

Расположение: `src/` math/renderer/types; `scenes/` зарегистрированные композиции; `assets/` шрифты, исходное аудио и references; `projects/` независимые briefs/timelines; `templates/` production документы; `skills/` reusable skill и pinned официальные Tesseract skills; `.agents/skills/` Codex discovery; `scripts/` установка, экспорт, анализ, critic; `reviews/` реальные evidence/дефекты/метрики; `out/` MP4/PNG/.tsrct; `tests/` регрессии; `.codex/` cloud setup/startup команды.

Ограничения: CPU rendering, нет supplied narration/brand/scientific assets; diagnostic audio — импульсы, не речь. Семантический reference review и научная проверка выполняются Astra по реальным изображениям/источникам. Forced alignment — ручные timestamps или подключаемый локальный aligner; платные API не нужны. 8/10 художественное качество не сертифицировано модельной самооценкой. Смотри [проверки](docs/TESTING.md), [сервер](docs/environment_report.md), [benchmark](docs/PERFORMANCE.md).
