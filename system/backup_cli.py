#!/usr/bin/env python3
"""Запуск: backup_cli.py <папка_назначения> <источник>... — делает копию и проверяет целостность."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from system import backup

def main(argv):
    if len(argv) < 3: print("usage: backup_cli.py DEST SRC..."); return 2
    backup.backup(argv[2:], argv[1]); bad = backup.verify(argv[1])
    print("OK" if not bad else "ПОВРЕЖДЕНЫ: " + ", ".join(bad)); return 0 if not bad else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
