# Summer Breeze Deezer Sync – Home Assistant Add-on

Home-Assistant-Add-on, das täglich automatisch eine Deezer-Playlist
mit den Top-3-Tracks aller aktuell angekündigten Summer-Breeze-Bands
pflegt. Für jedes Festivaljahr wird automatisch eine eigene, neue
Playlist angelegt (z.B. `SBOD2027`, im nächsten Jahr `SBOD2028`, ...),
die Playlist des Vorjahres bleibt dabei unverändert erhalten.

## Installation

1. Diesen Ordner in ein eigenes Git-Repository packen (z.B. auf
   GitHub) und pushen. Home Assistant liest Add-on-Repositories
   direkt aus Git.
2. In Home Assistant: **Einstellungen -> Add-ons -> Add-on-Store ->
   ⋮ (oben rechts) -> Repositories** -> die URL deines Repos
   eintragen -> Hinzufügen.
3. Das Add-on "Summer Breeze Deezer Sync" erscheint danach im
   Store -> installieren.
4. **Vor dem Start:** Einmalig einen Deezer-Access-Token besorgen
   (Anleitung in `summer_breeze_deezer_sync/DOCS.md`, dort auch als
   "Dokumentation"-Tab im Add-on selbst sichtbar) und in der
   Add-on-Konfiguration eintragen.
5. Add-on starten. Beim ersten Lauf wird sofort die Playlist für das
   aktuelle Festivaljahr angelegt, danach läuft der Abgleich
   automatisch einmal täglich zur eingestellten Uhrzeit.

## Ordnerstruktur

- `repository.yaml` – macht diesen Ordner als HA-Add-on-Repository
  erkennbar
- `summer_breeze_deezer_sync/` – das eigentliche Add-on (Dockerfile,
  Konfiguration, Skripte)
- `oauth_get_token.py` – **lokal auf deinem PC** (nicht im Add-on)
  einmalig auszuführen, um einen Deezer-Access-Token zu erhalten
