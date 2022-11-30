import numpy as np

#   int i1 = 0;
#	for (int l = 0; l < w2; l++) {
#		while (t >= ti[i1] ) i1++;
#		int i = i1-1;
#		col[l] = iColor[(i+8-k) % 7];
#		for (int j = 0; j < nt; j++) N[j][l] = 0;
#		N[i][l] = 1;
#		for (int m = 2; m <= k; m++) {
#			int jb = i-m+1;  if (jb < 0) jb = 0;
#			for (int j = jb; j <= i; j++) {
#				N[j][l] = N[j][l]*(t - ti[j])/(ti[j+m-1] - ti[j]) + N[j+1][l]*(ti[j+m] - t)/(ti[j+m] - ti[j+1]);
#			}
#		}
#		t += step;
#	}

ti = np.array([0,0,0,1,2,3,4,4,4], dtype=np.float64)

x = np.array([0,2,5,8,7], dtype=np.float64)
y = np.array([2,4,5,3,5], dtype=np.float64)

k = 3
n = 5

i1 = 0
t = 0
for l in np.arange(0, 5) :
	while t >= ti[i1] :
		i1 += 1
	i = i1 - 1
	for m in np.arange(2, k+1) :
		jb = i - m + 1
		if jb < 0 :
			jb = 0
		for j in np.arange(jb, i + 1) :
			a = "\n"
			a += " "*27
			a += "t - t%d" %(j,)
			a += " "*19
			a += "t%d - t \n" % (j+m,)
			a += "N(%d, %d, t) = " % (j, m)
			a += "N(%d, %d, t) * " % (j, m-1)
			a += "--------- + "
			a += "N(%d, %d, t) * " % (j+1, m-1)
			a += "--------- \n"
			a += " "*27
			a += "t%d - t%d" % (j+m-1, j)
			a += " "*18
			a += "t%d - t%d" % (j+m, j+1)
			print a
	t += 0.1



