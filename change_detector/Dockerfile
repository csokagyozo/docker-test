FROM python:3.11-alpine
COPY detect_change.py /detect_change.py
COPY state.json /vol/state.json
COPY log.json /vol/log.json
RUN chmod +x /detect_change.py
ENTRYPOINT python3 /detect_change.py
