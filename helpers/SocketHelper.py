import socket


class SocketHelper:
    @staticmethod
    def read_bytes(socket: socket.socket, count: int) -> bytes:
        buffer = b''
        while count > 0:
            received = socket.recv(count)
            if not received or len(received) == 0:
                raise BrokenPipeError("socket disconnected")
            buffer += received
            count -= len(received)
        return buffer


    @staticmethod
    def write_bytes(socket: socket.socket, buffer, count: int = -1):
        if count == -1:
            count = len(buffer)

        total_written = 0
        while total_written < count:
            written = socket.send(buffer[total_written:])
            if written == 0:
                raise BrokenPipeError("socket disconnected")
            total_written += written

    @staticmethod
    def read_varint(socket: socket.socket) -> int:
        value = 0
        while True:
            value <<= 7
            current_byte = SocketHelper.read_bytes(socket, 1)[0]
            value |= current_byte & 0x7f
            if not (current_byte & 0x80):  # if no continuation
                break
        return value
