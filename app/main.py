import sys
from schema import get_num_tables, get_cell_pointers, get_table_name, get_schema_info
from page import read_page_cells, read_record_values
from query import get_column_index

database_file_path = sys.argv[1]
command = sys.argv[2]

if command == ".dbinfo":
    with open(database_file_path, "rb") as database_file:
        database_file.seek(16)
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        print(f"database page size: {page_size}")
        num_tables = get_num_tables(database_file)
        print(f"number of tables: {num_tables}")

elif command == ".tables":
    with open(database_file_path, "rb") as database_file:
        num_tables = get_num_tables(database_file)
        cell_pointers = get_cell_pointers(database_file, num_tables)
        table_names = get_table_name(database_file, cell_pointers)
        print(" ".join(table_names))

elif command.upper().startswith("SELECT"):
    parts = command.split()
    table_name = parts[-1]
    columns_part = command.split("SELECT")[1].split("FROM")[0].strip()

    with open(database_file_path, "rb") as database_file:
        database_file.seek(16)
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        num_tables = get_num_tables(database_file)
        cell_pointers = get_cell_pointers(database_file, num_tables)
        rootpage, sql = get_schema_info(database_file, cell_pointers, table_name)
        page_offset = (rootpage - 1) * page_size
        table_cell_pointers = read_page_cells(database_file, page_offset, page_size)

        if columns_part.upper() == "COUNT(*)":
            print(len(table_cell_pointers))
        else:
            where_col = None
            where_val = None
            if "WHERE" in command.upper():
                where_col, where_val = command.split("WHERE")[1].strip().split("=")
                where_col = where_col.strip()
                where_val = where_val.strip().strip("'\"")

            select_cols = [c.strip() for c in columns_part.split(",")]

            for cell_pointer in table_cell_pointers:
                values = read_record_values(database_file, cell_pointer)
                if sql:
                    if where_col:
                        where_idx = get_column_index(sql, where_col)
                        if where_idx >= 0 and where_idx < len(values):
                            if str(values[where_idx]) != where_val:
                                continue
                    if select_cols == ["*"]:
                        print(" | ".join(str(v) for v in values))
                    else:
                        row_values = []
                        for col in select_cols:
                            idx = get_column_index(sql, col)
                            if idx >= 0 and idx < len(values):
                                row_values.append(str(values[idx]))
                        print("|".join(row_values))

else:
    print(f"Invalid command: {command}")
