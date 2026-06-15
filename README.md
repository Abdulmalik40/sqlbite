# SQLite Reader

A minimal SQLite file parser built in Python 

## Usage

```sh
python app/main.py <database.db> "<command>"
```

## Commands

**Show database info**
```sh
python app/main.py sample.db .dbinfo
```

**List tables**
```sh
python app/main.py sample.db .tables
```

**Count rows**
```sh
python app/main.py sample.db "SELECT COUNT(*) FROM apples"
```

**Select specific columns**
```sh
python app/main.py sample.db "SELECT id, name FROM apples"
```

**Filter with WHERE**
```sh
python app/main.py sample.db "SELECT name FROM apples WHERE color = 'yellow'"
```

## Project Structure

```
app/
├── main.py       - entry point, command handling
├── varint.py     - varint decoding
├── schema.py     - sqlite_schema parsing (tables, rootpage, sql)
├── page.py       - page and record reading
└── query.py      - column index lookup and WHERE filtering
```

## Sample Databases

A `sample.db` file is included in the repository with two tables: `apples` and `oranges`.

Additional test databases can be downloaded by running:

```sh
./download_sample_databases.sh
```

## Requirements

Python 3.7+
