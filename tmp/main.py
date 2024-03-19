from fastapi import FastAPI
import calculator_pb2
import calculator_pb2_grpc
import grpc

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/add")
def add(num1: int, num2: int):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        response = stub.Add(calculator_pb2.AddRequest(num1=num1, num2=num2))
        return {"result": response.result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
