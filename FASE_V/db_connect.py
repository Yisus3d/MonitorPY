import pymysql

def db_connection():
    return pymysql.connect(
        host="localhost",
        user="user",
        password="password",
        db="database"
    )
