#!/usr/bin/env python3

import math
import numpy as np

DISABLED CODE !!! cf. package/spline/bezier.py

"""
class of bezier curve
ctrl_pts if a list of four points
"""

from curve import norm

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
	""" cubic bezier with 4 control points """
	def __init__(self, p) :
		if len(p) != 4 :
			raise ValueError("Only 4 control points supported")
		self.p = np.array(p, dtype=np.double)
		
	def position_t_coef(self) :
		p = self.p
		return np.array([(p[3]-3*p[2]+3*p[1]-p[0]), (3*p[2]-6*p[1]+3*p[0]), (3*p[1]-3*p[0]), p[0]])
		
	def velocity_t_coef(self) :
		p = self.p
		return np.array([3*(p[3]-3*p[2]+3*p[1]-p[0]), 2*(3*p[2]-6*p[1]+3*p[0]), (3*p[1]-3*p[0])])
		
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
		return ((3*(p[3]-3*p[2]+3*p[1]-p[0]) * t**2
			+ 2*(3*p[2]-6*p[1]+3*p[0])) * t
			+ (3*p[1]-3*p[0]))
		
	velocity = velocity_a
	
	def trace(self, resolution=100) :
		t = 0.0
		c = list()
		while t < 1.0 :
			c.append(self.position(t))
			t += norm(self.velocity(t)) / resolution
		c.append(self.position(1.0))
		return np.array(c, dtype=np.double)
		
	def reframe(self, a, b):
		# tested ok
		b0 = self.position(a)
		b1 = self.position((2*a+b)/3)
		b2 = self.position((a+2*b)/3)
		b3 = self.position(b)
		q0 = b0
		q1 = (-15*b0 + 54*b1 - 27*b2 + 6*b3)/18
		q2 = (6*b0 - 27*b1 + 54*b2 - 15*b3)/18
		q3 = b3
		return bezier([q0, q1, q2, q3])
		
class bezier2d(bezier) :
	def angle(self, t) :
		return math.atan2(* self.velocity(t))
		
	def rotate(self, angle) :
		m = np.matrix([[math.cos(angle), math.sin(angle)], [-1.0*math.sin(angle), math.cos(angle)]])
		return bezier2d(np.array([np.squeeze(np.asarray(p*m)) for p in self.p]))
		
	def get_tangent(self, angle) :
		""" pour calculer les points où une droite de pente alpha tangente la courbe,
		on retourne la courbe d'un angle -alpha de façon à n'avoir plus qu'un paramètre à vérifier
		"""
		r = self.rotate(- (angle % (2.0*math.pi)))
		c = r.velocity_t_coef()
		p = poly2nom(* c[:,1])
		return p.zeros()
		
if __name__ == '__main__' :
	import matplotlib.pyplot as plt
	import profile
	
	""" profiling, for a resolution of 10000
	position_p() 2.942s	(velocity_a() 3.163s)
	position_a() 3.139s	(velocity_a() 3.195s)
	position_t() 4.940s	(velocity_a() 3.228s)
	position_f() 4.550s	(velocity_a() 3.226s)
	"""
	
	u = bezier2d([[0.0, 0.0], [2.0, 0.0], [-2.0, 2.0], [0.0, 2.0]])
	k = u.trace()
	
	a, b = u.get_tangent(math.pi/4)
	
	v = u.reframe(a, b)
	j = v.trace()
		
	plt.plot(k[:,0], k[:,1])
	plt.plot(j[:,0], j[:,1], color='red')
	plt.show()
	

	
