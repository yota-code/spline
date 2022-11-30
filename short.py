import sys
import string

fid = open(sys.argv[1])

line = 0
a = ""

for i in fid.read() :
	line += 1
	if i in string.printable :
		a += i
	else :
		a += "."
	sys.stdout.write("%02x " % ord(i))
	
	if line == 16 :
		sys.stdout.write("\t%s\n" % a)
		a = ""
		line = 0
		
	
