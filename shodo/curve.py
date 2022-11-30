#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as mpl

"""
	bezier : bicubic bezier curve
	bspline : all order b-spline with starting and ending point
"""

math.sqrt2 = math.sqrt(2.0)

def norm(v, n=2) :
	return np.power(np.sum(np.power(v, n)), 1/n)
	
def divzero(n, d) :
	if d == 0.0 :
		return 0.0
	else :
		return n / d

class curve(object):
	""" generic class for curve plotting """
	
	def trace(self, resolution=25, relative=False):
		a = float(len(self) if relative else 1)
		b = float(resolution)
		c = []
		for u in range(len(self.timeline) - 1) :
			t = self.timeline[u]
			while t <  self.timeline[u+1] :
				c.append(self.position(t))
				t += math.atan((a / b) * (1 / (norm(self.velocity(t))))) / math.sqrt2
		c.append(self.position(self.timeline[u+1]))
		self.curve = np.array(c)
		self.traced = True
		return self.curve
		
	def __len__(self) :
		l = 0.0
		for i in xrange(len(self.p) - 1) :
			l += norm(self.p[i] - self.p[i+1])
		return l
		
	def mpl_plot(self):
		if not self.traced :
			self.trace()
		mpl.plot(self.curve[:,0], self.curve[:,1],"-")
		mpl.plot(self.p[:,0], self.p[:,1])
		mpl.show()
		
if __name__ == '__main__' :
	a = np.array([3.0,4.0])
	print(norm(a))
		
