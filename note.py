import math
import numpy as np
import matplotlib.pyplot as mpl

"""
	bezier : bicubic bezier curve
	bspline : all order b-spline with starting and ending point
"""

math.sqrt2 = math.sqrt(2.0)

def prims(i):
	i = int(i)
	r = []
	for n in range(int(math.sqrt(i)) + 1):
		if 

def norm(v) :
	return np.sqrt(np.sum(np.square(v)))
	
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
		print len(c), b / len(c)
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
		print self.p
		mpl.plot(self.p[:,0], self.p[:,1])
		mpl.show()
		
"""
	p - control points
		p = [
			[x1 , y1 , z1],
			[x2 , y2 , z2],
			[x3 , y3 , z3] ...
		]
"""		
		
class bezier(curve) :
	def __init__(self, ctrl_pts) :
		self.p = np.atleast_2d(np.array(ctrl_pts, dtype=np.float))
		self.timeline = [0.0, 1.0]
		self.traced = False
		
	def position_p(self, t) :
		p = self.p
		return (((1-t)**3) * p[0]
			+ 3*(t)*((1-t)**2) * p[1]
			+ 3*(t**2)*(1-t) * p[2]
			+ (t**3) * p[3])

	def position_a(self, t) :
		p = self.p
		return ((((-t + 3)*t - 3)*t + 1) * p[0]
			+ (((3*t - 6)*t +3)*t) * p[1]
			+ ((-3*t + 3)*(t**2)) * p[2]
			+ (t**3) * p[3])

	def position_t(self, t):
		p = self.p
		return ((p[3]-3*p[2]+3*p[1]-p[0])*(t**3)
			+ (3*p[2]-6*p[1]+3*p[0])*(t**2)
			+ (3*p[1]-3*p[0])*(t)
			+ p[0])
		
	def position_f(self, t):
		p = self.p
		return ((((p[3]-3*p[2]+3*p[1]-p[0]) * t
			+ (3*p[2]-6*p[1]+3*p[0])) * t
			+ (3*p[1]-3*p[0])) * t
			+ p[0])
		
	position = position_p
	
	def velocity_p(self, t):
		p = self.p
		return ((3*(t**2)) * p[3]
			+ (-9*(t**2) + 6*t) * p[2]
			+ (9*(t**2) - 12*t + 3) * p[1]
			+ (-3*(t**2) + 6*t - 3) * p[0])
		
	def velocity_a(self, t):
		p = self.p
		return (
			(3*(t**2)) * p[3]
			+ (-9*(t**2) + 6*t) * p[2]
			+ (9*(t**2) - 12*t + 3) * p[1]
			+ (-3*((1-t)**2)) * p[0]
		)

	def velocity_t(self, t):
		p = self.p
		return (3*(p[3]-3*p[2]+3*p[1]-p[0])*(t**2)
			+ 2*(3*p[2]-6*p[1]+3*p[0])*(t)
			+ (3*p[1]-3*p[0]))
			
	def velocity_f(self, t):
		p = self.p
		return ((3*(p[3]-3*p[2]+3*p[1]-p[0]) * t
			+ 2*(3*p[2]-6*p[1]+3*p[0])) * t
			+ (3*p[1]-3*p[0]))
		
	velocity = velocity_a
		
	def reframe(self, a, b):
		pass
		p0, p1, p2, p3 = self.p[0,:], self.p[1,:], self.p[2,:], self.p[3,:]
		q = np.zeros_like(self.p)
		#q[0,:] = ((1-a)**3)*p0+3*a*((1-a)**2)*p1+3*(a**2)*(1-a)*p2+(a**3)*p3
		#q[1,:] = (2*(1-a)/(b-a))*(p1 - p0) + q[0,:]
		#q[2,:] = p2
		#q[3,:] = ((1-b)**3)*p0+3*b*((1-b)**2)*p1+3*(b**2)*(1-b)*p2+(b**3)*p3
		return bezier_4p(q)
		
class bspline(curve) :
	def __init__(self, ctrl_pts, order = 3) :
		self.p = np.atleast_2d(np.array(ctrl_pts, dtype=np.float))
		self.traced = False
		self.n = self.p.shape[0]
		self.k = ( order if order <= self.n else self.n)
		#self.N1 = np.zeros((self.n+1,self.k), dtype=np.float)
		#self.N0 = np.zeros((self.n+1,self.k), dtype=np.float)
		self.timeline = np.array(
			[0] * (self.k - 1) +
			range(self.n + 2 - self.k) +
			[self.n + 1 - self.k] * (self.k - 1), dtype=np.float)

	def position(self, t):
		il = self.k
		while t > self.timeline[il] :
			il += 1
		self.N0 = np.zeros((self.n+1, self.k), dtype=np.float64)
		self.N0[il-1, 0] = 1
		ti = self.timeline
		for j in range(2, self.k+1) :
			for i in range(il - j, il):
				self.N0[i ,j-1] = (
					self.N0[i  , j-2] * divzero((t       - ti[i]), (ti[i+j-1] - ti[i]  )) +
					self.N0[i+1, j-2] * divzero((ti[i+j] - t    ), (ti[i+j]   - ti[i+1]))
				)
		return np.dot(self.N0[:-1,-1], self.p)

	def velocity(self, t) :
		il = self.k
		while t > self.timeline[il] :
			il += 1
		self.N1 = np.zeros((self.n+1, self.k), dtype=np.float64)
		ti = self.timeline
		for j in range(2,self.k+1) :
			for i in range(il - j, il):
				self.N1[i,j-1] = (
					self.N1[i  , j-2] * divzero((  t - ti[i]), (ti[i+j-1] - ti[i]  )) +
					self.N0[i  , j-2] * divzero((          1), (ti[i+j-1] - ti[i]  )) +
					self.N1[i+1, j-2] * divzero((ti[i+j] - t), (ti[i+j]   - ti[i+1])) +
					self.N0[i+1, j-2] * divzero((         -1), (ti[i+j]   - ti[i+1]))
				)
		return np.dot(self.N1[:-1,-1], self.p)

class polygon(object) :
	def __init__(self, p = None, closed = True):
		if p is not None :
			self.p = p
		else :
			self.p = []
		self.closed = closed
		
#def norm(v_1):
#	return math.sqrt((v_1[0])**2 + (v_1[1])**2)
	
def vector(p_1, p_2):
	return (p_2[0] - p_1[0], p_2[1] - p_1[1])

def outer_product(v_1, v_2):
	return v_1[0] * v_2[0] + v_1[1] * v_2[1]

def rotation_sign(v_1, v_2):
	v = v_1[0] * v_2[1] - v_1[1] * v_2[0]
	if v < 0.0 :
		return -1.0
	elif v == 0.0 :
		return 0.0
	elif v > 0.0 :
		return 1.0

def angle(v_1, v_2):
	return acos(outer_product(v_1, v_2) / (norm(v_1) * norm(v_2))) * rotation_sign(v_1, v_2)

def two_circle_tangent(c_1, c_2, side = 1.0):
	v_1 = vector(c_1.center, c_2.center)
	angle_beta = asin((c_1.radius - c_2.radius) / norm(v_1))
	print "angle_beta =", angle_beta
	angle_alpha = (pi / 2) - angle_beta
	print "angle_alpha =", angle_alpha
	angle_theta = angle((1,0), v_1)
	print "angle_theta =", angle_theta
	p = []
	p.append((c_2.radius * cos(angle_theta + angle_alpha) + c_2.center[0],
		c_2.radius * sin(angle_theta + angle_alpha) + c_2.center[1]))
	p.append((c_1.radius * cos(angle_theta + angle_alpha) + c_1.center[0],
		c_1.radius * sin(angle_theta + angle_alpha) + c_1.center[1]))
	p.append((c_1.radius * cos(angle_theta - angle_alpha) + c_1.center[0],
		c_1.radius * sin(angle_theta - angle_alpha) + c_1.center[1]))
	p.append((c_2.radius * cos(angle_theta - angle_alpha) + c_2.center[0],
		c_2.radius * sin(angle_theta - angle_alpha) + c_2.center[1]))
	for i in p :
		print "(%+0.5f ; %+0.5f)" % i
	return p
	


#b = bezier([[0,1],[2,1],[1,2],[0,2]])
s = bspline([[0,0.5],[2,1],[1,2],[0,2],[1,3],[3,2],[0,1]])

#b.mpl_plot()
s.mpl_plot()
