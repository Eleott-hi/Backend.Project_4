import grpc
import auth_pb2_grpc
from concurrent import futures
import database.database as database
from AuthGRPC import AuthenticationServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthenticationServicer_to_server(AuthenticationServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started. Listening on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    database.init_db()
    database.test_create()
    serve()
