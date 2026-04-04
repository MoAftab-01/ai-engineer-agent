# temporary script (backend/reset_db.py)
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1407",  # 🔥 replace
    host="localhost",
    port="5432"
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("DROP DATABASE agent_memory;")
cursor.execute("CREATE DATABASE agent_memory;")

print("✅ Database reset")

cursor.close()
conn.close()