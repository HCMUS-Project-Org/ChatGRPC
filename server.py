import grpc
import time
from concurrent import futures

import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []

    def SendMessage(self, request, context):
        message = chat_pb2.Message(
            user_name=request.user_name, text=request.text)
        self.messages.append(message)
        return message

    def ReceiveMessage(self, request, context):
        for message in self.messages:
            yield message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
