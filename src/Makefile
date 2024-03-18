SERVER_DIR := fastapi
DB_DIR := postgres
DB_CONTAINER_NAME := db

all: clean_db
	docker-compose up

clean_db:
	-docker stop $(DB_CONTAINER_NAME)
	-docker rm $(DB_CONTAINER_NAME)

.PHONY: nginx
nginx:
	docker-compose restart nginx

.PHONY: fastapi
fastapi:
	docker-compose restart fastapi_1
	docker-compose restart fastapi_2
	docker-compose restart fastapi_3


key:
	openssl req -x509 -newkey rsa:4096 -keyout backend3.local.key -out backend3.local.crt -days 365 -nodes -subj "/CN=backend3.local"
