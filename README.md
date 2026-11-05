# NEVEXONA 2.1

Лёгкая Linux-система на базе Debian 13 (Trixie), amd64. Статус: **DEV 0.1.0 — ранняя разработка**.
Сейчас в репозитории только каркас сборки Live ISO (Core). ISO ещё **не собиралась и не проверялась на ПК**.

См. `CONTINUATION.md` — что сделано, что нет, известные проблемы.

## Сборка ISO
GitHub → Actions → **Build ISO** → Run workflow. Результат (ISO, SHA256, логи) — в Artifacts.

## Локальные проверки
```
python3 tests/run_tests.py
```
