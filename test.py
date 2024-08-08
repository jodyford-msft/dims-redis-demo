import pyodbc

server = 'dims-sql-server.database.windows.net'
database = 'dims-sql'
connection_string = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server={server};"
    f"Database={database};"
    f"Authentication=ActiveDirectoryMsi;"
)

connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    ""
    "Database=VectorBlack;"
    "Uid=vectorblacknet-server-admin;"
    ""
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

try:
    with pyodbc.connect(connection_string) as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")