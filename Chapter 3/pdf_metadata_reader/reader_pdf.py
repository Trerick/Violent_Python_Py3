#Program to extract metadata from a specified PDF
#Chapter 3 converted Python2 to Python3

from PyPDF2 import PdfFileReader
import PyPDF2
import argparse


def showData(fileID):
	tarPdf = PdfFileReader(fileID, 'rb')
	pdfInfo = tarPdf.getDocumentInfo()
	print("[*] PDF MetaData For: " + str(fileID))
	for metaItem in pdfInfo:
		print("[+]" + metaItem + ':' + pdfInfo[metaItem])

def main():
	argsParser = argparse.ArgumentParser()
	argsParser.add_argument('-F', '--fileID', help="specify PDF file name")
	args = argsParser.parse_args()
	fileID = args.fileID
	
	if (fileID is None):
		argsParser.print_help()
		exit(0)
	else:
		showData(fileID)

if __name__ == '__main__':
	main()
