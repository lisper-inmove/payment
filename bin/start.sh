source bin/util.sh

uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 2
