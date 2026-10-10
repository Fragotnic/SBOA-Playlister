# Summer Breeze Deezer Sync

Dieses Add-on hält eine Deezer-Playlist automatisch synchron mit der
aktuellen Bandliste des Summer Breeze Open Air
(https://www.summer-breeze.de/de/bands/). Einmal täglich wird
geprüft:

- **Neue Bands** -> ihre laut Deezer beliebtesten 3 Tracks werden
  der Playlist hinzugefügt.
- **Abgesagte/entfernte Bands** -> ihre Tracks werden wieder
  entfernt.
- **Neues Festivaljahr** (z.B. wechselt die Ankündigung von 2027 auf
  2028) -> es wird automatisch eine neue, eigene Playlist angelegt
  (z.B. `SBOD2028`), die Playlist des Vorjahres bleibt unverändert
  bestehen.

## Voraussetzung: Deezer-Access-Token

Das Add-on kann selbst keinen Login-Dialog anzeigen. Du musst dir
daher einmalig auf deinem PC einen Deezer-Access-Token besorgen:

1. App unter https://developers.deezer.com/myapps registrieren
   (als Redirect-URI z.B. `http://localhost:8888/callback`
   eintragen).
2. Das im Repository mitgelieferte Skript `oauth_get_token.py`
   (außerhalb des Add-ons, lokal bei dir) ausführen:
   ```
   pip install requests
   DEEZER_APP_ID=... DEEZER_APP_SECRET=... python oauth_get_token.py
   ```
3. Den ausgegebenen Access-Token in die Add-on-Konfiguration unter
   `deezer_access_token` eintragen.

## Konfiguration

| Option | Beschreibung |
|---|---|
| `deezer_access_token` | Dein Deezer-Access-Token (siehe oben) |
| `playlist_prefix` | Präfix für den Playlistnamen, z.B. `SBOD` -> Playlist heißt `SBOD2027` |
| `bands_url` | URL der Bandseite (im Normalfall nicht ändern) |
| `sync_hour` | Uhrzeit (0-23) der täglichen Aktualisierung, in der Systemzeit von Home Assistant |

## Logs

Im Log des Add-ons siehst du bei jedem Lauf, welche Bands neu
hinzugekommen sind, welche entfernt wurden, und ob eine neue
Playlist für ein neues Festivaljahr angelegt wurde.

## Bekannte Einschränkungen

- Für manche Bands (Tribute-/Sonderprojekte) findet die automatische
  Künstlersuche eventuell keinen oder den falschen Deezer-Künstler;
  solche Fälle werden im Log mit `!` markiert.
- Deezer-Access-Tokens können irgendwann ungültig werden; schlägt
  der Sync mit einem Auth-Fehler fehl, Schritt 2 oben wiederholen
  und den Token in der Konfiguration erneuern.
