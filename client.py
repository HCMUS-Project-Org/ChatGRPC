import grpc
import my_service_pb2
import my_service_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = my_service_pb2_grpc.MyServiceStub(channel)
        request = my_service_pb2.MyRequest()
        # set request parameters
        response = stub.my_method(request)
        # handle response


if __name__ == '__main__':
    run()
