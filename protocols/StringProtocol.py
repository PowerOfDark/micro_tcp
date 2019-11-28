from helpers.BinaryEncoder import BinaryEncoder
from helpers.SocketHelper import SocketHelper
from protocols.NetProtocol import NetProtocol


class StringProtocol(NetProtocol):

    PAYLOAD_FLAG = b'\x01'

    def __init__(self, serializer):
        super().__init__(serializer)
        pass

    def write_raw(self, socket, buffer, count=-1):
        SocketHelper.write_bytes(socket, buffer, count)

    def write_payload(self, socket, payload):
        self.write_raw(socket, StringProtocol.PAYLOAD_FLAG)

        payload_serialized = self._serializer.serialize(payload)
        payload_bytes = bytes(payload_serialized, 'utf8')
        content_length = len(payload_bytes)
        header_bytes = BinaryEncoder.encode_varint(content_length)

        SocketHelper.write_bytes(socket, header_bytes)
        SocketHelper.write_bytes(socket, payload_bytes)

    def write(self, socket, payload):
        self.write_payload(socket, payload)

    def read_payload(self, socket):
        content_length = SocketHelper.read_varint(socket)
        payload_bytes = SocketHelper.read_bytes(socket, content_length)
        payload_str = str(payload_bytes, 'utf8')
        return self._serializer.deserialize(payload_str)

    def read(self, socket):
        flag = SocketHelper.read_bytes(socket, 1)
        if flag != StringProtocol.PAYLOAD_FLAG:
            raise RuntimeError(f"unknown packet flag: {flag}")
        return self.read_payload(socket)
