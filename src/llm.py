from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = yaml.safe_load((ROOT / "config" / "settings.yaml").read_text(encoding="utf-8"))
CLIENT = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _read_prompt(name: str) -> str:
    return (ROOT / "prompts" / name).read_text(encoding="utf-8")


def _json_response(prompt: str) -> Any:
    response = CLIENT.responses.create(
        model=MODEL,
        input=prompt,
    )
    text = response.output_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].lstrip()
    return json.loads(text)


def generate_ideas() -> list[dict[str, Any]]:
    count = SETTINGS["content"]["ideas_per_run"]
    categories = ", ".join(SETTINGS["content"]["categories"])
    prompt = _read_prompt("strategist.md") + f"\n\nGenerá exactamente {count} ideas. Categorías permitidas: {categories}. Devolvé un array JSON, sin markdown."
    result = _json_response(prompt)
    if not isinstance(result, list):
        raise ValueError("El estratega no devolvió un array JSON")
    return result


def generate_script(idea: dict[str, Any]) -> dict[str, Any]:
    prompt = _read_prompt("script.md") + "\n\nIdea seleccionada:\n" + json.dumps(idea, ensure_ascii=False)
    result = _json_response(prompt)
    if not isinstance(result, dict) or "script" not in result:
        raise ValueError("El generador de guion devolvió un formato inválido")
    return result
