#Banner Grabber program to scan for open ports and display the banner information
#Chapter 2 converted Python2 to Python3

import argparse
import socket
import threading

screenLock = threading.Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'ViolentPython3\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print("[+] %d/tcp open" % tgtPort)
        print('[+] ' + str(results))
        
    except:
        screenLock.acquire()
        print("[-] %d/tcp closed" % tgtPort)
        
    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    
    try:
        tgtIp = socket.gethostbyname(tgtHost)
        
    except:
        print("[-] Cannot resolve '%s': Unkown host" % tgtHost)
        return

    try:
        tgtName = socket.gethostbyaddr(tgtIp)
        print("\n[+] Scan Results for: " + tgtName[0])
        
    except:
        print("\n[+] Scan Results for: " + tgtIp)

    socket.setdefaulttimeout(1)
    
    for tgtPort in tgtPorts:
        t = threading.Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument('-H', '--host', help="specify target host")
    argsParser.add_argument('-P', '--port', help="specify target port[s] \
                             separated by comma")
    args = argsParser.parse_args()

    tgtHost = args.host
    tgtPorts = str(args.port).split(',')

    if (tgtHost is None) | (tgtPorts[0] is None):
        argsParser.print_help()
        exit(0)

    portScan(tgtHost, tgtPorts)


if __name__ == '__main__':
    main()
