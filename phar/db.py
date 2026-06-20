import mysql.connector
# Database connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="7dubai9hotel0RESORT",
        database="pharmacy_db"
    )
    