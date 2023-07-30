import threading
from ping3 import ping


def ping_range(start_ip, end_ip):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))

    ip_range = []
    ip_range.append(start_ip)

    while start != end:
        start[3] += 1
        for i in range(3, 0, -1):
            if start[i] == 256:
                start[i] = 0
                start[i - 1] += 1
        ip_range.append('.'.join(map(str, start)))

    return ip_range


start_ip = input("Start IP:")
end_ip = input("End IP:")

ip_range = ping_range(start_ip, end_ip)
correctIPs = []


def check_ip(ip):
    try:
        if ping(ip):
            correctIPs.append(ip)
    except:
        pass


threads = []

for ip in ip_range:
    t = threading.Thread(target=check_ip, args=(ip,))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

with open("Correct_IP.txt", "w") as f:
    for ip in correctIPs:
        f.write(ip + "\n")

print("Scanning done.")
