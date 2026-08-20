# Gamer Factory Clips Agent

MVP para generar, evaluar y registrar videos cortos de Gamer Factory usando OpenAI + MoneyPrinterTurbo.

## Objetivo

Automatizar el ciclo inicial:

1. Generar ideas de contenido.
2. Elegir las mejores.
3. Crear guiones y keywords.
4. Ejecutar MoneyPrinterTurbo por CLI.
5. Guardar cada experimento en SQLite.
6. Dejar los videos listos para revisión humana.

La publicación automática y el loop de analytics se agregan después de validar calidad.

## Requisitos

- Windows o macOS.
- Python 3.11+.
- `uv` instalado.
- MoneyPrinterTurbo instalado y ya configurado localmente.
- Variables de entorno de OpenAI configuradas.

MoneyPrinterTurbo se ejecuta mediante su helper oficial `docs/skill/mpt_agent.py`, siguiendo el flujo recomendado por el proyecto.

## Configuración rápida

1. Copiar `.env.example` a `.env`.
2. Completar `OPENAI_API_KEY`.
3. Ajustar `MPT_SKILL_DIR` para que apunte a la carpeta `docs/skill` de tu instalación local de MoneyPrinterTurbo.
4. Revisar `config/settings.yaml`.
5. Ejecutar:

```bash
uv run python -m src.main
```

Por defecto el MVP genera ideas y guiones, registra todo en SQLite y deja `auto_publish: false`.

## Seguridad

Nunca subir API keys, tokens ni el `config.toml` de MoneyPrinterTurbo al repositorio.
