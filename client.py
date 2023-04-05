import grpc
import os
import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    user_name = input("Enter your name: ")

    while True:
        text = input("Enter your message: ")

        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"Enter your name: {user_name}")
        print("-------------- CHAT BOX - gRPC --------------")
        message = chat_pb2.Message(user_name=user_name, text=text)
        response = stub.SendMessage(message)

        messages = stub.ReceiveMessage(chat_pb2.Empty())
        for message in messages:
            print(f"{message.user_name}: {message.text}")

        print('---------------------------------------------')


if __name__ == '__main__':
    run()
