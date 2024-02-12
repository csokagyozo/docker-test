FROM python:3.11-alpine
COPY detect_change.py /detect_change.py
CMD curl https://raw.githubusercontent.com/csokagyozo/docker-test/no-volumes/change_detector/state.json --output /vol/state.json
CMD curl https://raw.githubusercontent.com/csokagyozo/docker-test/no-volumes/change_detector/log.json --output /vol/log.json
RUN chmod +x /detect_change.py
ENTRYPOINT python3 /detect_change.py
