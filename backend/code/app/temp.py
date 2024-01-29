import psycopg2 as ps

DB_URL: str = "postgresql://root@172.69.0.4:5432/root"
conn = ps.connect(dbname="root", user="root", host="172.69.0.4")

cur = conn.cursor()
cur.execute("select * from skills")

for record in cur:
    print(record)

cur.close()
conn.close()