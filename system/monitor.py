#!/usr/bin/env python3
"""Системный монитор: реальные данные из /proc. Запуск: nevexona-monitor"""
import os, shutil

def meminfo(path="/proc/meminfo"):
    d = {}
    for line in open(path):
        k, v = line.split(":")
        d[k] = int(v.split()[0]) * 1024
    used = d["MemTotal"] - d["MemAvailable"]
    return {"total": d["MemTotal"], "used": used, "percent": round(used * 100 / d["MemTotal"], 1)}

def disk(path="/"):
    u = shutil.disk_usage(path)
    return {"total": u.total, "used": u.used, "percent": round(u.used * 100 / u.total, 1)}

def load():
    return os.getloadavg()

def main():
    m, d = meminfo(), disk()
    print(f"RAM: {m['used']//2**20} / {m['total']//2**20} МБ ({m['percent']}%)")
    print(f"Диск /: {d['used']//2**30} / {d['total']//2**30} ГБ ({d['percent']}%)")
    print("Нагрузка:", " ".join(f"{x:.2f}" for x in load()))

if __name__ == "__main__":
    main()
