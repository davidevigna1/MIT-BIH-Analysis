import mysql.connector
import pandas as pd

df = pd.read_csv('data_analysis.csv')

config = {
    "host": "localhost",
    "user": "root",
    "password": ""
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # 1) Creation of the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
    cursor.execute("USE hospital_db")
    print("Database 'hospital_db' ready.")

    # 2) Creation of the table
    cursor.execute("DROP TABLE IF EXISTS patients_records")
    
    create_table_query = """
    CREATE TABLE patients_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ID_Paziente VARCHAR(50) NOT NULL,
        BPM FLOAT NOT NULL,
        Stato VARCHAR(50) NOT NULL,
        Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_query)

    # 3) Insertion of the data
    insert_query = "INSERT INTO patients_records (ID_Paziente, BPM, Stato) VALUES (%s, %s, %s)"
    
    data = [tuple(row) for row in df.values]
    
    cursor.executemany(insert_query, data)
    conn.commit()
    print(f"Success: {cursor.rowcount} rows inserted correctly.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed.")