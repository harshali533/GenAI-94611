import mysql.connector

host = "localhost"
user = "root"
password = "******" #replace with your password
database = "gen_ai"

try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    print("Connected to MYSQL databases!")

    #Create a cursor to execute queries
    cursor = conn.cursor()

    #Example : Fetch tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in databses:",tables)

    #Example : fetch some data
    cursor.execute("SELECT * FROM employees LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    #close cursor and connection
    cursor.close()
    conn.close()
    print("Connection closed.")

except mysql.connector.Error as err:
    print("Error:",err)