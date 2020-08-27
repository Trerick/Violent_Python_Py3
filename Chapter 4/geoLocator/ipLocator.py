#Program to iterate through captured packet data contained within a pcap file
#and displaying the source and destination address
#Chapter 4 converted from Python2 to Python3

import geoip2.database
import dpkt
import socket
import argparse

reader = geoip2.database.Reader('#Input geolite2_city.mmdb dir location here#')

def getGeo(ip):
	try:
		response = reader.city(ip)
		tgtCity = response.city.name
		tgtCountry = response.country.iso_code
		if tgtCity != None:
			geoLoc = tgtCity + ', ' + tgtCountry
		else:
			geoLoc = tgtCountry
			
		return geoLoc
		
	except Exception as e:
		return "Unregistered"
		
def showPcap(pcap):
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			print("[+] Src: " + src + "--> Dst: " + dst)
			print("[+] Src: " + getGeo(src) + "--> Dst: " \
				+ getGeo(dst))
		except:
			pass
			
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--pcapFile', help="specify pcap file")
	args = parser.parse_args()
	if args.pcapFile == None:
		parser.print_help()
		exit(0)
	pcapFile = args.pcapFile
	f = open(pcapFile, 'rb')
	pcap = dpkt.pcap.Reader(f)
	showPcap(pcap)
	
if __name__ == '__main__':
	main()
	
