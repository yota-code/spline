import sys

import numpy as np
import matplotlib.pyplot as plt
		
class spline(object) :
	def __init__(self):
		self.t = 0.0
		self.N_dict = {}
		self.k = 3
		self.n = 4
		self.ti = [0,0,0,1.5,2.0,2.0,2.0]
		self.x = [1,2,3,4]
		self.y = [2,1,2,1]
		
		self.cx = []
		self.cy = []
		
		self.dx = []
		self.dy = []
		
	def div_t(self, n, d) :
		#print >>sys.stderr, "div_t(%0.2f, %0.2f)" % (n, d)
		if d == 0.0 :
			if n == 0.0 :
				return 0
			else :
				return 1
		else :
			return n / d
		
	def N(self, i, k, t) :
		if (i,k) not in self.N_dict :
			self.N_dict[(i,k)] = {}
		if k == 1 :
			if self.ti[i] <= t <= self.ti[i+1] :
				self.N_dict[(i,k)][t] = 1
				return 1
			else :
				self.N_dict[(i,k)][t] = 0
				return 0
		else :
			u =  self.N(i  , k-1, t) * self.div_t(t       - self.ti[i] , self.ti[i+k-1] - self.ti[i]  )
			u += self.N(i+1, k-1, t) * self.div_t(self.ti[i+k] - t     , self.ti[i+k]   - self.ti[i+1])
			self.N_dict[(i,k)][t] = u
			return u
			
	def N_prime(self, i, k, t) :
		if k == 1 :
			return 0
		else :
			u =  self.N_prime(i   , k-1, t) * self.div_t(t - self.ti[i] , self.ti[i+k-1] - self.ti[i]  )
			u +=       self.N(i   , k-1, t) * self.div_t(             1 , self.ti[i+k-1] - self.ti[i]  )
			u += self.N_prime(i+1 , k-1, t) * self.div_t(self.ti[i+k] - t , self.ti[i+k]   - self.ti[i+1])
			u +=       self.N(i+1 , k-1, t) * self.div_t(         -1 , self.ti[i+k]   - self.ti[i+1])
			return u
			
	def curve(self, t = None) :
		cx = 0.0
		cy = 0.0
		dx = 0.0
		dy = 0.0
		if t == None :
			t = self.t
		for i in range(self.n) :
			#print >>sys.stderr, i, self.k, t, self.N(i, self.k, t) * self.x[i + 1], self.N(i, self.k, t) * self.y[i + 1]
			cx += self.N(i, self.k, t) * self.x[i]
			cy += self.N(i, self.k, t) * self.y[i]
			dx += self.N_prime(i, self.k, t) * self.x[i]
			dy += self.N_prime(i, self.k, t) * self.y[i]
			
		self.cx.append(cx)
		self.cy.append(cy)
		
		self.dx.append(dx)
		self.dy.append(dy)
		
		self.t += 0.005
		
		return cx, cy
		
			
	def plot(self) :
		pass
	

b = spline()
while b.t < 2.0 :
	print "%0.15f" % b.t
	b.curve()

plt.subplot(2,1,1)
plt.plot(b.cx, b.cy, b.x, b.y)
plt.subplot(2,1,2)
plt.plot(b.cx)
plt.plot(b.cy)
plt.plot(b.dx)
plt.plot(b.dy)
plt.show()

print b.curve(2.0)
