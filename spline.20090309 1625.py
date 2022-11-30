import sys

import numpy as np
import matplotlib.pyplot as plt

"""
int i1 = 0;
for (int l = 0; l < w2; l++) {
	while (t >= ti[i1] ) i1++;
	int i = i1-1;
	for (int j = 0; j < nt; j++) N[j][l] = 0;
	N[i][l] = 1;
	for (int m = 2; m <= k; m++) {        //  basis functions calculation
		int jb = i-m+1;  if (jb < 0) jb = 0;
		for (int j = jb; j <= i; j++){
			N[j][l] = N[j][l]*(t - ti[j])/(ti[j+m-1] - ti[j]) +
			N[j+1][l]*(ti[j+m] - t)/(ti[j+m] - ti[j+1]);
		}
	}
	t += step;
}
"""
	
class spline(object) :
	def __init__(self, ctrl_pts = None, dimension = 3, order = 3, step = 1):
		"""  - First two dimensions are x, y : position of the pen in the
		paper plane, in orthonormal coordinates
		  - The third dimension is p : the pressure exerted on the pen, from it,
		the thickness and the shape of the line can be deduced
		  - Other dimensions can be used to interpolate any parameter : 
		rotations, shape or fade coefficients.
		"""
		
		self.dimension = dimension
		self.order = order
		self.step = step
		self.calculated_curve = None
		
		if ctrl_pts is None :
			self.reset_spline()
		else :
			self.load_controls(ctrl_pts)
		
	def reset_spline(self) :
		self.n = 0
		self.k = self.order
		self.timeline = None
		self.controls = np.empty((0,self.dimension), dtype=np.float64)
		
	def load_controls(self, ctrl_pts) :
		self.reset_spline()
		for p in ctrl_pts :
			self.add_control(p)
		
	def add_control(self, ctrl_pt) :
		""" ctrl_pt = [x, y, p, ...]
		"""
		self.controls = np.vstack((self.controls, ctrl_pt))
		self.n += 1
		
	def div2(self, n, d) :
		if d == 0.0 :
			return 0
		else :
			return n / d
			
	def dist(self, v) :
		return np.sqrt(np.sum(np.power(v[0:2], 2)))
		
	def make_timeline(self) :
		if self.k > self.n :
			self.k = self.n
		self.timeline = np.array([0] * (self.k - 1) +
			range(self.n + 2 - self.k) +
			[self.n + 1 - self.k]*(self.k - 1), dtype=np.float64)
		
		return len(self.timeline)
		
	def walk(self, t) :
		print t
		_c = self.trace_curve(t)
		self.curve = np.vstack((self.curve, _c))
		
		_d = self.trace_derivate(t)
		self.derivate = np.vstack((self.derivate, _d))
		
		return t + self.step / max(self.dist(_d),1)
			
	def trace(self) :
		self.curve = np.empty((0,3), dtype=np.float64)
		self.derivate = np.empty((0,3), dtype=np.float64)
		
		self.t = []
		for u in range(self.make_timeline() - 1) :
			self.t.append(self.timeline[u])
			while self.t[-1] < self.timeline[u+1] :
				self.t.append(self.walk(self.t[-1]))
		self.t.append(self.walk(self.timeline[u+1]))
		
		print self.t
		#verbose : print >>sys.stderr, self.curve
		return self.curve, self.derivate
		
	def N(self, i, k, t) :
		ti = self.timeline
		
		#if not np.isnan(self.N_values[i,k-1]) :
		#	return self.N_values[i,k-1]
		#print "%d < %0.2f < %d" % (ti[i] , t , ti[i+1])
		if k == 1 :
			if ti[i] <= t < ti[i+1] :
				#print >>sys.stderr, "N(%d, %d, %0.2f) = 1" % (i, k, t)
				self.N_values[i,k-1] = 1
				return 1
			else :
				#print >>sys.stderr, "N(%d, %d, %0.2f) = 0" % (i, k, t)
				self.N_values[i,k-1] = 0
				return 0
		else :
			u =  self.N(i  , k-1, t) * self.div2((  t - ti[i]),(ti[i+k-1] - ti[i]))
			u += self.N(i+1, k-1, t) * self.div2((ti[i+k] - t),(ti[i+k] - ti[i+1]))
			#print >>sys.stderr, "N(%d, %d, %0.2f) = %f" % (i, k, t, u)
			self.N_values[i,k-1] = u
			return u
			
	def N_prime(self, i, k, t) :
		ti = self.timeline
		
		if k == 1 :
			self.N_primes[i,k-1] = 0
			return 0
		else :
			u =  self.N_prime(i  , k-1, t) * self.div2((  t - ti[i]), (ti[i+k-1] - ti[i]  ))
			u +=       self.N(i  , k-1, t) * self.div2((          1), (ti[i+k-1] - ti[i]  ))
			u += self.N_prime(i+1, k-1, t) * self.div2((ti[i+k] - t), (ti[i+k]   - ti[i+1]))
			u +=       self.N(i+1, k-1, t) * self.div2((         -1), (ti[i+k]   - ti[i+1]))
			self.N_primes[i,k-1] = u
			return u
			
	def calculate_curve(self, t) :
		#print self.n, self.k
		self.N_values = np.zeros((self.n + self.k - 1,self.k))
		curve = np.zeros(self.dimension)
		for i in range(self.n) :
			curve += self.N(i, self.k, t) * self.controls[i,:]
		return curve
		
	def trace_explicit_curve(self, i, k, t) :
		ti = self.timeline
		if k == 1 :
			if ti[i] <= t < ti[i+1] :
				self.N0[i,k-1] = 1
				print >>sys.stderr, "N(%d, %d, %0.2f) = 1" % (i, k, t)
				return 1
			else :
				self.N0[i,k-1] = 0
				print >>sys.stderr, "N(%d, %d, %0.2f) = 0" % (i, k, t)
				return 0
		else :
			u =  self.N0[i, k-2] * self.div2(( t - ti[i]),(ti[i+k-1] - ti[i]))
			u += self.N0[i+1, k-2] * self.div2((ti[i+k] - t),(ti[i+k] - ti[i+1]))
			print >>sys.stderr, "N(%d, %d, %0.2f) = %0.2f" % (i, k, t, u)
			self.N0[i,k-1] = u
			return u
			
	def trace_explicit_derivate(self, i, k, t):
		ti = self.timeline
		if k == 1 :
			return 0
		else :
			u =  self.N1[i  , k-2] * self.div2((  t - ti[i]), (ti[i+k-1] - ti[i]  ))
			u += self.N0[i  , k-2] * self.div2((          1), (ti[i+k-1] - ti[i]  ))
			u += self.N1[i+1, k-2] * self.div2((ti[i+k] - t), (ti[i+k]   - ti[i+1]))
			u += self.N0[i+1, k-2] * self.div2((         -1), (ti[i+k]   - ti[i+1]))
			self.N1[i,k-1] = u
			return u
		
	def trace_curve(self,t) :
		il = 0
		while t > self.timeline[il] :
			il += 1
			
		self.N0 = np.zeros((self.n+1,self.k), dtype=np.float64)
		self.N0[il-1,0] = 1
		ti = self.timeline
		for k in range(2, self.k+1) :
			for i in range(il - k, il):
				u =  self.N0[i, k-2] * self.div2(( t - ti[i]),(ti[i+k-1] - ti[i]))
				u += self.N0[i+1, k-2] * self.div2((ti[i+k] - t),(ti[i+k] - ti[i+1]))
				self.N0[i,k-1] = u
				
		self.calculated_curve = t
		self.il = il
		
		return np.dot(self.N0[:-1,-1], self.controls)
				
	def trace_derivate(self, t) :
		if self.calculated_curve != t :
			self.curve(t)
		il = self.il

		self.N1 = np.zeros((self.n+1,self.k), dtype=np.float64)
		ti = self.timeline
		for k in range(2,self.k+1) :
			for i in range(il - k, il):
				u =  self.N1[i  , k-2] * self.div2((  t - ti[i]), (ti[i+k-1] - ti[i]  ))
				u += self.N0[i  , k-2] * self.div2((          1), (ti[i+k-1] - ti[i]  ))
				u += self.N1[i+1, k-2] * self.div2((ti[i+k] - t), (ti[i+k]   - ti[i+1]))
				u += self.N0[i+1, k-2] * self.div2((         -1), (ti[i+k]   - ti[i+1]))
				self.N1[i,k-1] = u

		return np.dot(self.N1[:-1,-1], self.controls)
		
	def calculate_derivate(self, t) :
		self.N_primes = np.zeros((self.n + self.k - 1,self.k))
		derivate = np.zeros(self.dimension)
		for i in range(self.n) :
			derivate += self.N_prime(i, self.k, t) * self.controls[i,:]
		return derivate
		
		

