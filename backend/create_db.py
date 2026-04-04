import psycopg2

try:
    # connect to default postgres DB
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1407",  # 🔥 replace
        host="localhost",
        port="5432"
    )

    conn.autocommit = True
    cursor = conn.cursor()

    # create database
    cursor.execute("CREATE DATABASE agent_memory;")

    print("✅ Database 'agent_memory' created successfully!")

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)