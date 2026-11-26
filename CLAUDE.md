# meine-app

Regeln für alle KI-Agenten stehen in [`AGENTS.md`](AGENTS.md).

Diese App läuft auf LayerNX Deploy und folgt dem App-Standard 1.

## Eckdaten

- App: `meine-app` (Art `web`), Einstieg `app.main:app` (ASGI).
- Health-Pfad: `GET /healthz` antwortet `200` und `{"status": "ok"}`.
- Datenordner: `DATA_DIR`; bleibt bei jedem Deploy erhalten.
- Prüfen: `uv run ruff check .` und `uv run pytest`.

## Regeln

- Halte dich an den LayerNX App-Standard 1; ändere `layernx.toml` nur, wenn nötig, und prüfe mit `lnxdeploy check`.
- Backend nur Python (FastAPI empfohlen). Kein PHP, kein Node zur Laufzeit.
- Daten nur in `DATA_DIR` oder in der Datenbank. Keine festen Pfade, Ports, Hostnamen.
- Konfiguration nur über Umgebungsvariablen in `app/config.py`.
- Jede Änderung mit Test; `pytest` muss grün sein.
- Migrationen rückwärtskompatibel (erst hinzufügen, später entfernen).
- Keine Inline-Skripte und keine Inline-Styles; keine externen Quellen (CDN).
- Den Pfad `/_lnxd/` nicht benutzen, er gehört LayerNX Deploy.
- Hintergrundarbeit als `[[worker]]` oder `[[cron]]` im Manifest, nie als Thread in der Web-App.
- Lokal starten: `lnxdeploy dev` oder `uv run uvicorn app.main:app --reload`.
- Deployen: `lnxdeploy deploy` bzw. Push auf den Branch; live schalten macht ein Mensch im Panel.
