from db_connect import db_connection
import FASE_V_data as data
import datetime


def delete_data_log():
    mydb = db_connection()
    log = []
    with mydb.cursor() as cursor:
        cursor.execute("SELECT  host, port, status, time, id FROM log")
        log = cursor.fetchall()
        log = str(log)
        data.bot_sendtext("DESTROYED TABLE\n"+log)
        cursor.execute("TRUNCATE TABLE log")
    mydb.commit()
    mydb.close()

def create_data_logs(host, port):
    x = datetime.datetime.now()
    time = x.strftime("%d/%m/%Y %X")
    hosts = host.split(',')
    ports = port.split(',')
    print (hosts,ports)
    for portt in ports:
            for hostt in hosts:
                data.test_ports(time,hostt,portt)
    hostss = len(hosts)
    portss = len(ports)
    all = hostss*portss
    mydb = db_connection()
    with mydb.cursor() as cursor:
        cursor.execute("SELECT host, port, status, time, id FROM log ORDER BY id DESC LIMIT %s", (all))
        logs = cursor.fetchall()
        logs = str(logs)
        data.bot_sendtext("Created \nhost, port, status, time, id\n"+logs)
    mydb.commit()
    mydb.close()


def default_data_logs():
    x = datetime.datetime.now()
    time = x.strftime("%d/%m/%Y %X")
    hostserver = ['127.0.0.1','192.168.1.1','192.168.0.1']
    hostports = ["80","443","22","3306"]
    for port in hostports:
            for host in hostserver:
                data.test_ports(time,host,port)
    hosts = len(hostserver)
    ports = len(hostports)
    all = hosts*ports
    mydb = db_connection()
    with mydb.cursor() as cursor:
        cursor.execute("SELECT host, port, status, time, id FROM log ORDER BY id DESC LIMIT %s", (all))
        logs = cursor.fetchall()
        logs = str(logs)
        data.bot_sendtext("Created \nhost, port, status, time, id\n"+logs)
    mydb.commit()
    mydb.close()


def put_log(host, port, status):
    x = datetime.datetime.now()
    time = x.strftime("%d/%m/%Y %X")
    host_put = host + "(manual)"
    mydb = db_connection()
    with mydb.cursor() as cursor:
        cursor.execute("INSERT INTO log(host, port, status,time) VALUES (%s, %s, %s,%s)",
                       (host_put, port, status, time))
        cursor.execute("SELECT host, port, status, time, id FROM log ORDER BY id DESC LIMIT 1")
        logs = cursor.fetchall()
        for log in logs:
            host = log[0]
            port = log[1]
            status = log[2]
            time= log[3]
            id = log[4]
            data.bot_sendtext('Created Manual\nid|host|port|status|time\n{}|{}|{}|{}|{}'.format(id,host,port,status,time))
    mydb.commit()
    mydb.close()


def get_logs():
    mydb = db_connection()
    log = []
    with mydb.cursor() as cursor:
        cursor.execute("SELECT  host, port, status, time, id FROM log")
        log = cursor.fetchall()
    mydb.close()
    return log


def delete_log(id):
    mydb = db_connection()
    with mydb.cursor() as cursor:
        cursor.execute("SELECT  host, port, status, time, id FROM log WHERE id = %s", (id))
        logs = cursor.fetchall()
        for log in logs:
            host = log[0]
            port = log[1]
            status = log[2]
            time= log[3]
            id = log[4]
            data.bot_sendtext('Deleted\nid|host|port|status|time\n{}|{}|{}|{}|{}'.format(id,host,port,status,time))
        cursor.execute("DELETE FROM log WHERE id = %s", (id,))
    mydb.commit()
    mydb.close()


def get_log_id(id):
    mydb = db_connection()
    log = None
    with mydb.cursor() as cursor:
        cursor.execute(
            "SELECT host, port, status, time, id FROM log WHERE id = %s", (id))
        log = cursor.fetchone()
    mydb.close()
    return log

def telegram_log():
    mydb = db_connection()
    log = []
    with mydb.cursor() as cursor:
        cursor.execute("SELECT  host, port, status, time, id FROM log")
        logs = cursor.fetchall()
        logs = str(logs)
        data.bot_sendtext("Log Table\nhost, port, status, time, id\n"+logs)
    mydb.close()


def update_log(host, port, status, id):
    x = datetime.datetime.now()
    time = x.strftime("%d/%m/%Y %X")
    if "edited" in host:
        host_edited= host
    else:
        host_edited= host + "(edited)" 
    mydb = db_connection()
    with mydb.cursor() as cursor:
        cursor.execute("UPDATE log SET host = %s, port = %s, status = %s, time = %s WHERE id = %s",
                       (host_edited, port, status,time, id))
        cursor.execute("SELECT  host, port, status, time, id FROM log WHERE id = %s", (id))
        logs = cursor.fetchall()
        logs = str(logs)
        data.bot_sendtext("Updated\nhost, port, status, time, id\n"+logs)
    mydb.commit()
    mydb.close()
