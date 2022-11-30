import sys
import numpy as np
	
class spline(object) :
	def __init__(self, ctrl_pts = None, order = 3, step = 1):
		"""
		  - First two dimensions are x, y : position of the pen in the
		paper plane, in orthonormal coordinates
		  - The third dimension is p : the pressure excerted on the pen, from
		it, the thickness and the shape of the line is deduced.
		  - Other dimensions can be used to interpolate any parameter : 
		rotations, shape or fade coefficients.
		"""
		self.order = order
		self.step = step
		
		self.calculated_curve = None
		
		self.load_controls(ctrl_pts)
		
	def reset_spline(self) :
		self.calculated_curve = None
		self.dimension = 2
		self.n = 0
		self.k = self.order
		self.timeline = None
		self.controls = np.empty((0, self.dimension), dtype=np.float64)
		
	def load_controls(self, ctrl_pts) :
		self.reset_spline()
		
		for p in ctrl_pts :
			self.add_control(p)
		
	def add_control(self, ctrl_pt) :
		""" ctrl_pt = [x, y, p, ..., w] """
		self.controls = np.vstack((self.controls, ctrl_pt))
		self.n += 1
		
	def div2(self, n, d) :
		if d == 0.0 :
			return 0
		else :
			return n / d
			
	def dist(self, v) :
		return np.sqrt(np.sum(np.power(v, 2)))
			
	def trace(self) :
		self.curve = np.empty((0,3), dtype=np.float64)
		self.derivate = np.empty((0,3), dtype=np.float64)
		if self.k > self.n :
			self.k = self.n
		self.timeline = np.array(
			[0] * (self.k - 1) +
			range(self.n + 2 - self.k) +
			[self.n + 1 - self.k] * (self.k - 1), dtype=np.float64)
		self.t = []
		for u in range(len(self.timeline) - 1) :
			self.t.append(self.timeline[u])
			while self.t[-1] < self.timeline[u+1] :
				self.t.append(self.walk(self.t[-1]))
		self.t.append(self.walk(self.timeline[u+1]))
		
		return self.curve, self.derivate
		
	def walk(self, t) :
		_c = self.trace_curve(t)
		self.curve = np.vstack((self.curve, _c))
		
		_d = self.trace_derivate(t)
		self.derivate = np.vstack((self.derivate, _d))
		
		return t + self.step / max(self.dist(_d),1)
		
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
		
