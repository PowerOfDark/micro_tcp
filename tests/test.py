from TcpClient import TcpClient
from TcpServer import TcpServer
from protocols.StringProtocol import StringProtocol
from serializers.JsonSerializer import JsonSerializer

proto = StringProtocol(JsonSerializer())


def payload_received(client: TcpClient, payload: str):
    print(f"[{client.local_endpoint}->{client.remote_endpoint}]'{payload}'")
    client.send(("some", "response"))


def client_connected(server: TcpServer, client: TcpClient):
    print(f"client {client.remote_endpoint} connected")
    client.on_payload.subscribe(payload_received)


def client_disconnected(server: TcpServer, client: TcpClient, error: Exception):
    print(f"client {client.remote_endpoint} disconnected: {error}")


tcp_server = TcpServer('0.0.0.0', 33333, proto)
tcp_server.on_client_connected.subscribe(client_connected)
tcp_server.on_client_disconnected.subscribe(client_disconnected)

tcp_server.start()

input("Running")