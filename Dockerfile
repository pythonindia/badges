FROM python:3.8-slim

WORKDIR /opt/badges
COPY requirements.txt requirements-prod.txt /opt/badges/

RUN python -m pip install -r requirements-prod.txt -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["./run_server.sh"]
