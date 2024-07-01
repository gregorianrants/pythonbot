import zmq
import json
import time


class Publisher:
    def __init__(self, context, address, node, topic):
        self.context = context
        self.publicationAddress = None
        self.socket = None
        self.address = address
        self.node = node
        self.topic = topic
        self.register()

    def register(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect("tcp://192.168.178.23:3000")
        socket.send_json(
            {
                "action": "register",
                "register_as": "publisher",
                "topic": self.topic,
                "node": self.node,
                "address": self.address,
            }
        )

        message = socket.recv_json()
        print(message)
        self.publicationAddress = message["data"]["full_address"]
        self.socket = self.context.socket(zmq.PUB)
        print(f"subscribing to {self.publicationAddress}")
        self.socket.bind(self.publicationAddress)

    def send_json(self, py_dict):
        as_json = json.dumps(py_dict)
        self.socket.send_string(as_json)

    def send_bytes(self, data):
        message = [bytes(self.node, "UTF-8"), bytes(self.topic, "UTF-8"), data]
        # print(message)
        self.socket.send_multipart(message)


# context = zmq.Context()
# publisher = Publisher(
#     context=context, address="tcp://192.168.178.26", node="camera", topic="frame"
# )

# time.sleep(5)
# print("sending it")
# publisher.send_json({"hello": "there"})
