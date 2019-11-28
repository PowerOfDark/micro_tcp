from serializers.Serializer import Serializer
import socket


class NetProtocol:
    """Abstract base class for implementing custom typed protocols"""
    def __init__(self, serializer: Serializer):
        self._serializer = serializer
        pass

    @property
    def serializer(self):
        return self._serializer

    def write(self, socket: socket.socket, payload):
        """
        Writes the custom-typed payload to the socket
        :param socket: Target socket
        :param payload: Custom-typed payload
        :return: None
        """
        pass

    def read(self, socket: socket.socket):
        """
        Reads a custom-typed payload from the socket
        :param socket: Target socket
        :return: Custom-typed payload
        """
        pass
