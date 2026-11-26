# LNX Deploy Beispiel-App

Eine FastAPI-Beispiel-App für LayerNX Deploy. Sie zeigt einen persistenten
SQLite-Zähler mit HTMX und einen Healthcheck unter `/healthz`.

## Lokal starten

Voraussetzungen sind Python 3.13 oder neuer und [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked
uv run uvicorn app.main:app --reload
```

Die App ist unter http://127.0.0.1:8000 erreichbar. Lokal legt sie die
SQLite-Datei standardmäßig in `.data/` ab.

## Auf LayerNX Deploy bereitstellen

Verbinde dieses Repository in LayerNX Deploy mit dem Branch `main`. Das
Manifest `layernx.toml` beschreibt den Einstiegspunkt, den persistenten
Datenordner und den Healthcheck. Wenn LayerNX eine MariaDB zuweist, prüft
`/healthz` auch deren Erreichbarkeit. Der Zähler nutzt SQLite.

Setze Zugangsdaten wie `DB_PASSWORD` und `SECRET_KEY` in der Laufzeitumgebung.
Für Beispiele kannst du reservierte Werte wie `https://app.example.com` und
`beispiel@example.com` verwenden.

## Prüfen

```sh
uv run ruff check .
uv run pytest
```

Die Python-Vorlage steht unter MIT. Die Lizenzhinweise für HTMX und die
Schriftarten liegen bei den jeweiligen Dateien unter `app/static/`.
