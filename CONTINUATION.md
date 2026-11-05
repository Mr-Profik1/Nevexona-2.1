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
