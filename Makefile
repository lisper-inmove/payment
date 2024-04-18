dev:
	make api && make entity && export PYTHONPATH=`pwd`/src && source bin/util.sh && APPROOT=`pwd`/src uvicorn --host 0.0.0.0 src.app:app --port 9091 --reload

api:
	cd src/proto && make api-python
	cd src/proto && make api-typescript
entity:
	cd src/proto && make entity

bd:
	sudo docker build . -t mh.com:8890/test/payment:v1.0
	sudo docker push mh.com:8890/test/payment:v1.0

rd:
	sudo docker stop payment_v1
	sudo docker rm payment_v1
	sudo docker run --restart always --network=host -d --name payment_v1 -p 10001:8000 mh.com:8890/test/payment:v1.0

sd:
	sudo docker run --restart always --network=host -d --name payment_v1 -p 10001:8000 mh.com:8890/test/payment:v1.0

restart:
	kubectl delete -f k8s/deployment.yaml
	kubectl apply -f k8s/deployment.yaml
