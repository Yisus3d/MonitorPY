import os
import socket
from datetime import datetime
import mysql.connector
import requests



mydb = mysql.connector.connect(
	host="localhost",
	user="user",
	password="password",
	database="database"
)

def bot_sendtext(bot_message):
   bot_token = 'yourtoke'
   bot_chatID = 'yourchatid'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)
   return response.json()


def servertest(host,port):
    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for family, socktype, proto, canonname, sockaddr in args:
        s = socket.socket(family, socktype, proto) 
    try:
        s.settimeout(10)
        s.connect(sockaddr)
        s.settimeout(None)
    except socket.error:
        return False
    else:
        s.close() 
    return True

def ping(host):
    response = os.system("ping -c 2 -n -i 0.2 -W1 " + host)
    if response == 0:
        return True
    else:
         return False

def test_ports(time,hostserver,hostports):
    if ping(hostserver):
                if  servertest(hostserver,hostports):
                    status = "OK"
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO log (host, port, status, time) VALUES (%s, %s, %s, %s)"
                    val = (hostserver,hostports,status,time)
                    mycursor.execute(sql, val)
                    mydb.commit()
                else:
                    status = "NOT OK"
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO log (host, port, status, time) VALUES (%s, %s, %s, %s)"
                    val = (hostserver,hostports,status,time)
                    mycursor.execute(sql, val)
                    mydb.commit()
    else:
                    status = "NOT PING"
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO log (host, port, status, time) VALUES (%s, %s, %s, %s)"
                    val = (hostserver,hostports,status,time)
                    mycursor.execute(sql, val)
                    mydb.commit()

