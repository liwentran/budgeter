import psycopg
import psycopg.conninfo


def connect(database: str | None) -> psycopg.Connection:
    """Connect to the PostgreSQL database server"""
    try:
        with open("/run/secrets/db-password", "r") as f:
            password = f.read().strip()
        if database:
            conn = psycopg.connect(
                f"host=db user=postgres password={password} dbname={database}"
            )
        else:
            conn = psycopg.connect(f"host=db user=postgres password={password}")
        print("Connected to the PostgreSQL server.")
        conn._set_autocommit(True)
        return conn
    except (psycopg.DatabaseError, Exception) as error:
        print("Unable to connect to database")
        raise error


def reset_database(database: str):
    conn = connect(database=None)
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {database}")
        cur.execute(f"CREATE DATABASE {database}")
    conn.close()
    print(f"Database {database} has been reset")


def reset_transactions_table(database: str, table: str):
    conn = connect(database=database)
    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {table}")
        cur.execute(
            f"CREATE TABLE {table} (name VARCHAR(255), description VARCHAR(255))"
        )
    conn.close()
    print(f"Table {table} in database {database} has been reset")


def add_transaction(database: str, table: str, name: str, description: str):
    conn = connect(database=database)
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO {table} (name, description) VALUES (%s, %s)",
            (name, description),
        )
    conn.close()
    print(f"Values inserted in table {table} in database {database}")
