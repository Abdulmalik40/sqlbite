from varint import read_varint


def get_num_tables(database_file):
    database_file.seek(103)
    return int.from_bytes(database_file.read(2), byteorder="big")


def get_cell_pointers(database_file, num_tables):
    cell_pointers = []
    database_file.seek(108)
    for i in range(num_tables):
        pointer = int.from_bytes(database_file.read(2), byteorder="big")
        cell_pointers.append(pointer)
    return cell_pointers


def get_table_name(database_file, cell_pointers):
    table_names = []
    for pointer in cell_pointers:
        database_file.seek(pointer)
        read_varint(database_file)  # record size
        read_varint(database_file)  # rowid
        read_varint(database_file)  # header size
        serial_type1 = read_varint(database_file)  # type col
        serial_type2 = read_varint(database_file)  # name col
        serial_type3 = read_varint(database_file)  # tbl_name col
        read_varint(database_file)  # rootpage col
        read_varint(database_file)  # sql col
        size_1 = (serial_type1 - 13) // 2
        size_2 = (serial_type2 - 13) // 2
        size_3 = (serial_type3 - 13) // 2
        database_file.read(size_1)
        database_file.read(size_2)
        table_name = database_file.read(size_3).decode("utf-8")
        if not table_name.startswith("sqlite_"):
            table_names.append(table_name)
    return table_names


def get_schema_info(database_file, cell_pointers, target_table):
    for pointer in cell_pointers:
        database_file.seek(pointer)
        read_varint(database_file)  # record size
        read_varint(database_file)  # rowid
        read_varint(database_file)  # header size
        serial_type1 = read_varint(database_file)  # type col
        serial_type2 = read_varint(database_file)  # name col
        serial_type3 = read_varint(database_file)  # tbl_name col
        serial_type4 = read_varint(database_file)  # rootpage col
        serial_type5 = read_varint(database_file)  # sql col
        size_1 = (serial_type1 - 13) // 2
        size_2 = (serial_type2 - 13) // 2
        size_3 = (serial_type3 - 13) // 2
        size_5 = (serial_type5 - 13) // 2
        database_file.read(size_1)
        name = database_file.read(size_2).decode("utf-8")
        database_file.read(size_3)
        rootpage = int.from_bytes(database_file.read(serial_type4), byteorder="big")
        sql = database_file.read(size_5).decode("utf-8")
        if name == target_table:
            return rootpage, sql
    return None, None
