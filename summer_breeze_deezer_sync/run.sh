#!/usr/bin/with-contenv bashio

export DEEZER_ACCESS_TOKEN=$(bashio::config 'deezer_access_token')
export PLAYLIST_PREFIX=$(bashio::config 'playlist_prefix')
export BANDS_URL=$(bashio::config 'bands_url')
export STATE_DIR=/data/state
SYNC_HOUR=$(bashio::config 'sync_hour')

mkdir -p "$STATE_DIR"

bashio::log.info "Summer Breeze Deezer Sync gestartet. Täglicher Lauf um ${SYNC_HOUR}:00 Uhr (Systemzeit)."

while true; do
    bashio::log.info "Starte Sync-Lauf ..."
    if ! python3 /app/sync.py; then
        bashio::log.error "Sync-Lauf fehlgeschlagen."
    fi

    SLEEP_SECONDS=$(python3 /app/sleep_until.py "$SYNC_HOUR")
    bashio::log.info "Nächster Lauf in $((SLEEP_SECONDS / 3600)) Stunden."
    sleep "$SLEEP_SECONDS"
done
