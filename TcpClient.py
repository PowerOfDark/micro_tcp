from dispatchers.Event import Event
from protocols.NetProtocol import NetProtocol
import socket
import _thread


class TcpClient:
    def __init__(self, protocol: NetProtocol):
        self._protocol = protocol
        self._socket = socket.socket()
        self._on_disconnected = Event()
        self._on_payload = Event()
        self._run = False
        self._lock = _thread.allocate_lock()

    @property
    def local_endpoint(self) -> tuple:
        return self._socket.getsockname()

    @property
    def remote_endpoint(self) -> tuple:
        return self._socket.getpeername()

    @property
    def on_disconnected(self) -> Event:
        return self._on_disconnected

    @property
    def on_payload(self) -> Event:
        return self._on_payload

    @property
    def is_connected(self) -> bool:
        return self._socket is not None and self._run

    def _read_worker(self, socket: socket.socket):
        if self._socket != socket:
            return
        while self.is_connected and socket == self._socket:
            try:
                received = self._protocol.read(socket)
                self._on_payload.invoke(self, received)
            except Exception as error:
                self._close(error)

    def connect(self, hostname: str, port: int):
        temp_socket = socket.socket(socket.AF_INET)
        addr = socket.getaddrinfo(hostname, port, socket.AF_INET)[0][4]
        temp_socket.connect(addr)
        self.connect_socket(temp_socket)

    def connect_socket(self, socket: socket.socket):
        if self.is_connected:
            self.close()

        with self._lock:
            self._socket = socket
            self._run = True
            _thread.start_new_thread(self._read_worker, (self._socket,))

    def _close(self, error: Exception):
        with self._lock:
            if self._run:
                self._run = False
                self._on_disconnected.invoke(self, error)
                self._socket.close()
                self._socket = None

    def close(self):
        self._close(ConnectionAbortedError())

    def send(self, payload):
        self._protocol.write(self._socket, payload)
