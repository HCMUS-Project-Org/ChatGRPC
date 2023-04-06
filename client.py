import grpc
import os
import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc
import datetime


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # Do not specify the user ID, it will be assigned by the server
        user_name = input("Enter your name: ")
        user = chat_pb2.User(name=user_name)

        while True:
            msg = input("Enter your message: ")

            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"Enter your name: {user_name}")
            print("-------------- CHAT BOX - gRPC --------------")

            # get current time
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")

            # send msg to server
            message = chat_pb2.Message(user=user, msg=msg, time=formatted_time)
            response = stub.SendMessage(message)

            # update user id if it is not set
            if not user.id:
                user.id = response.user.id
            print("[Client - Response(SendMsg)]: ", response)

            # receive all msg from server
            messages = stub.ReceiveMessage(chat_pb2.Empty())
            for message in messages:
                print(
                    f"[{message.time}][{message.user.id}] {message.user.name}: {message.msg}")

            print('---------------------------------------------')


if __name__ == '__main__':
    run()
