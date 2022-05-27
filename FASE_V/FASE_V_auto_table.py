#!usr/bin/python3
import sys
import os
import socket
import datetime
from db_connect import db_connection
import requests


hostserver = ['127.0.0.1','192.168.1.1','192.168.0.1']
hostports = ["80","443","22","3306"]
x = datetime.datetime.now()
mydb = db_connection()

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

def message_len():
    hostss = len(hostserver)
    portss = len(hostports)
    all = hostss*portss
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT host, port, status, time, id FROM log ORDER BY id DESC LIMIT %s", (all))
    logs = mycursor.fetchall()
    logs = str(logs)
    bot_sendtext("Created AUTO \nhost, port, status, time, id\n"+logs)
    mydb.commit()

def show_tables_telegram():
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT  host, port, status, time, id FROM log")
    logs = mycursor.fetchall()
    logs = str(logs)
    bot_sendtext("Log Table\nhost, port, status, time, id\n"+logs)
    mydb.commit()

def delete_data_log():
    mydb = db_connection()
    log = []
    with mydb.cursor() as cursor:
        cursor.execute("SELECT  host, port, status, time, id FROM log")
        log = cursor.fetchall()
        log = str(log)
        bot_sendtext("DESTROYED TABLE\n"+log)
        cursor.execute("TRUNCATE TABLE log")
    mydb.commit()
    mydb.close()

def no_works_log():
    mydb = db_connection()
    log = []
    with mydb.cursor() as cursor:
        cursor.execute("SELECT  host, port, status, time, id FROM log WHERE status != 'OK' ")
        log = cursor.fetchall()
        log = str(log)
        bot_sendtext("No works\n"+log)
    mydb.commit()
    mydb.close()

def test_ports():
    for port in hostports:
        for host in hostserver:    
            if ping(host):
                        if  servertest(host,port):
                            status = "OK"
                            time = x.strftime("%d/%m/%Y %X")
                            with mydb.cursor() as mycursor:
                                mycursor.execute("INSERT INTO log(host, port, status,time) VALUES (%s, %s, %s,%s)",
                                    (host, port, status, time))
                            mydb.commit()
                        else:
                            status = "NOT OK"
                            time = x.strftime("%d/%m/%Y %X")
                            with mydb.cursor() as mycursor:
                                mycursor.execute("INSERT INTO log(host, port, status,time) VALUES (%s, %s, %s,%s)",
                                    (host, port, status, time))
                            mydb.commit()
            else:
                            status = "NOT PING"
                            time = x.strftime("%d/%m/%Y %X")
                            with mydb.cursor() as mycursor:
                                mycursor.execute("INSERT INTO log(host, port, status,time) VALUES (%s, %s, %s,%s)",
                                    (host, port, status, time))
                            mydb.commit()
    message_len()
test_ports()
