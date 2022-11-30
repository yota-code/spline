#!/usr/bin/env python3

import math
import numpy as np

"""
 2d geometry
"""

class Vector() :
	""" 2d vector, no origin """
	def __init__(self, x, y) :
		self.p = np.array([x,y], dtype=np.float)
		
	def norm(self) :
		return math.sqrt(((self.p)**2).sum())
		
	def normalize(self) :
		n = self.norm()
		if n != 0 :
			self.p = self.p / n

class Dot(Vector) :
	""" like a 2d vector, but it's a dot """
	def distance(self, other) :
		if isinstance(other, Dot) :
			return math.sqrt(((self.p - other.p)**2).sum())
		if isinstance(other, Line) :
			
			
class Line() :
	""" can be defined as
	canonical form a*x + b*y = 0
	parametric form x(t) = a*t + b, y(t) = c*t +d
	
	
	
	"""
	def __init__(self, a, b, c) :
		self.p = p
		self.m = m
		
		self.cartesian = (a, b, c) 
		
	def set_parametric(self, ax, bx, ay, by) :
		self.parametric = [[ax, bx], [ay, by]]
		self.cartesian = 
	def set_
	def solve_cartesian(x, y) :
		
			
a = Dot(0,0)
b = Dot(3,4)

print a.distance(b)

#class Line() :
#	def __init__(self, anchor, direction) :
#		self.anchor = anchor
#		self.direction = direction
#		
#	def intersection(self, other) :
#		if 
#		
#
#class Segment() :
#	def __init__(self, x0, y0, x1, y1) :
#		self.x0 = x0
#		self.x1 = x1
#		self.y0 = y0
#		self.y1 = y1
#		
#	def intersection(self, line) :
#		
#
#segment_intersection(
#
#class Polyline() :
#	def __init__(self) :
#		pass
#	
#	def set_control(self, control_lst) :
#		c = np.atleast_2d(np.array(control_lst, dtype=np.float))
#		
