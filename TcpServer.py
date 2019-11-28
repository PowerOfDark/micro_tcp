import _thread
import socket

from TcpClient import TcpClient
from dispatchers.Event import Event
from protocols.NetProtocol import NetProtocol


class TcpServer:
    def __init__(self, hostname: str, port: int, protocol: NetProtocol):
        self._socket = socket.socket()
        self._hostname = hostname
        self._port = port
        self._protocol = protocol
        self._clients = set()
        self._on_client_connected = Event()
        self._on_client_disconnected = Event()
        self._is_listening = False

    @property
    def clients(self) -> set:
        return self._clients

    @property
    def on_client_connected(self) -> Event:
        return self._on_client_connected

    @property
    def on_client_disconnected(self) -> Event:
        return self._on_client_disconnected

    @property
    def endpoint(self) -> tuple:
        return self._hostname, self._port

    @property
    def socket(self) -> socket.socket:
        return self._socket

    def _listen(self):
        self._is_listening = True
        self._socket.bind(self.endpoint)
        self._socket.listen(10)
        while self._is_listening:
            try:
                (socket, addr) = self._socket.accept()
                client = TcpClient(self._protocol)
                client.connect_socket(socket)
                self._clients.add(client)
                client.on_disconnected.subscribe(self._handle_disconnected)
                self._on_client_connected.invoke(self, client)
            except:
                pass

    def start(self):
        if self._is_listening:
            return
        self._is_listening = True
        _thread.start_new_thread(self._listen, ())

    def stop(self):
        self._is_listening = False

    def _handle_disconnected(self, client: TcpClient, error: Exception):
        self._clients.remove(client)
        self._on_client_disconnected.invoke(self, client, error)