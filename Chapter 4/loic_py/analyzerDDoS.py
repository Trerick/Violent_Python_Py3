#Program to test if threat actor downloaded the malicious toolkit, /
#Established a connection with the HIVE, and if an attack is curently in progress
#Ensure to specify the pcap file and threshold value
#Chapter 4 converted Python2 to Python3

import dpkt
import argparse
import socket


def findDownload(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    print('[!] ' + src + ' Downloaded LOIC.')
        except Exception as e:
        	print(e)
        	pass

def findHivemind(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            sport = tcp.sport
            print("DPORT: " , dport)
            if dport == 6667:
                if b'!lazor' in tcp.data.lower():
                    print('[!] DDoS Hivemind issued by: '+src)
                    print('[+] Target CMD: ' + str(tcp.data, encoding='utf-8'))
                    

            if sport == 6667:
                if b'!lazor' in tcp.data.lower():
                    print('[!] DDoS Hivemind issued to: '+dst)
                    print('[+] Target CMD: ' + tcp.data)


        except Exception as e:
            print(e)
            pass
            
        
def findAttack(pcap):
    pktCount = {}
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            if dport == 80:
                stream = src + ':' + dst
                if pktCount.has_key(stream):
                    pktCount[stream] = pktCount[stream] + 1
                else:
                    pktCount[stream] = 1
        except Exception as e:
            print(e)
            pass
        
    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print('[+] '+src+' attacked '+dst+' with ' \
                  + str(pktsSent) + ' pkts.')
def main():

    argsParser = argparse.ArgumentParser()
    argsParser.add_argument('-p', '--pcapFile', help="specify pcap file")
    argsParser.add_argument('-t', '--thresh', help="specify theshhold count")
    args = argsParser.parse_args()

    if args.pcapFile is None:
        argsParser.print_help()
        exit(0)

    if args.thresh is None:
        argsParser.print_help()
        exit(0)
		
    pcapFile = args.pcapFile
    f = open(pcapFile, 'rb')
    pcap = dpkt.pcap.Reader(f)
	
    findDownload(pcap)
    findHivemind(pcap)
    findAttack(pcap)

if __name__ == '__main__':
    main()
