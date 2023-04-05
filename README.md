1. **Define your gRPC service** using protocol buffers. This will define the messages and methods used for communication.

   1. Define your service in a .proto file using protocol buffer syntax. (`chat_service.proto` in `/service`)

      ```go
      syntax = "proto3";

      import "google/protobuf/empty.proto";

      package chat;

      message Message {
        string text = 1;
        string sender = 2;
      }

      service ChatService {
        rpc SendMessage(Message) returns (google.protobuf.Empty);
        rpc ReceiveMessage(google.protobuf.Empty) returns (stream Message);
      }
      ```

      <details>
        <summary>Explain variable</summary>

      This defines a:

      -  **Message** type with `text` and `sender` fields
      -  **ChatService** with two methods:
         -  `SendMessage` for sending a message, taking a Message parameter and returns an empty response
         -  `ReceiveMessage` for receiving messages as a stream, taking no parameters and returns a stream of Message responses

      </details>

   2. Use the generated code to implement your gRPC service.

      ```shell
      python -m grpc_tools.protoc -I /path/to/protos --python_out=. --grpc_python_out=. /path/to/protos/my_service.proto
      ```

      Example:

      ```shell
      python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/my_service.proto
      ```

2. **Implement the server-side code** for your gRPC service. This will handle incoming requests and provide responses. You can create a new process for each instance of your gRPC server.

3. **Implement the client-side code** for your gRPC service. This will send requests to the server and receive responses. You can create one or more client processes as needed.

4. **Start** the `server process(es)` and `client process(es)`.

5. Use gRPC's built-in functionality to handle the communication between the server and client processes.
