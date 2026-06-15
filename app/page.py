from varint import read_varint


def read_page_cells(database_file, page_offset, page_size):
    database_file.seek(page_offset + 3)
    num_cells = int.from_bytes(database_file.read(2), byteorder="big")
    database_file.seek(page_offset + 8)
    cell_pointers = []
    for _ in range(num_cells):
        pointer = int.from_bytes(database_file.read(2), byteorder="big")
        cell_pointers.append(page_offset + pointer)
    return cell_pointers


def read_record_values(database_file, cell_pointer):
    database_file.seek(cell_pointer)
    read_varint(database_file)  # record size
    read_varint(database_file)  # rowid
    header_start = database_file.tell()
    header_size = read_varint(database_file)
    serial_types = []
    while database_file.tell() < header_start + header_size:
        serial_types.append(read_varint(database_file))
    values = []
    for st in serial_types:
        if st == 0:
            values.append(None)
        elif st == 1:
            values.append(int.from_bytes(database_file.read(1), byteorder="big"))
        elif st == 2:
            values.append(int.from_bytes(database_file.read(2), byteorder="big"))
        elif st == 3:
            values.append(int.from_bytes(database_file.read(3), byteorder="big"))
        elif st == 4:
            values.append(int.from_bytes(database_file.read(4), byteorder="big"))
        elif st == 5:
            values.append(int.from_bytes(database_file.read(6), byteorder="big"))
        elif st == 6:
            values.append(int.from_bytes(database_file.read(8), byteorder="big"))
        elif st >= 13 and st % 2 == 1:
            size = (st - 13) // 2
            values.append(database_file.read(size).decode("utf-8"))
        elif st >= 12 and st % 2 == 0:
            size = (st - 12) // 2
            values.append(database_file.read(size))
        else:
            values.append(None)
    return values
