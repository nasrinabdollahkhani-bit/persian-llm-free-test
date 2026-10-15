#!/usr/bin/env python3
"""Dependency-free, non-executing capacity check for a temporary public CI runner.

Does not download models, install packages, or contact external services.
Does not assert private-lab, air-gap, or Windows security readiness.
"""
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone

GIB = 1024 ** 3


def meminfo():
    data = {}
    with open("/proc/meminfo", encoding="utf-8") as f:
        for line in f:
            key, value = line.split(":", 1)
            data[key] = int(value.split()[0]) * 1024
    return data


def cgroup_limit():
    for name in ("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        if os.path.isfile(name):
            text = open(name, encoding="utf-8").read().strip()
            if text.isdecimal():
                num = int(text)
                if num < 2**60:
                    return num
    return None


def main():
    mem = meminfo()
    limit = cgroup_limit()
    disk = shutil.disk_usage(os.getcwd())
    cpu = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count()
    effective_available = min(mem["MemAvailable"], limit) if limit else mem["MemAvailable"]
    checks = {
        "linux_x64": platform.system() == "Linux" and platform.machine().lower() in ("x86_64", "amd64"),
        "cpu_at_least_4": cpu >= 4,
        "available_memory_at_least_8_gib": effective_available >= 8 * GIB,
        "disk_free_at_least_5_gib": disk.free >= 5 * GIB,
    }
    output = {
        "schema": "public.synthetic.runner-preflight.v1",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "cpu_affinity_count": cpu,
        "memory_total_gib": round(mem["MemTotal"] / GIB, 3),
        "memory_available_gib": round(mem["MemAvailable"] / GIB, 3),
        "effective_memory_limit_gib": round(limit / GIB, 3) if limit else None,
        "disk_free_gib": round(disk.free / GIB, 3),
        "checks": checks,
        "capacity_preflight": "PASS" if all(checks.values()) else "BLOCKED",
        "downloads": "NOT_EXECUTED",
        "model_execution": "NOT_EXECUTED",
        "windows_native": "NOT_EXECUTED",
        "is_private_or_air_gapped": False,
    }
    with open("preflight.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    sys.exit(main())
