"""
Scraper für die Summer Breeze Bandseite: liest die Bandliste UND das
aktuelle Festivaljahr (für die Playlist-Benennung, z.B. SBOD2027)
aus derselben Seite.
"""
import re
import requests
from bs4 import BeautifulSoup

BANDS_URL = "https://www.summer-breeze.de/de/bands/?bands_sort_order=alph"

# Band-Detailseiten haben immer die Form /de/bands/<slug>-<zahl>/
BAND_LINK_RE = re.compile(r"^/de/bands/[a-z0-9\-]+-\d+/?$", re.IGNORECASE)
# z.B. "18.08.2027 - 21.08.2027" -> Jahr 2027
DATE_RANGE_RE = re.compile(r"\d{2}\.\d{2}\.(\d{4})\s*-\s*\d{2}\.\d{2}\.\d{4}")


def fetch_page(url: str = BANDS_URL, timeout: int = 20) -> BeautifulSoup:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SummerBreezeSync/1.0)"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def extract_band_names(soup: BeautifulSoup):
    bands = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        path = href
        if href.startswith("https://www.summer-breeze.de"):
            path = href[len("https://www.summer-breeze.de"):]
        if BAND_LINK_RE.match(path):
            name = a.get_text(strip=True)
            if name:
                # Duplikate (gleiche Band mehrfach verlinkt) zusammenfassen
                bands[name.upper()] = name
    return sorted(bands.values())


def extract_festival_year(soup: BeautifulSoup) -> str:
    """Liest das Festivaljahr aus dem Datumsbereich am Seitenkopf,
    z.B. aus '18.08.2027 - 21.08.2027' -> '2027'."""
    match = DATE_RANGE_RE.search(soup.get_text(" "))
    if not match:
        raise ValueError("Festivaljahr konnte nicht aus der Seite ermittelt werden.")
    return match.group(1)


def fetch_bands_and_year(url: str = BANDS_URL):
    soup = fetch_page(url)
    return extract_band_names(soup), extract_festival_year(soup)


if __name__ == "__main__":
    names, year = fetch_bands_and_year()
    print(f"Festivaljahr: {year}")
    print(f"{len(names)} Bands gefunden:")
    for n in names:
        print(" -", n)
