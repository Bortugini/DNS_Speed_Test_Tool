# _*_ coding: utf-8 _*_
import subprocess
import threading
from _datetime import datetime
import time

class dnsTest(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        global timeDns
        f = True
        i = 0
        lim.acquire()
        while f:
            out = subprocess.Popen("ping -n 1 " + self.ip, encoding="437", shell=True, stdout=subprocess.PIPE
                                   , stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            out = out.stdout.read()
            time.sleep(5)
            # Attempt ping 3 times, then abort on failure.
            if "Lost = 1" in out:
                i += 1
                if i == 3:
                    out = out.split("for")[1].split("with")[0]
                    out = out.strip(" ").split(":")[0]
                    lock.acquire()
                    print("No connection to: " + out)
                    lock.release()
                    f = False
            else:
                out = out.split("time=")[1].split("TTL")[0]
                out = out.strip(" ")
                lock.acquire()
                timeDns.append(out + ":" + self.ip)
                lock.release()
                f = False
        lim.release()

def output(diff, timeDns):
    print("\n"*3 + "Server speed in descending order:\n" + "-"*32)
    for i in timeDns:
        print("Ping " + str(i[0]) + "ms for " + i[1])
        print("-"*32)
    print("Total test time: " + str(diff))

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
    try:
        file = open("DNS Server.txt", "r").read() # path to file
        ip = file.splitlines()
        return ip
    except:
        print("DNS Server.txt could not be opened.")

# Main code section #
print("Pinging servers, please wait.. (No progress is shown)")
# Global Variables
timeDns = []

ip = openIp()
lock = threading.Lock()
tstart = datetime.now()

# Maximum number of threads
maxThred = 100
lim = threading.Semaphore(value=maxThred)
threads = []

# Create threads
for i in range(len(ip)):
    thread = dnsTest(ip[i])
    threads.append(thread)
# Starts all threads in threads
for thread in threads:
    thread.start()
# Waits for all threads within threads to finish
for thread in threads:
    thread.join()

timeDns = sortTime(timeDns)
tend = datetime.now()
diff = tend - tstart
output(diff, timeDns)
