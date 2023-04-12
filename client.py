import threading
import time
import grpc
import os
import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc
import datetime


class ChatClient:
    def __init__(self):
        # Create a gRPC channel
        self.channel = grpc.insecure_channel('localhost:50051')

        # Create a stub for the service
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

        # Do not specify the user ID, it will be assigned by the server
        self.user_name = input("Enter your name: ")
        self.user = chat_pb2.User(name=self.user_name)
        self.number_msg = 0

    def IsLikeMessage(self, msg):
        msg_components = msg.split('_')
        if len(msg_components) == 2 and msg_components[0] == 'LIKE' and msg_components[1].isdigit():
            return True
        return False

    def ClearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def ShowMessage(self):
        # receive all msg from server
        messages = self.stub.ReceiveMessage(chat_pb2.Empty())

        for message in messages:
            if not self.IsLikeMessage(message.msg):
                print(
                    f"[{message.time}][{message.user.id}] {message.user.name}: {message.msg}")

    def InputAndSendMsg(self):
        while True:
            try:
                msg = input()

                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")

                # send msg to server
                message = chat_pb2.Message(
                    user=self.user, msg=msg, time=formatted_time)
                response = self.stub.SendMessage(message)

                # update user id if it is not set
                if not self.user.id:
                    self.user.id = response.user.id

            except grpc.RpcError as e:
                error_details = e.details().strip("Exception calling application: ")

                error = error_details.split("_")[0]
                id = error_details.split("_")[1]
                # update user id if it is not set
                if not self.user.id:
                    self.user.id = id

                print('---------------------------------------------')
                print(error)

            print('---------------------------------------------')

    def run(self):
        threading.Thread(target=self.InputAndSendMsg, args=()).start()
        while True:
            messages = self.stub.ReceiveMessage(chat_pb2.Empty())
            len_msg = len(list(messages))

            if int(self.number_msg) != int(len_msg):
                self.number_msg = len_msg

                self.ClearScreen()

                print(f"WELCOME {self.user_name}!")
                print("-------------- CHAT BOX - gRPC --------------")

                self.ShowMessage()
                print("----------------------------------------------")
                print("Enter your message: ")


if __name__ == '__main__':
    client = ChatClient()
    client.run()
