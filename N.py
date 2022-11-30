import numpy as np
import sys

ti = range(16)

def N(i, k, t) :
	if k == 1 :
		if ti[i] <= t <= ti[i+1] :
			print >>sys.stderr, "\nN(%d, %d, t) = 1" % (i, k)
			return 1
		else :
			print >>sys.stderr, "\nN(%d, %d, t) = 0" % (i, k)
			return 0
	else :
		a = "\n"
		a += " "*27
		a += "t - t%d" %(i,)
		a += " "*19
		a += "t%d - t \n" % (i+k,)
		a += "N(%d, %d, t) = " % (i, k)
		a += "N(%d, %d, t) * " % (i, k-1)
		a += "--------- + "
		a += "N(%d, %d, t) * " % (i+1, k-1)
		a += "--------- \n"
		a += " "*27
		a += "t%d - t%d" % (i+k-1, i)
		a += " "*18
		a += "t%d - t%d" % (i+k, i+1)
		print >>sys.stderr, a
		return N(i, k-1, t) * (t - ti[i]) / (ti[i+k-1] - ti[i]) + N(i+1, k-1, t) * (ti[i+k] - t) / (ti[i+k] - ti[i+1])
		
		
N(int(sys.argv[1]),int(sys.argv[2]),0.0)

