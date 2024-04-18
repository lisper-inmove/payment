source bin/util.sh

uvicorn src.app:app --host 0.0.0.0 --port 9090 --workers 2
