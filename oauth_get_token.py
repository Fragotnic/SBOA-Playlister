"""
Lokal auf deinem PC ausführen (NICHT Teil des Add-ons), um einmalig
einen Deezer User-Access-Token mit Schreibrecht auf die Bibliothek
(manage_library) zu erhalten. Den Token danach in die
Add-on-Konfiguration unter 'deezer_access_token' eintragen.

Voraussetzung: Eine registrierte App unter
https://developers.deezer.com/myapps mit einer Redirect-URI,
z.B. http://localhost:8888/callback

Ablauf:
1. App-ID, App-Secret und Redirect-URI als Umgebungsvariablen setzen
   (DEEZER_APP_ID / DEEZER_APP_SECRET / DEEZER_REDIRECT_URI) oder
   unten eintragen.
2. Skript starten -> Browser öffnet sich -> bei Deezer einloggen und
   die App autorisieren.
3. Der Access-Token wird in der Konsole ausgegeben.
"""
import http.server
import os
import urllib.parse
import webbrowser

import requests

APP_ID = os.environ.get("DEEZER_APP_ID", "DEINE_APP_ID")
APP_SECRET = os.environ.get("DEEZER_APP_SECRET", "DEIN_APP_SECRET")
REDIRECT_URI = os.environ.get("DEEZER_REDIRECT_URI", "http://localhost:8888/callback")
PERMS = "basic_access,manage_library"

_auth_code = {}


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get("code", [None])[0]
        _auth_code["code"] = code
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        msg = (
            "Autorisierung erhalten, du kannst dieses Fenster schließen."
            if code
            else "Fehler: kein Code erhalten."
        )
        self.wfile.write(msg.encode("utf-8"))

    def log_message(self, format, *args):
        pass  # Konsole sauber halten


def main():
    auth_url = "https://connect.deezer.com/oauth/auth.php?" + urllib.parse.urlencode(
        {"app_id": APP_ID, "redirect_uri": REDIRECT_URI, "perms": PERMS}
    )
    print("Öffne Browser zur Autorisierung ...")
    print(auth_url)
    webbrowser.open(auth_url)

    host, port = urllib.parse.urlparse(REDIRECT_URI).netloc.split(":")
    server = http.server.HTTPServer((host, int(port)), CallbackHandler)
    server.handle_request()  # wartet auf genau einen Request (den Callback)

    code = _auth_code.get("code")
    if not code:
        raise SystemExit("Kein Autorisierungs-Code erhalten. Abbruch.")

    token_resp = requests.get(
        "https://connect.deezer.com/oauth/access_token.php",
        params={"app_id": APP_ID, "secret": APP_SECRET, "code": code, "output": "json"},
        timeout=15,
    )
    data = token_resp.json()
    access_token = data.get("access_token")
    if not access_token:
        raise SystemExit(f"Kein Token erhalten: {data}")

    print("\nAccess-Token erhalten:")
    print(access_token)
    print("\nBitte in der Add-on-Konfiguration unter 'deezer_access_token' eintragen.")


if __name__ == "__main__":
    main()
