import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="PixelAdvant@123",
    database="travel_crm",
    port=3306
)
print("✅ Connected successfully")
conn.close()
print("✅ Connection closed")