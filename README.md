<h1 align="center">
  <img src="./assets/grpc-icon.png" alt="icon" width="200"></img>
  <br>
  <b>Chat gRPC</b>
</h1>

<p align="center">Chat application use gRPC to communicate between processes.</p>

<!-- Badges -->
<p align="center">
  <a href="https://github.com/HCMUS-Project/ChatGRPC/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/HCMUS-Project/ChatGRPC" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/HCMUS-Project/ChatGRPC" alt="last update" />
  </a>
  <a href="https://github.com/HCMUS-Project/ChatGRPC/network/members">
    <img src="https://img.shields.io/github/forks/HCMUS-Project/ChatGRPC" alt="forks" />
  </a>
  <a href="https://github.com/HCMUS-Project/ChatGRPC/stargazers">
    <img src="https://img.shields.io/github/stars/HCMUS-Project/ChatGRPC" alt="stars" />
  </a>
  <a href="https://github.com/HCMUS-Project/ChatGRPC/issues/">
    <img src="https://img.shields.io/github/issues/HCMUS-Project/ChatGRPC" alt="open issues" />
  </a>
</p>

<p align="center">
  <b>
      <a href="#demo">Demo</a> •
      <a href="https://github.com/HCMUS-Project/ChatGRPC">Documentation</a> •
      <a href="https://github.com/HCMUS-Project/ChatGRPC/issues/">Report Bug</a> •
      <a href="https://github.com/HCMUS-Project/ChatGRPC/issues/">Request Feature</a>
  </b>
</p>

<br/>

<details open>
<summary><b>📖 Table of Contents</b></summary>

-  [Demo](#film_projector-demo)
-  [Report](#newspaper-report)
-  [Getting Started](#toolbox-getting-started)
   -  [Prerequisites](#pushpin-prerequisites)
   -  [How to use gRPC](#mechanical_arm-how-to-use-grpc)
   -  [Installation](#hammer_and_wrench-installation)
   -  [Chat Convention](#speech_balloon-chat-convention)
      -  [LIKE reply](#like-reply)
      -  [Exception](#exception)
   -  [Log](#page_facing_up-log)
      -  [Log file](#log-file)
      -  [Content](#content)
-  [Roadmap](#world_map-roadmap)
-  [silhouette: Contributors](#busts_in_silhouette-contributors)
-  [Credits](#sparkles-credits)
-  [License](#scroll-license)

# :film_projector: Demo

Check out the [**demo video**](https://youtu.be/j3ZhaS5n7hU) to see the app in action.

# :newspaper: Report

Check out the [**report**](https://docs.google.com/document/d/1XG1qBbMOVZpRwFrU5hV9Z66X6tNGrkkXGsKeIZU_Ns8/edit?usp=sharing) to see full report.

# :toolbox: Getting Started

## :pushpin: Prerequisites

-  **Python:** `>= 3.10.7`
-  **gRPC tools:** gRPC compiler, Install [here](https://grpc.io/docs/languages/python/quickstart/).

## :mechanical_arm: How to use gRPC

**1**. **Define your gRPC service** using protocol buffers. This will define the messages and methods used for communication.

1. Define your service in a .proto file using protocol buffer syntax. (`chat.proto` in `/service`)

   ```go
   syntax = "proto3";

   service ChatService {
     rpc SendMessage(Message) returns (Message) {}
     rpc ReceiveMessage(Empty) returns (stream Message) {}
   }

   message Message {
     string user_name = 1;
     string text = 2;
   }

   message Empty {}
   ```

   <details>
     <summary>Explain variable</summary>

   This defines a:

   -  **Message** type with `text` and `sender` fields
   -  **ChatService** with two methods:
      -  `SendMessage` takes a `Message` object as input and returns a `Message` object
      -  `ReceiveMessage` takes an empty `Empty` object as input and returns a stream of `Message` objects.

   </details>

2. Use the generated code to implement your gRPC service.

   ```shell
   python -m grpc_tools.protoc -I /path/to/protos --python_out=. --grpc_python_out=. /path/to/protos/my_service.proto
   ```

   Example:

   ```shell
   python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/my_service.proto
   ```

3. **Implement the server-side code** for your gRPC service. This will handle incoming requests and provide responses. You can create a new process for each instance of your gRPC server.
     <details>
       <summary>Explain server</summary>

   -  This defines a `ChatServiceServicer` class that implements the `ChatService` defined in `chat.proto`. The `SendMessage` function appends the received message to a list of messages and returns the same message. The `ReceiveMessage` function yields all the messages in the list.
   -  The `serve` function creates a gRPC server and adds the `ChatServiceServicer` to it. It starts the server on port `50051`.

      </details>

4. **Implement the client-side code** for your gRPC service. This will send requests to the server and receive responses. You can create one or more client processes as needed.

5. **Start** the `server process(es)` and `client process(es)`.

6. Use gRPC's built-in functionality to handle the communication between the server and client processes.

## :hammer_and_wrench: Installation

Install application

```bash
# Clone this repository
git clone https://github.com/HCMUS-Project/ChatGRPC.git

# Go into the repository
cd ChatGRPC
```

Run server

```bash
python server.py
```

Run client (open new terminal)

```bash
python client.py
```

> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.

## :speech_balloon: Chat Convention

### LIKE reply

> **LIKE reply**: for allow user XX to continue chat (at least 2 LIKE)

**Syntax**: `LIKE_<user_id>`  
**Rule**:

-  Only LIKE once per user
-  Can not LIKE your self

**Example**: LIKE_01

### Exception

**Syntax**: `[<type>] <content>_<user_id>`  
**Program exception:**

-  [WARNING] You can not LIKE yourself\_`<from_user>`!
-  [WARNING] You only LIKED: [`<user_id>`]'s message ONCE!\_`<from_user>`
-  [WARNING] You are NOT allowed to send message\_`<from_user>`
-  [INFO] You LIKED: [`<user_id>`]'s message\_`<from_user>`

## :page_facing_up: Log

### Log file

Syntax: `[<time>] <content>`

```log
<!-- logfile.log exapmle  -->
[15:47:47] Quan join group chat - ID(01)
[15:47:54] User[01] send message 'hello'
[15:47:54] User[01] is BLOCKED to send message
[15:48:08] User[01] is not allow to send message
[15:48:15] Van join group chat - ID(02)
[15:48:20] Lien join group chat - ID(03)
[15:48:23] Hao join group chat - ID(04)
[15:48:29] Dat join group chat - ID(05)
[15:48:35] User[05] send message 'hello'
[15:48:35] User[05] is BLOCKED to send message
[15:48:42] User[04] send message 'chao moi nguoi'
[15:48:42] User[04] is BLOCKED to send message
[15:48:51] User[03] send message 'alo alo'
[15:48:51] User[03] is BLOCKED to send message
[15:49:03] User[03] like for User[01]
[15:49:15] User[03] like for User[01]
[15:49:28] User[03] like for User[03]
[15:49:36] User[04] like for User[01]
[15:49:36] User[01] is ALLOWED to send message
[15:49:56] User[01] send message 'hi , i am free'
[15:49:56] User[01] is BLOCKED to send message
[15:50:00] User[01] is not allow to send message
```

### Content

-  Client connect and enter username:  
   `<username> join group chat - ID(<user_id>)`
-  Client send msg success:  
   `User[<user_id>] send message ‘<message>`
-  Client A like client B's msg:  
   `User[<userA_id>] like for User[<userB_id>]`
-  Client being block send msg but still try sending msg:  
   `User[<user_id>] is not allow to send message`
-  Client has been blocked from sending messages:  
   `User[<user_id>] is BLOCKED to send message`
-  The client is allowed to send messages:  
   `User[<user_id>] is ALLOWED to send message`

# :world_map: Roadmap

-  [x] Complete the server
-  [x] Complete the client
-  [x] Log file
-  [x] Report

# :busts_in_silhouette: Contributors

<a href="https://github.com/HCMUS-Project/ChatGRPC/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HCMUS-Project/ChatGRPC" />
</a>

Contributions are always welcome!

# :sparkles: Credits

This software uses the following open source packages:

-  [gRPC](https://grpc.io/)
-  Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)

# :scroll: License

Distributed under the MIT License. See <a href="./LICENSE">`LICENSE`</a> for more information.

---

> Bento [@quanblue](https://bento.me/quanblue) &nbsp;&middot;&nbsp;
> GitHub [@QuanBlue](https://github.com/QuanBlue) &nbsp;&middot;&nbsp; Gmail quannguyenthanh558@gmail.com
