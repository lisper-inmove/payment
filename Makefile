dev:
	make api && make entity && export PYTHONPATH=`pwd`/src && source bin/util.sh && APPROOT=`pwd`/src uvicorn src.app:app --reload

api:
	cd src/proto && make api-python
entity:
	cd src/proto && make entity

build:
	sudo docker build . -t mh.com:8890/test/task-distribute:v1.0
	sudo docker push mh.com:8890/test/task-distribute:v1.0
restart:
	kubectl delete -f k8s/deployment.yaml
	kubectl apply -f k8s/deployment.yaml

create:
	/bin/bash bin/create.sh
