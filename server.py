import service.chat_service_pb2_grpc
import service.chat_service_pb2
import grpc
from concurrent import futures


class MyService(my_service_pb2_grpc.CalculatorServiceServicer):
    def my_method(self, request, context):
        # handle incoming request
        response = my_service_pb2.MyResponse()
        # create and return response


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_service_pb2_grpc.add_CalculatorServiceServicer_to_server(
        MyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()
