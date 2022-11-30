fid = open("all_chr.txt", 'w')

for i in range(256) :
	fid.write(chr(i))
