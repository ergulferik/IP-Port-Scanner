import socket
import threading

from queue import Queue

ip_and_port = []


def scan(targetIP):
    global ip_and_port

    t_IP = socket.gethostbyname(targetIP)
    socket.setdefaulttimeout(0.25)
    print_lock = threading.Lock()

    def portscan(port):

        global ip_and_port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((t_IP, port))
            with print_lock:
                ip_and_port.append(str(t_IP) + ":" + str(port))
            con.close()
        except:
            pass

    def threader():
        while True:
            workers = q.get()
            portscan(workers)
            q.task_done()

    q = Queue()

    for x in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1, 500):
        q.put(worker)

    q.join()


correctIPs = []

with open("Correct_IP.txt") as f:
    for i in f.readlines():
        correctIPs.append([i.strip()])

for i in correctIPs:
    scan(i[0])

for ip in correctIPs:
    for i in ip_and_port:
        arr = str(i).split(":")
        if ip[0] == arr[0]:
            ip.append(arr[1])

for i in correctIPs:
    if len(i) > 1:
        print(i[0], " is reachable and ports are : ")
        for j in range(1, len(i)):
            print(i[j])
    else:
        print(i[0], " is reachable but have not port")
