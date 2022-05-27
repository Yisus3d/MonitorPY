import socket

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


if __name__ == "__main__":
    for port in hostports:
        for hosts in hostserver:
            if  servertest(hosts,port):
                status = "OK"
                print("Funciona el Port {} en el host {}".format(port,hosts))

            else:
                status = "NOT OK"
                print("No Funciona el Port {} en el host {}".format(port,hosts))
