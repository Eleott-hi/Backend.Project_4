import grpc
import calculator_pb2
import calculator_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    response: calculator_pb2.AddResponse = stub.Add(
        calculator_pb2.AddRequest(num1=10, num2=5)
    )
    print("Result of adding 10 and 5:", response.result)


if __name__ == "__main__":
    run()
