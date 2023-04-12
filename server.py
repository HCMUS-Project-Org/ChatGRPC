import grpc
import time
from concurrent import futures

import service.chat_pb2 as chat_pb2
import service.chat_pb2_grpc as chat_pb2_grpc


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = set()
        self.messages = []
        self.allow_users = [
            {"user_id": "00", "like_count": 0, "like_from": [], "is_allow": True}]
        self.max_user_id = 0

    def GenerateUserId(self):
        print("[GENERATE] User ID:", end=" ")
        new_id = str(self.max_user_id + 1)

        # Add a leading zero to the user ID if it is less than 10
        if len(new_id) < 2:
            new_id = '0' + new_id

        self.max_user_id += 1
        print(new_id)

        return new_id

    def CreateNewUser(self):
        print("[CREATE] New user:")

        new_id = self.GenerateUserId()
        new_user = {"user_id": new_id, 'like_count': 0,
                    'like_from': [], 'is_allow': True}

        print("  {")
        print("    user_id:", new_user["user_id"])
        print("    like_count:", new_user["like_count"])
        print("    like_from:", new_user["like_from"])
        print("    is_allow:", new_user["is_allow"])
        print("  }")

        # Add the user to the list of allowed users
        self.allow_users.append(new_user)

        return new_id

    def IsLikeMessage(self, msg):
        print("[CHECK] Is LIKE message:", end=" ")

        msg_components = msg.split('_')

        if len(msg_components) == 2 and msg_components[0] == 'LIKE' and msg_components[1].isdigit():
            print("True")
            return True

        print("False")
        return False

    def HandleLikeMessage(self, msg, from_user):
        print("[HANDLE] LIKE message")

        msg_components = msg.split('_')
        user_id = msg_components[1]

        if user_id == from_user:
            error_msg = "[WARNING] You can not LIKE yourself!"
            from_user = "_" + from_user
            raise grpc.RpcError(error_msg + from_user)

        if from_user in self.allow_users[int(user_id)]["like_from"]:
            error_msg = "[WARNING] You only LIKED: [" + \
                user_id + "]'s message ONCE!"
            from_user = "_" + from_user
            raise grpc.RpcError(error_msg + from_user)

        for user in self.allow_users:
            if user_id == user['user_id']:
                self.allow_users[int(user_id)]['like_count'] += 1
                self.allow_users[int(user_id)]['like_from'].append(from_user)
                if self.allow_users[int(user_id)]['like_count'] >= 2:
                    self.allow_users[int(user_id)]['is_allow'] = True

        print("  {")
        print("    user_id: ", self.allow_users[int(user_id)]["user_id"])
        print("    like_count: ", self.allow_users[int(user_id)]["like_count"])
        print("    like_from: ", self.allow_users[int(user_id)]["like_from"])
        print("    is_allow: ", self.allow_users[int(user_id)]["is_allow"])
        print("  }")

        error_msg = "[INFO] You LIKED: ["+user_id + "]'s message"
        from_user = "_" + from_user
        raise grpc.RpcError(error_msg + from_user)

    def SendMessage(self, request, context):
        # TODO: change LOG

        print('--------- Server - Send Request ---------------------')

        # if request of new user (dont have id)
        if not request.user.id:
            print("[CHECK] Is NEW user: True")
            request.user.id = self.CreateNewUser()
        else:
            print("[CHECK] Is NEW user: False")

        if self.IsLikeMessage(request.msg):
            # if LIKE msg, still allow this user send msg
            self.HandleLikeMessage(request.msg, request.user.id)
        else:
            # if user is allowed to send message
            if self.allow_users[int(request.user.id)]['is_allow']:
                print("[CHECK] Is ALLOW send msg: True")
                # add message
                self.messages.append(request)

                # reset user state
                self.allow_users[int(request.user.id)]['like_count'] = 0
                self.allow_users[int(request.user.id)]['is_allow'] = False
            else:
                print("[CHECK] Is ALLOW send msg: False")
                error_msg = "[WARNING] You are NOT allowed to send message"
                from_user = "_" + request.user.id
                raise grpc.RpcError(error_msg+from_user)

        print("[UPDATE] User state ")
        print("  {")
        print("    user_id: ", self.allow_users[int(
            request.user.id)]["user_id"])
        print("    like_count: ", self.allow_users[int(
            request.user.id)]["like_count"])
        print("    is_allow: ", self.allow_users[int(
            request.user.id)]["is_allow"])
        print("  }")

        print("[SEND] Message")
        print("  user {")
        print("    id: ", request.user.id)
        print("    name: ", request.user.name)
        print("  }")
        print("  msg: ", request.msg)
        print("  time: ", request.time)

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


if __name__ == '__main__':
    serve()
