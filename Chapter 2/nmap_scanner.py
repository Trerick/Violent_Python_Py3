#Nmap integration to scan for open ports on specified target
#Chapter 2 converted Python2 to Python3

import nmap
import argparse

def nmapScan(tgtHost, tgtPort):
	nmScan = nmap.PortScanner()
	nmScan.scan(tgtHost, tgtPort)
	state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
	print("[+] " + tgtHost + " tcp/" + tgtPort + " " + state)
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-H', '--host', help="specify target host")
	parser.add_argument('-P', '--port', help="specify target port[s] separated by commas")
	args = parser.parse_args()
	
	tgtHost = args.host
	tgtPorts = str(args.port).split(',')
	
	if (tgtHost is None) | (tgtPorts[0] is None):
		parser.print_help()
		exit(0)
	for tgtPort in tgtPorts:
		nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
	main()
