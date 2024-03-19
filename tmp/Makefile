
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt


build:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto


server:
	python3 server.py

client:
	python3 client.py

fastapi:
	python3 main.py