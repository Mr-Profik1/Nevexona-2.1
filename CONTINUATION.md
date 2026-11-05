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
