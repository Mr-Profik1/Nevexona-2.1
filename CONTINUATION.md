# CONTINUATION

## Этап 2 (в процессе): каркас Core ISO — DEV 0.1.0
Сделано:
- структура каталогов, LICENSE (MIT), .gitignore, .env.example
- scripts/build-iso.sh (Debian Live Build, trixie, amd64, GRUB BIOS+UEFI)
- workflows: checks.yml (shellcheck + тесты), build-iso.yml (ручной запуск, ISO+SHA256+лог как Artifact)
- branding: простой знак N (SVG/PNG/ICO), палитра Minimal Orange
- tests/run_tests.py (структура, брендинг, секреты, синтаксис shell, YAML)

НЕ сделано / не проверено:
- ISO ни разу не собиралась; параметры `lb config` и имена пакетов не проверены сборкой
- версии Actions (checkout@v4, upload-artifact@v4) и лимиты нужно сверить
- рабочий стол, приложения, драйверы, голос, AI, антивирус, игры, установщик — только заглушки README
- загрузка на физический ПК / VM не проверялась

## Следующий шаг
Запустить Actions → Build ISO, прислать лог ошибки, исправить конфигурацию.

## Известные проблемы
- Нет проверки в реальной среде (в среде разработки нет live-build и сети для установки).

## Этап 3 (DEV 0.2.0): рабочий стол и первые модули
Сделано (код + тесты): voice/intents.py (белый список, подтверждения, без shell), security/quarantine.py,
system/backup.py (манифест SHA256, проверка, восстановление), system/monitor.py.
Рабочий стол: конфиги Openbox/tint2 (Minimal Orange), обои, lightdm; пакеты добавлены в core.list.chroot.
Первая сборка Core ISO прошла в Actions (1.26 GB в Artifact); загрузка на ВМ/ПК НЕ проверена.
НЕТ: GUI-приложений (Explorer-окно, Settings, Security/Voice GUI), распознавание речи, ClamAV-интеграция,
Game Hub, установщик, Android (Waydroid) — только план. Голос: нет STT-движка, только разбор команд.
Тема Openbox/tint2 и имена пакетов проверяются очередной сборкой.

## Driver Center (логика)
drivers/detect.py: разбор `lspci -nnk`, производитель, драйвер, статус, предлагаемый firmware-пакет Debian. Тест на образце.
НЕТ: установка пакетов с журналом и предупреждением, USB-устройства, GUI.

## Game Hub (логика)
gaming/hub.py: библиотека (Steam appmanifest + свои игры), запуск без shell, каталог платформ с честными статусами.
Roblox: официально не поддерживается на Linux — не обещаем. Steam/Wine ставятся по кнопке (apt, i386) — установка ещё не реализована.
Название системы в os-release/issue: NEVEXONA 2.1 GAMING (ядро остаётся Linux; ID=debian оставлен для совместимости пакетов).
НЕТ: GUI Game Hub, установка платформ, Proton-версии, профили, мониторинг FPS, бэкап сохранений.

## NEVEXONA Android (логика)
gaming/android.py: обёртка Waydroid (установка APK, запуск, список, проверка требований). Тесты есть.
НЕТ: пакет waydroid в ISO/установка по кнопке, GUI-окно, магазин; на X11 Waydroid не работает без Wayland-композитора.
НЕ обещаем: «не вылетает» — стабильность проверяется только тестами на ВМ/железе.

## Update Center (логика)
system/updater.py: проверка последнего GitHub Release, загрузка .deb, проверка SHA256, установка только с подтверждением (pkexec apt).
НЕТ: упаковка NEVEXONA в .deb, workflow публикации релиза (.deb + .sha256), кнопка в Settings, загрузка файла, APT-репозиторий.
Обновление ядра/firmware — через обычный APT Debian. «Установка онлайн в стиле установщика» — ещё не реализована (Calamares не подключён).

## Control Center (DEV 0.3.0)
apps/panels.py (данные вкладок, тесты) + apps/control_center.py (Tk-окно: Монитор, Драйверы, Игры, Безопасность, Голос, Обновления).
GUI НЕ запускалась ни разу: в среде разработки нет tkinter. Проверено только py_compile и тестами panels. Первый запуск — на ВМ после сборки.
Ярлык в меню и на панели добавлены. Микрофон/STT не подключены.

## Оформление в стиле Windows (по референсам пользователя)
Панель tint2 48px с кнопкой «Пуск» (jgmenu, тема Minimal Orange), новые обои (свечение и лучи только в обоях).
НЕ проверено: параметры jgmenurc и работа кнопки «Пуск» — проверяются на ВМ. Иконки приложений пока системные.

## Сайт и публикация ISO
site/index.html (скачивание, инструкция EtchDroid/Rufus/balenaEtcher), .github/workflows/pages.yml (GitHub Pages).
Build ISO: input publish=true публикует ISO + .sha256 в Releases (softprops/action-gh-release@v2; версия экшена не сверена с актуальной).
Нужно включить Pages: Settings → Pages → Source: GitHub Actions. Лимит файла в Release — 2 GB.

## Оптимизация под 2 ГБ ОЗУ (DEV 0.4.0)
zram-tools (zstd, 50%), sysctl (swappiness, cache pressure), хук отключения фоновых таймеров в Live, профили производительности (system/profiles.py, вкладка «Профиль»).
Реальный расход ОЗУ НЕ измерен: нужна загрузка ISO на ВМ с 2 ГБ и замер `free -m` после входа. Firefox на 2 ГБ тяжёлый.

## Пакет функций (DEV 0.5.0)
network/center.py (Wi-Fi nmcli, Bluetooth bluetoothctl), laptop/center.py (батарея, яркость), security/scanner.py (ClamAV, отчёт),
system/files.py (копия, перенос, поиск, корзина freedesktop), system/display.py (масштаб 100–200%). Тесты: tests/test_features.py. Вкладки Сеть/Ноутбук/Масштаб в Control Center.
НЕ проверено на железе: nmcli/bluetoothctl/ClamAV в Live, GUI-вкладки, запись яркости (нужны права).

## Расширенный набор (extras.list.chroot)
Офис (LibreOffice), VLC, GIMP, Python dev, git, htop и др. Ожидаемый размер ISO ~2.0–2.5 ГБ (оценка, не измерено).
ВАЖНО: файл в GitHub Releases не может быть больше 2 ГБ. При превышении публикация релиза упадёт — ISO останется в Artifacts (в ZIP).
Не добавлено намеренно: Wine/Steam (нужен i386 multiarch в live-build, риск сломать сборку) — ставятся из Game Hub по выбору.
Имена пакетов проверяются только реальной сборкой.

## Драйверы в ISO (drivers.list.chroot)
Firmware Intel/Realtek/Atheros/Broadcom/MediaTek/AMD, микрокод CPU, видеодрайверы Xorg (включая nouveau для старых NVIDIA), Mesa/Vulkan, PipeWire, принтеры/сканеры, ntfs/exfat, gparted, VPN, pciutils (нужен Driver Center).
Проприетарный драйвер NVIDIA НЕ включён (ставится по выбору). Publish release теперь continue-on-error (лимит 2 ГБ).
Ожидаемый размер ISO ~2.5–3 ГБ — оценка, измерить после сборки.

## Пакет «всё остальное» (DEV 0.6.0)
gaming/platforms.py (установка Steam/Lutris/Wine/Java с подтверждением и i386), system/updater.download, voice/stt.py (Vosk, модель только по согласию),
ai/assistant.py (LOCAL/CLOUD/AUTO, ключ 0600, согласие перед облаком), установщик: пакеты calamares + calamares-settings-debian (НЕ проверен, брендинг не настроен).
Вкладки «Ассистент», кнопки установки платформ. Не проверено: имена пакетов (wine, calamares-settings-debian), GUI, vosk (нужен pip install vosk), llama-cli в ISO нет.
Нет: локальная LLM в ISO (качается пользователем), Explorer/Settings/Game Hub как отдельные окна, окно записи микрофона.

## Отдельные окна (DEV 0.7.0)
apps/explorer.py (+explorer_core, тесты), apps/game_hub.py, apps/settings.py, apps/theme.py; запуск: nevexona-explorer / -gamehub / -settings; .desktop-файлы для меню.
GUI не запускалась на экране (нет tkinter в среде разработки) — проверены только компиляция и логика. Следующий шаг: ВМ, скриншоты, правки.
Нет: окно записи микрофона, настройка Calamares, локальная LLM в ISO.

## DEV 0.8.0
system/schedule.py + backup_cli.py (расписание бэкапов, systemd user timer), security/integrity.py (эталон SHA256 + автозапуск), scanner.usb_mounts,
system/monitors.py (xrandr), gaming/proton.py (версии Proton, бэкап сохранений), voice/session.py + apps/voice_window.py (микрофон только по кнопке, индикатор),
apps/backup.py, экран входа (lightdm-gtk-greeter), dunst, volumeicon, blueman-applet, тёмная тема GTK.
Roblox: через Waydroid не гарантирован (защита от эмуляторов).
НЕ сделано: Plymouth (загрузочный экран), окно мониторов, ваш логотип, настройка Calamares, локальная LLM, проверка на экране/железе.

## Брендинг (DEV 0.9.0)
Собственный логотип N (оранжевый + светлая вертикаль, наклон), все форматы в branding/ (svg, png, ico, favicon, boot/installer logo, mark.png), новые обои, загрузочный экран Plymouth (тема nevexona, хук 0200, пакет plymouth).
Plymouth/хук не проверены на загрузке. Если у пользователя есть собственный логотип — заменить branding/logo.svg и пересобрать png/ico.
