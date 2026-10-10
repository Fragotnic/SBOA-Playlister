"""
Hauptskript für den Add-on-Betrieb: gleicht die Deezer-Playlist des
aktuellen Festivaljahres mit der Summer-Breeze-Bandliste ab. Wird
von run.sh einmal täglich aufgerufen.

Für jedes Festivaljahr wird eine eigene Playlist (z.B. SBOD2027) und
ein eigener Zustand (state_<jahr>.json unter /data/state) geführt.
Taucht ein neues Jahr auf (nächste Festivalausgabe), wird
automatisch eine neue, leere Playlist dafür angelegt - die Playlist
des Vorjahres bleibt unverändert erhalten.
"""
import json
import os
import pathlib
import sys

from scraper import fetch_bands_and_year
from deezer_client import DeezerPlaylist, top_tracks_for_band

STATE_DIR = pathlib.Path(os.environ.get("STATE_DIR", "/data/state"))
STATE_DIR.mkdir(parents=True, exist_ok=True)

ACCESS_TOKEN = os.environ.get("DEEZER_ACCESS_TOKEN", "")
PLAYLIST_PREFIX = os.environ.get("PLAYLIST_PREFIX", "SBOD")
BANDS_URL = os.environ.get("BANDS_URL") or None


def load_json(path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    if not ACCESS_TOKEN:
        sys.exit("Kein DEEZER_ACCESS_TOKEN gesetzt. Bitte in den Add-on-Optionen eintragen.")

    print("Lade Bandliste und Festivaljahr ...")
    current_bands, year = fetch_bands_and_year(BANDS_URL) if BANDS_URL else fetch_bands_and_year()
    current_bands = set(current_bands)

    playlist_title = f"{PLAYLIST_PREFIX}{year}"
    state_path = STATE_DIR / f"state_{year}.json"
    state = load_json(
        state_path, {"playlist_id": None, "playlist_title": playlist_title, "bands": {}}
    )

    playlist = DeezerPlaylist(ACCESS_TOKEN)

    if not state.get("playlist_id"):
        state["playlist_id"] = playlist.create_playlist(playlist_title)
        state["playlist_title"] = playlist_title
        print(f"Neue Playlist für {year} angelegt: '{playlist_title}' (ID {state['playlist_id']})")

    playlist_id = state["playlist_id"]
    known_bands = set(state["bands"].keys())

    new_bands = sorted(current_bands - known_bands)
    removed_bands = sorted(known_bands - current_bands)

    print(
        f"Festival {year}: {len(current_bands)} Bands angekündigt "
        f"({len(new_bands)} neu, {len(removed_bands)} entfernt)."
    )

    for band in removed_bands:
        track_ids = state["bands"].pop(band, [])
        if track_ids:
            print(f"- Entferne '{band}' ({len(track_ids)} Tracks)")
            playlist.remove_tracks(playlist_id, track_ids)

    for band in new_bands:
        tracks = top_tracks_for_band(band, limit=3)
        if not tracks:
            print(f"! Kein Deezer-Künstler gefunden für '{band}', übersprungen.")
            continue
        track_ids = [t["id"] for t in tracks]
        print(f"+ Füge '{band}' hinzu: {[t['title'] for t in tracks]}")
        playlist.add_tracks(playlist_id, track_ids)
        state["bands"][band] = track_ids

    save_json(state_path, state)
    print("Fertig.")


if __name__ == "__main__":
    main()
