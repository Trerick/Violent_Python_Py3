#Program to iterate through a system and find all filenames based on user input
#E.g. inputting password to find all files containing the name password

import os

def fileLocator():

	input_sub = input('Enter filename or part of filename to search for: ')
	substring = input_sub
	
	for root, dirs, files in os.walk("/home"):
		for file in files:
			types = [".doc", ".docx", ".txt"]
			file.endswith(tuple(types))
			path_file = os.path.join(root, file)
			fullstring = str(path_file)
			
			if substring in fullstring:
				print(path_file)
	
	

def fileContents():

	user_input = input('\n Input file to display contents using directory path: ')
	f = open(user_input, "r")
	
	if f.mode == "r":
		contents = f.read()
		print(contents)
	
	
		

def main():

	fileLocator()
	fileContents()
	
main()
