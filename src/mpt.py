from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


def render_video(subject: str) -> str:
    skill_dir_raw = os.getenv("MPT_SKILL_DIR")
    if not skill_dir_raw:
        raise RuntimeError("Falta MPT_SKILL_DIR en .env")

    skill_dir = Path(skill_dir_raw).expanduser().resolve()
    helper = skill_dir / "mpt_agent.py"
    if not helper.exists():
        raise FileNotFoundError(f"No se encontró mpt_agent.py en {skill_dir}")

    cmd = [
        "uv",
        "run",
        "--no-project",
        "--python",
        "3.11",
        "python",
        "mpt_agent.py",
        "--subject",
        subject,
    ]

    completed = subprocess.run(
        cmd,
        cwd=skill_dir,
        capture_output=True,
        text=True,
        timeout=30 * 60,
        check=False,
    )

    output = (completed.stdout or "") + "\n" + (completed.stderr or "")
    if completed.returncode != 0:
        tail = "\n".join(output.splitlines()[-25:])
        raise RuntimeError(f"MoneyPrinterTurbo falló (exit {completed.returncode}):\n{tail}")

    match = re.search(r"^VIDEO_FILE=(.+)$", output, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("MoneyPrinterTurbo terminó sin informar VIDEO_FILE")

    return match.group(1).strip()
