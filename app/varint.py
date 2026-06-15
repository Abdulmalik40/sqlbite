def read_varint(database_file):
    result = 0
    for i in range(9):
        byte = int.from_bytes(database_file.read(1), byteorder="big")
        result = (result << 7) | (byte & 0x7F)
        if (byte & 0x80) == 0:
            return result
    return result
