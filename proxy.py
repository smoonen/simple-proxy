import select
import socket
import threading

def listen_thread(sip, dip, port) :
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  s.bind((sip, port))
  s.listen(10)
  while True :
    conn, addr = s.accept()
    print("Connection on %s:%d" % (sip, port))
    x = threading.Thread(target = proxy_thread, args = (conn, dip, port))
    x.start()

def proxy_thread(conn, dip, port) :
  conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  conn2.connect((dip, port))
  excep_count = 0
  while True :
    readable, writeable, exceptional = select.select([conn, conn2], [], [conn, conn2])
    if conn in readable :
      data = conn.recv(4096)
      conn2.send(data)
      excep_count = 0
    if conn2 in readable :
      data = conn2.recv(4096)
      conn.send(data)
      excep_count = 0
    if conn in exceptional or conn2 in exceptional :
      excep_count = excep_count + 1
      if excep_count > 1 :
        conn.close()
        conn2.close()
        return

t1 = threading.Thread(target = listen_thread, args = ("10.209.185.115", "10.73.96.254", 80))
t2 = threading.Thread(target = listen_thread, args = ("10.209.185.115", "10.73.96.254", 443))
t3 = threading.Thread(target = listen_thread, args = ("10.209.185.116", "10.73.96.196", 80))
t4 = threading.Thread(target = listen_thread, args = ("10.209.185.116", "10.73.96.196", 443))
t1.start()
t2.start()
t3.start()
t4.start()
