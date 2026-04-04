import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",   # or agent_memory if created
        user="postgres",
        password="1407",  # 🔥 change this
        host="localhost",
        port="5432"
    )

    print("Connected successfully 🚀")

    conn.close()

except Exception as e:
    print("Error:", e)