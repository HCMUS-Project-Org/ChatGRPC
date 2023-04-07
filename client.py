import grpc
import os
import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc
import datetime


def IsLikeMessage(msg):
    msg_components = msg.split('_')
    if len(msg_components) == 2 and msg_components[0] == 'LIKE' and msg_components[1].isdigit():
        return True
    return False


def ClearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def ShowMessage(stub):
    # receive all msg from server
    messages = stub.ReceiveMessage(chat_pb2.Empty())
    for message in messages:
        if not IsLikeMessage(message.msg):
            print(
                f"[{message.time}][{message.user.id}] {message.user.name}: {message.msg}")


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        # Do not specify the user ID, it will be assigned by the server
        user_name = input("Enter your name: ")
        user = chat_pb2.User(name=user_name)

        while True:
            try:
                msg = input("Enter your message: ")

                ClearScreen()
                print(f"Enter your name: {user_name}")
                print("-------------- CHAT BOX - gRPC --------------")

                # get current time
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")

                # send msg to server
                message = chat_pb2.Message(
                    user=user, msg=msg, time=formatted_time)
                response = stub.SendMessage(message)

                # update user id if it is not set
                if not user.id:
                    user.id = response.user.id
                # print("[Client - Response(SendMsg)]: ", response)

                ShowMessage(stub)
            except grpc.RpcError as e:
                error_details = e.details().strip("Exception calling application: ")

                error = error_details.split("_")[0]
                id = error_details.split("_")[1]
                # update user id if it is not set
                if not user.id:
                    user.id = id

                ShowMessage(stub)
                print('---------------------------------------------')
                print(error)
                continue

            print('---------------------------------------------')
            # TODO: continues update msg


if __name__ == '__main__':
    run()
