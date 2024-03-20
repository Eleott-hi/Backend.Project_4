
grpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. auth.proto

server: install
	python3 main.py

install:
	pip install -r requirements.txt

test:
	pytest
