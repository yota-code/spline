#!/usr/bin/env python3

import math
import numpy as np

"""
class of bezier curve
ctrl_pts if a list of four points
"""

def norm(v, n=2) :
	return np.power(np.sum(np.power(v, n)), 1/n)
	
def divzero(n, d) :
	if d == 0.0 :
		return 0.0
	else :
		return n / d

class poly2nom() :
	def __init__(self, a, b, c) :
		""" a*x**2 + b*x + c = 0 """
		self.a, self.b, self.c = a, b, c
		
	@property
	def delta(self) :
		return self.b**2 - (4 * self.a * self.c)
		
	def __str__(self) :
		return "{0}*x**2 + {1}*x + {2} = 0".format(self.a, self.b, self.c)
		
	def zeros(self) :
		a, b, c, d = self.a, self.b, self.c, self.delta
		print(a, b, c, d)
		if d > 0.0 :
			return [(-b + math.sqrt(d)) / (2*a), (-b - math.sqrt(d)) / (2*a)]
		elif d == 0.0 :
			return [(-self.b) / (2*a),]
		else :
			return list()

class bezier() :
	""" cubic bezier (with 4 control points) """
	def __init__(self, p) :
		if len(p) != 4 :
			raise ValueError("Only 4 control points supported")
		self.p = np.array(p, dtype=np.double)
		
	@property
	def position_coef(self) :
		p = self.p
		return np.array([p[0], (3*p[1]-3*p[0]), (3*p[2]-6*p[1]+3*p[0]), (p[3]-3*p[2]+3*p[1]-p[0])])
		
	@property
	def velocity_coef(self) :
		p = self.p
		return np.array([(3*p[1]-3*p[0]), 2*(3*p[2]-6*p[1]+3*p[0]), 3*(p[3]-3*p[2]+3*p[1]-p[0])])
		
	def _position_p(self, t) :
		p = self.p
		return (((1-t)**3) * p[0]
			+ 3*(t)*((1-t)**2) * p[1]
			+ 3*(t**2)*(1-t) * p[2]
			+ (t**3) * p[3])

	def _position_a(self, t) :
		p = self.p
		return ((((-t + 3)*t - 3)*t + 1) * p[0]
			+ (((3*t - 6)*t +3)*t) * p[1]
			+ ((-3*t + 3)*(t**2)) * p[2]
			+ (t**3) * p[3])

	def _position_t(self, t):
		p = self.p
		return ((p[3]-3*p[2]+3*p[1]-p[0])*(t**3)
			+ (3*p[2]-6*p[1]+3*p[0])*(t**2)
			+ (3*p[1]-3*p[0])*(t)
			+ p[0])
		
	def _position_f(self, t):
		p = self.p
		return ((((p[3]-3*p[2]+3*p[1]-p[0]) * t
			+ (3*p[2]-6*p[1]+3*p[0])) * t
			+ (3*p[1]-3*p[0])) * t
			+ p[0])

	position = _position_t
			
	def _velocity_p(self, t):
		p = self.p
		return ((3*(t**2)) * p[3]
			+ (-9*(t**2) + 6*t) * p[2]
			+ (9*(t**2) - 12*t + 3) * p[1]
			+ (-3*(t**2) + 6*t - 3) * p[0])
		
	def _velocity_a(self, t):
		p = self.p
		return (
			(3*(t**2)) * p[3]
			+ (-9*(t**2) + 6*t) * p[2]
			+ (9*(t**2) - 12*t + 3) * p[1]
			+ (-3*((1-t)**2)) * p[0]
		)

	def _velocity_t(self, t):
		p = self.p
		return (3*(p[3]-3*p[2]+3*p[1]-p[0])*(t**2)
			+ 2*(3*p[2]-6*p[1]+3*p[0])*(t)
			+ (3*p[1]-3*p[0]))
			
	def _velocity_f(self, t):
		p = self.p
		return ((3*(p[3]-3*p[2]+3*p[1]-p[0]) * t**2
			+ 2*(3*p[2]-6*p[1]+3*p[0])) * t
			+ (3*p[1]-3*p[0]))

	velocity = _velocity_a
			
	def trace_even_space(self, resolution=100) :
		p0, p1, p2, p3 = self.position_coef
		v0, v1, v2 = self.velocity_coef
		c = list()
		t = 0.0
		while t < 1.0 :
			t1 = t
			t2 = t1 * t
			t3 = t2 * t
			p = p0 + p1 * t1 + p2 * t2 + t3 * t3
			c.append(p)
			v = v0 + v1 * t1 + v2 * t2
			t += norm(v) / resolution
		p = p0 + p1 + p2 + p3
		c.append(p)
		return np.array(c)

	def trace_even_time(self, resolution=100) :
		p0, p1, p2, p3 = self.position_coef
		v0, v1, v2 = self.velocity_coef
		c = list()
		resolution -= 1
		for i in range(resolution) :
			t = 1.0 / (resolution)
			t1 = t
			t2 = t1 * t
			t3 = t2 * t
			p = p0 + p1 * t1 + p2 * t2 + t3 * t3
			c.append(p)
		p = p0 + p1 + p2 + p3
		c.append(p)
		return np.array(c)

	def reframe(self, a, b):
		""" return the coefficients which make a part of a bezier curve
		where 0 ≤ a < b ≤ 1

		> tested: ok
		"""
		b0 = self.position(a)
		b1 = self.position((2*a+b)/3)
		b2 = self.position((a+2*b)/3)
		b3 = self.position(b)
		q0 = b0
		q1 = (-15*b0 + 54*b1 - 27*b2 + 6*b3)/18
		q2 = (6*b0 - 27*b1 + 54*b2 - 15*b3)/18
		q3 = b3
		return bezier([q0, q1, q2, q3])
		
class bezier_2d(bezier) :
	def angle(self, t) :
		return math.atan2(* self.velocity(t))
		
	def rotate(self, angle) :
		m = np.matrix([[math.cos(angle), math.sin(angle)], [-1.0*math.sin(angle), math.cos(angle)]])
		return bezier_2d(np.array([np.squeeze(np.asarray(p*m)) for p in self.p]))
		
	def get_tangent(self, angle) :
		""" pour calculer les points où une droite de pente alpha tangente la courbe,
		on retourne la courbe d'un angle -alpha de façon à n'avoir plus qu'un paramètre à vérifier
		"""
		r = self.rotate(- (angle % (2.0*math.pi)))
		c = r.velocity_coef
		p = poly2nom(* c[::-1,1])
		return p.zeros()
		
if __name__ == '__main__' :
	import time

	import matplotlib.pyplot as plt	
	
	u = bezier_2d([[0.0, 0.0], [2.0, 0.0], [-2.0, 2.0], [0.0, 2.0]])

	t_zero = time.time()
	k = u.trace_even_space(1000000)
	t_one = time.time()
	print(t_one - t_zero, len(k))

	t_zero = time.time()
	k = u.trace_even_time(len(k))
	t_one = time.time()
	print(t_one - t_zero, len(k))
	
	a, b = u.get_tangent(math.pi/4)
	
	v = u.reframe(a, b)
	j = v.trace_even_space()

	u.trace_even_space()
		
	plt.plot(k[:,0], k[:,1])
	plt.plot(j[:,0], j[:,1], color='red')
	plt.show()
	