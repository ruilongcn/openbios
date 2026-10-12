# -*- coding: utf-8 -*-
"""启动脚本：创建/复用虚拟环境、安装依赖、启动 Uvicorn。"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = ROOT / ".venv"
PYTHON = VENV_DIR / "Scripts" / "python.exe" if sys.platform == "win32" else VENV_DIR / "bin" / "python"


def ensure_venv():
    if not (VENV_DIR / "pyvenv.cfg").exists():
        print("[start] 创建虚拟环境 ...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    if not PYTHON.exists():
        raise RuntimeError("虚拟环境 Python 不存在，请检查 .venv")


def ensure_deps():
    print("[start] 检查/安装依赖 ...")
    subprocess.run([str(PYTHON), "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8002)
    parser.add_argument("--skip-install", action="store_true")
    args = parser.parse_args()

    ensure_venv()
    if not args.skip_install:
        ensure_deps()

    print(f"[start] 启动服务: http://{args.host}:{args.port}")
    cmd = [str(PYTHON), "-m", "uvicorn", "web.main:app", "--host", args.host, "--port", str(args.port), "--app-dir", str(ROOT)]
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
