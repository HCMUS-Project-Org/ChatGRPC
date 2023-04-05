1. **Define your gRPC service** using protocol buffers. This will define the messages and methods used for communication.

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
