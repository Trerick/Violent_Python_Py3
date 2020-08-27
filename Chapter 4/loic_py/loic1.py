#Program to check data of a pcap file
#Additional task to ensure data contained within the pcap matches the DDosAnalyzer

import dpkt
import socket

with open('download.pcap', "rb") as f:
    pcap = dpkt.pcap.Reader(f)
    for t, buf in pcap:
        print(str(t) + ': ' + str(len(buf)))
        
        eth = dpkt.ethernet.Ethernet(buf)

        ip = eth.data
        src = ip.src
        dst = ip.dst
        src_a = socket.inet_ntoa(src)
        dst_a = socket.inet_ntoa(dst)
        
        print("Source IP :%s" % src_a)
        print("Destination IP :%s" % dst_a)

