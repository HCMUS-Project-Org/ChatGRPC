import datetime
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

    def Log(self, content):
        with open("logfile.log", "a") as f:
            f.write(content + '\n')
            print(content)

    def GenerateUserId(self):
        new_id = str(self.max_user_id + 1)

        # Add a leading zero to the user ID if it is less than 10
        if len(new_id) < 2:
            new_id = '0' + new_id

        self.max_user_id += 1

        return new_id

    def CreateNewUser(self, request, context):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")

        new_id = self.GenerateUserId()
        request.id = new_id
        new_user = {"user_id": new_id, 'like_count': 0,
                    'like_from': [], 'is_allow': True}

        # Add the user to the list of allowed users
        self.allow_users.append(new_user)

        log = "["+formatted_time+"] " + request.name + \
            " join group chat" + " - ID(" + new_id + ")"
        self.Log(log)

        return request

    def IsLikeMessage(self, msg):
        msg_components = msg.split('_')

        if len(msg_components) == 2 and msg_components[0] == 'LIKE' and msg_components[1].isdigit():
            return True

        return False

    def HandleLikeMessage(self, time,  msg, from_user):
        msg_components = msg.split('_')
        user_id = msg_components[1]

        log = "[" + time + "] User[" + from_user + \
            "] like for User[" + user_id + "]"
        self.Log(log)

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

        error_msg = "[INFO] You LIKED: ["+user_id + "]'s message"
        from_user = "_" + from_user
        raise grpc.RpcError(error_msg + from_user)

    def SendMessage(self, request, context):
        if self.IsLikeMessage(request.msg):
            # if LIKE msg, still allow this user send msg
            self.HandleLikeMessage(request.time, request.msg, request.user.id)
        else:
            log = ''
            # if user is allowed to send message
            if self.allow_users[int(request.user.id)]['is_allow']:
                # print("[CHECK] Is ALLOW send msg: True")
                # print("[", request.time, "] [", request.user.id, "] ", request.user.name,
                #       " send message '", request.msg, "'", sep="")
                log = "[" + request.time + "] User[" + \
                    request.user.id + "] send message '" + request.msg + "'"
                self.Log(log)

                # add message
                self.messages.append(request)

                # reset user state
                self.allow_users[int(request.user.id)]['like_count'] = 0
                self.allow_users[int(request.user.id)]['is_allow'] = False
            else:
                # print("[CHECK] Is ALLOW send msg: False")
                # print("[", request.time, "] [", request.user.id, "] ", request.user.name,
                #       " is not allow to send message", sep="")
                log = "[" + request.time + "] User[" + request.user.id + \
                    "] is not allow to send message"
                self.Log(log)

                error_msg = "[WARNING] You are NOT allowed to send message"
                from_user = "_" + request.user.id
                raise grpc.RpcError(error_msg+from_user)

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
