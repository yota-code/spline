import math
import numpy as np

def solve_root_2nd(a, b, c) :
	"""
	return all real solutions of a*x^2 + b*x + c = 0
	"""
	delta = (b**2) - (4 * a * c)
	if delta == 0 :
		return tuple((-1 * b) / (2 * a))
	if delta < 0 :
		return tuple()
	if delta > 0 :
		return (
			((-1 * b) - math.sqrt(delta)) / (2 * a),
			((-1 * b) + math.sqrt(delta)) / (2 * a)
		)

class Spline() :
	def __init__(self) :
		self._position = dict()
		self._velocity = dict()
		self._timeline = list()
		
		self.curs = 0.0
		self.window = [0, 1]
		
	def trace(self, res=32.0) :
		res = float(res)
		
	def next(self) :
		pass
	
	def prev(self) :
		pass
	
	def position(self, t) :
		pass
	
	def velocity(self, t) :
		pass
	
	
class Bezier(Spline) :
	def __init__(self) :
		
		self.timeline = [0.0, 1.0]
		self.traced = False
		
	def set_control(self, control_lst) :
		c = np.atleast_2d(np.array(control_lst, dtype=np.float))
		
		p0 = np.zeros_like(c)
		p1 = np.zeros_like(c[:-1,:])
		
		# position
		p0[0] = c[3]-3*c[2]+3*c[1]-c[0]
		p0[1] = 3*c[2]-6*c[1]+3*c[0]
		p0[2] = 3*c[1]-3*c[0]
		p0[3] = c[0]
		
		# velocity
		p1[0] = 3*p0[0]
		p1[1] = 2*p0[1]
		p1[2] = p0[2]
		
		self.control_lst = c
		self.p0 = p0
		self.p1 = p1
		
	def position(self, t) :
		p0 = self.p0
		return (((((((p0[0])*t) + (p0[1]))*t) + (p0[2]))*t) + p0[3])		
		
	def velocity(self, t) :
		p1 = self.p1
		return ((((((p1[0]))*t) + (p1[1]))*t) + p1[2])
		
	def slope(self, t) :
		x, y = self.velocity(t)
		return math.atan2(y, x)
		
	def find_tangent(self, dx, dy) :
		p1_y = self.p1[:,1]
		p1_x = self.p1[:,0]
		
		m = (p1_y * dx - p1_x * dy)
				
		return solve_root_2nd(* m)
		
		
"""
pour trouver la tangente definie par son dy /dx

poser b_y(t) / b_x(t) = dy / dx 
resoudre b_y(t) * dx = b_x(t) * dy
soit b_y(t) * dx - b_x(t) * dy = 0
"""
		
