from TcpClient import TcpClient
from TcpServer import TcpServer
from protocols.StringProtocol import StringProtocol
from serializers.JsonSerializer import JsonSerializer

proto = StringProtocol(JsonSerializer())


def payload_received(client: TcpClient, payload: str):
    print(f"[{client.local_endpoint}->{client.remote_endpoint}] {payload}")


def client_disconnected(client: TcpClient, error: Exception):
    print(f"client {client.remote_endpoint} disconnected: {error}")


tcp_client = TcpClient(proto)

tcp_client.on_disconnected.subscribe(client_disconnected)
tcp_client.on_payload.subscribe(payload_received)
tcp_client.connect("localhost", 33333)

tcp_client.send({"some": "object", "more": ("d", "a", "t", "a")})

input("Running")