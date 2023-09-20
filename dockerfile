FROM mh.com:8890/test/fastapi-base:v1.0

WORKDIR /app

ENV API_VERESION=v1.0 \
    APPROOT=/app/src \
    PYTHONPATH=/app:/app/src

COPY . .

CMD ["/bin/bash", "bin/start.sh"]
