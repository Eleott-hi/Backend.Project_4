all: install grpc run

grpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/auth.proto

install:
	pip install -r requirements.txt

run:
	python3 main.py