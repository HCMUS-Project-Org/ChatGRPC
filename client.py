import grpc

import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    user_name = input("Enter your name: ")

    while True:
        text = input("Enter your message: ")
        message = chat_pb2.Message(user_name=user_name, text=text)
        response = stub.SendMessage(message)
        print(f"{response.user_name}: {response.text}")

        messages = stub.ReceiveMessage(chat_pb2.Empty())
        for message in messages:
            print(f"{message.user_name}: {message.text}")


if __name__ == '__main__':
    run()
