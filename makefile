SHELL=/bin/bash

NAME=jimon

.PHONY: gen
gen: ./$(NAME)_pb2.py

./$(NAME)_pb2.py: $(NAME).proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<

.PHONY: server
server:
	python ./server.py

.PHONY: client
client:
	python ./client.py

.PHONY: env
env:
	pip install loguru psutil grpcio grpcio-tools peewee fire