FROM python:3.8-slim

WORKDIR /opt/badges
COPY requirements.txt /opt/badges/

RUN python -m pip install -r requirements-prod.txt requirements.txt

COPY . .

CMD ["./run_server.sh"]
