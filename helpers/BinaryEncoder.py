class BinaryEncoder:
    @staticmethod
    def encode_varint(value):
        packed = 0
        while True:
            packed <<= 8
            packed |= value & 0x7f
            value >>= 7  # move 7 bits
            if value:
                packed |= 0x80  # continuation bit
            else:
                break

        return packed.to_bytes((packed.bit_length() + 7) // 8, byteorder="big")

    @staticmethod
    def decode_varint(hex_str):
        value = 0
        for byte in hex_str:
            value |= byte & 0x7f
            value <<= 7
        return value

