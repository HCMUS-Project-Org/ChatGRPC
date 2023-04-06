import grpc
import time
from concurrent import futures

import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []
        self.max_user_id = 0

    def SendMessage(self, request, context):
        print('--------- Server - Send Request ---------------------')
        print("--- [original]: \n", request)
        # Increment the user ID if it is not set or if it is lower than the current max ID
        if not request.user.id:
            request.user.id = str(self.max_user_id + 1)
            self.max_user_id += 1

        # Add a leading zero to the user ID if it is less than 10
        if len(request.user.id) < 2:
            request.user.id = '0' + request.user.id

        print("--- [original]: \n", request)

        self.messages.append(request)
        return request

    def ReceiveMessage(self, request, context):
        # while True:
        for message in self.messages:
            yield message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")

    server.wait_for_termination()

    # try:
    #     while True:
    #         time.sleep(86400)
    # except KeyboardInterrupt:
    #     server.stop(0)


if __name__ == '__main__':
    serve()
