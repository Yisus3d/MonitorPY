import socket
import mysql.connector
import datetime
from flask import Flask, render_template
 
 
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="database"
)
 
def servertest(host,port):
    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for family, socktype, proto, canonname, sockaddr in args:
        s = socket.socket(family, socktype, proto)
    try:
        s.connect(sockaddr)
    except socket.error:
        return False
    else:
        s.close()
    return True
 
hostserver = ['127.0.0.1','192.168.1.1','192.168.0.1']
hostports = ["80","443","22","3306"]
 
x = datetime.datetime.now()
 
 
if __name__ == "__main__":
    for port in hostports:
        for hosts in hostserver:
            if  servertest(hosts,port):
                status = "OK"
                mycursor = mydb.cursor()
                time = x.strftime("%d/%m/%Y %X")
                sql = "INSERT INTO log (host, port, status, time) VALUES (%s, %s, %s, %s)"
                val = (hosts,port,status,time)
                mycursor.execute(sql, val)
                mydb.commit()
            else:
                status = "NOT OK"
                mycursor = mydb.cursor()
                time = x.strftime("%d/%m/%Y %X")
                sql = "INSERT INTO log (host, port, status, time) VALUES (%s, %s, %s, %s);"
                val = (hosts,port,status,time)
                mycursor.execute(sql, val)
                mydb.commit()
 
    mycursor = mydb.cursor()
    sql = "select * from log order by time desc;"
    mycursor.execute(sql)
    records = mycursor.fetchall()
    print("('host', 'port' , 'status' , 'time')")
    for record in records:
        print(record)
    mydb.commit()
 
    app = Flask(__name__)
    @app.route('/')
    def homepage():
        return render_template("index.html",hostserver = hostserver, hostports = hostports, time = x.strftime("%d/%m/%Y %X"))
    app.jinja_env.globals.update(servertest=servertest)
    app.run(use_reloader = True, debug = True , host='192.168.2.4', port=8000)
