# _*_ coding: utf-8 _*_
import subprocess
import threading
from datetime import datetime
import time
import os

class dnsTest(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        global dns_time
        f = True
        i = 0
        lim.acquire()
        while f:
            out = subprocess.Popen("ping -n 1 " + self.ip, encoding="437", shell=True, stdout=subprocess.PIPE
                                   , stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            out = out.stdout.read()
            time.sleep(5)
            # Wen ping keine Antwort erhält wird 3 mal versucht sonst abgebrochen
            if "Verloren = 1" in out:
                i += 1
                if i == 3:
                    out = out.split("für")[1].split("mit")[0]
                    out = out.strip(" ")
                    lock.acquire()
                    print("Keine Verbindung zu: " + out)
                    lock.release()
                    f = False
            else:
                out = out.split("Zeit=")[1].split("TTL")[0]
                out = out.strip(" ")
                lock.acquire()
                dns_time.append(out + ":" + self.ip)
                lock.release()
                f = False
        lim.release()

def print_result(diff, timeDns):
    for i in timeDns:
        print("Zeit " + str(i[0]) + "ms für " + i[1])
        print("--------------------------------")
    print("Zeit für den Test: " + str(diff))

def sortTime(str):
    buffer = []
    for i in range(len(str)):
        res = str[i].split(":")
        tub = tuple((res[0], res[1]))
        tub = list(tub)
        tub[0] = tub[0].strip('ms')
        tub[0] = int(tub[0])
        buffer.append(tub)
    buffer.sort()
    return buffer

def openIp():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(ROOT_DIR + "\DNS Server.txt") as file:
        lines = file.read().splitlines()
    return lines

#Globale Variable
dns_time = []

ip = openIp()
lock = threading.Lock()
start_time = datetime.now()

#Maximale Anzahl Threads
maxThreads = 100
lim = threading.Semaphore(value=maxThreads)
threads = []

# erzeugt Threads
for i in range(len(ip)):
    thread = dnsTest(ip[i])
    threads.append(thread)
# Startet alle Threads in threads
for thread in threads:
    thread.start()
# Wartet auf beenden von allen Threads in threads
for thread in threads:
    thread.join()

dns_time = sortTime(dns_time)
end_time = datetime.now()
diff_time = end_time - start_time
print_result(diff_time, dns_time)
