#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


MIN_VERSION = (3, 11)
MAX_VERSION = (3, 13)
PYTHON_CANDIDATES = ("python3.11", "python3.12", "python3.10", "python")


def version_supported(version: tuple[int, int]) -> bool:
    return MIN_VERSION <= version < MAX_VERSION


def reexec_with_supported_python() -> None:
    if os.environ.get("PROTOTYPE2_PYTHON_REEXEC") == "1":
        return

    for candidate in PYTHON_CANDIDATES:
        executable = shutil.which(candidate)
        if not executable:
            continue

        try:
            output = subprocess.check_output(
                [
                    executable,
                    "-c",
                    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
                ],
                text=True,
            ).strip()
            major, minor = (int(part) for part in output.split(".", 1))
        except Exception:
            continue

        if version_supported((major, minor)):
            env = os.environ.copy()
            env["PROTOTYPE2_PYTHON_REEXEC"] = "1"
            os.execve(executable, [executable, *sys.argv], env)


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run(command: list[str], cwd: Path) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.check_call(command, cwd=str(cwd))


def main() -> int:
    current_version = (sys.version_info.major, sys.version_info.minor)
    if not version_supported(current_version):
        reexec_with_supported_python()
        print(
            "Prototype requires Python 3.10, 3.11, or 3.12. "
            "Python 3.11 is recommended because the camera pipeline uses MediaPipe.",
            file=sys.stderr,
        )
        print("Install Python 3.11, then run: python3.11 run_prototype.py", file=sys.stderr)
        return 1

    root = Path(__file__).resolve().parent
    venv_dir = root / ".venv"
    python = venv_python(venv_dir)

    if not python.exists():
        run([sys.executable, "-m", "venv", str(venv_dir)], root)

    run([str(python), "-m", "pip", "install", "--upgrade", "pip"], root)
    run([str(python), "-m", "pip", "install", "-r", str(root / "requirements.txt")], root)

    run([str(python), "-m", "project_database.create_tables"], root)
    os.execv(str(python), [str(python), "-m", "bridge.bridge", *sys.argv[1:]])  

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
