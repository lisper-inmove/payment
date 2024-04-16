export APP_PRIVATE_KEY_FILE=/home/inmove/payment-files/app-private-key.txt
export ALIPAY_PUBLIC_KEY_FILE=/home/inmove/payment-files/alipay-public-key.RSA2.txt
export ALIPAY_APPID=2021001102655667


dev:
	make api && make entity && export PYTHONPATH=`pwd`/src && source bin/util.sh && APPROOT=`pwd`/src uvicorn --host 0.0.0.0 src.app:app --reload

api:
	cd src/proto && make api-python
	cd src/proto && make api-typescript
entity:
	cd src/proto && make entity

build:
	sudo docker build . -t mh.com:8890/test/demo:v1.0
	sudo docker push mh.com:8890/test/demo:v1.0
restart:
	kubectl delete -f k8s/deployment.yaml
	kubectl apply -f k8s/deployment.yaml

create:
	/bin/bash bin/create.sh
clear:
	echo "输入要删除的entity: "; \
	read entity; \
	echo "Just For Test"; \
	rm src/manager/$${entity}_manager.py; \
	rm src/proto/api/api_$${entity}.proto; \
	rm src/dao/$${entity}_dao.py; \
	rm src/routers/$${entity}_router.py; \
	rm src/proto/entities/$${entity}.proto
