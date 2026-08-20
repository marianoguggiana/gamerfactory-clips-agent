from __future__ import annotations

from src.llm import SETTINGS, generate_ideas, generate_script
from src.mpt import render_video
from src.storage import init_db, mark_rendered, save_experiment


def rank_ideas(ideas: list[dict]) -> list[dict]:
    def score(item: dict) -> float:
        viral = float(item.get("viral_score", 0))
        commercial = float(item.get("commercial_relevance", 0))
        return viral * 0.7 + commercial * 0.3

    return sorted(ideas, key=score, reverse=True)


def main() -> None:
    init_db()

    ideas = generate_ideas()
    selected_count = int(SETTINGS["content"]["selected_per_run"])
    selected = rank_ideas(ideas)[:selected_count]

    print(f"Generadas {len(ideas)} ideas; seleccionadas {len(selected)}.")

    for index, idea in enumerate(selected, start=1):
        script_data = generate_script(idea)
        experiment = {
            **idea,
            "script": script_data["script"],
            "keywords": script_data.get("keywords", []),
            "metadata": {"cta": script_data.get("cta")},
            "status": "scripted",
        }
        experiment_id = save_experiment(experiment)

        print(f"[{index}/{len(selected)}] Renderizando: {idea['topic']}")
        video_path = render_video(script_data["script"])
        mark_rendered(experiment_id, video_path)
        print(f"Listo: {video_path}")

    print("MVP finalizado. Los videos quedaron registrados para revisión manual.")


if __name__ == "__main__":
    main()
