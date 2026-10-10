"""
Kleiner Client für die Deezer Web API: Künstler-/Track-Suche und
Playlist-Verwaltung (letzteres erfordert einen User-Access-Token mit
'manage_library'-Recht).
"""
import time
import requests

API_BASE = "https://api.deezer.com"


class DeezerError(RuntimeError):
    pass


def _check(data):
    if isinstance(data, dict) and "error" in data:
        raise DeezerError(data["error"])
    return data


def search_artist_id(band_name: str):
    """Sucht einen Künstler bei Deezer und gibt die ID des besten
    Treffers zurück (None, falls nichts gefunden wurde)."""
    resp = requests.get(f"{API_BASE}/search/artist", params={"q": band_name}, timeout=15)
    data = _check(resp.json())
    results = data.get("data", [])
    if not results:
        return None
    return results[0]["id"]


def get_top_tracks(artist_id: int, limit: int = 3):
    """Holt die laut Deezer beliebtesten Tracks eines Künstlers."""
    resp = requests.get(
        f"{API_BASE}/artist/{artist_id}/top",
        params={"limit": limit},
        timeout=15,
    )
    data = _check(resp.json())
    return data.get("data", [])


def top_tracks_for_band(band_name: str, limit: int = 3):
    """Kombiniert Suche + Top-Tracks. Gibt [] zurück, wenn kein
    passender Künstler gefunden wurde."""
    artist_id = search_artist_id(band_name)
    if artist_id is None:
        return []
    time.sleep(0.2)  # kleine Pause, um das Rate-Limit zu schonen
    return get_top_tracks(artist_id, limit=limit)


class DeezerPlaylist:
    """Playlist-Operationen, die einen Access-Token benötigen."""

    def __init__(self, access_token: str):
        self.token = access_token

    def _post(self, path, **params):
        params["access_token"] = self.token
        resp = requests.post(f"{API_BASE}{path}", params=params, timeout=15)
        return _check(resp.json())

    def _get(self, path, **params):
        params["access_token"] = self.token
        resp = requests.get(f"{API_BASE}{path}", params=params, timeout=15)
        return _check(resp.json())

    def _delete(self, path, **params):
        params["access_token"] = self.token
        resp = requests.delete(f"{API_BASE}{path}", params=params, timeout=15)
        return _check(resp.json())

    def create_playlist(self, title: str) -> int:
        result = self._post("/user/me/playlists", title=title)
        return int(result["id"])

    def get_track_ids(self, playlist_id: int):
        data = self._get(f"/playlist/{playlist_id}/tracks")
        return [t["id"] for t in data.get("data", [])]

    def add_tracks(self, playlist_id: int, track_ids):
        if not track_ids:
            return
        songs = ",".join(str(t) for t in track_ids)
        self._post(f"/playlist/{playlist_id}/tracks", songs=songs)

    def remove_tracks(self, playlist_id: int, track_ids):
        if not track_ids:
            return
        songs = ",".join(str(t) for t in track_ids)
        self._delete(f"/playlist/{playlist_id}/tracks", songs=songs)
