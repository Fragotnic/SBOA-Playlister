"""
Gibt die Anzahl Sekunden bis zur nächsten Ziel-Uhrzeit (lokale
Systemzeit) auf stdout aus. Wird von run.sh genutzt, um den
Sync-Lauf einmal täglich zur konfigurierten Uhrzeit auszuführen,
unabhängig von der Startzeit des Containers.
"""
import sys
from datetime import datetime, timedelta


def seconds_until(hour: int) -> int:
    now = datetime.now()
    target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


if __name__ == "__main__":
    hour = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print(seconds_until(hour))
