ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY scraper.py deezer_client.py sync.py sleep_until.py /app/

COPY run.sh /
RUN chmod a+x /run.sh

LABEL \
    io.hass.name="Summer Breeze Deezer Sync" \
    io.hass.description="Täglicher Deezer-Playlist-Sync für Summer-Breeze-Bands" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"

CMD [ "/run.sh" ]
