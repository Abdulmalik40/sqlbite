def get_column_index(sql, column_name):
    start = sql.index("(") + 1
    end = sql.rindex(")")
    columns_str = sql[start:end]
    columns = [col.strip() for col in columns_str.split(",")]
    for i, col in enumerate(columns):
        col_name = col.strip().split()[0]
        if col_name.lower() == column_name.lower():
            return i
    return -1
