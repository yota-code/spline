#!/usr/bin/env python3

""" disk and tangent ploting of curve

une courbe, d'épaisseur variable, est approximée par le tracé sucessif de disques pleins (à
chaque point calculé) et de tangentes les joignants

"""

import math

class Vector2d() :
	def __init__(self, x, y) :
		self.x = x
		self.y = y
		
	def __repr__(self) :
		return "Vector2d({0}, {1})".format(self.x, self.y)

	def __add__(self, other) :
		return Vector2d(self.x + other.x, self.y + other.y)
		
	def __sub__(self, other) :
		return Vector2d(self.x - other.x, self.y - other.y)
		
	def inner_product(self, other) :
		return (self.x * other.y) - (self.y * other.x)
		
	def outer_product(self, other) :
		return (self.x * other.x) + (self.y * other.y)

	def rotation_sign(self, other) :
		return math.copysign(1, self.inner_product(other))
		
	def norm(self, n=2) :
		return math.pow(math.pow(self.x, n) + math.pow(self.y, n), 1/n)
		
	def angle(self, other) :
		return math.acos(self.outer_product(other) / (self.norm() * other.norm())) * self.rotation_sign(other)
		
class Circle2d() :
	def __init__(self, center, radius) :
		self.center = center
		self.radius = radius
		
	def polygon_join(self, other) :
		""" for two circles, return the joining polygon """
		v = other.center - self.center
		
		if max(self.radius, other.radius) > v.norm() :
			return None
		
		beta = math.asin((self.radius - other.radius) / v.norm())
		alpha = (math.pi / 2) - beta
		print(alpha)
		theta = Vector2d(1, 0).angle(v)
		
		return [[
				other.radius * math.cos(theta + alpha) + other.center.x,
				other.radius * math.sin(theta + alpha) + other.center.y
			], [
				self.radius * math.cos(theta + alpha) + self.center.x,
				self.radius * math.sin(theta + alpha) + self.center.y
			], [
				self.radius * math.cos(theta - alpha) + self.center.x,
				self.radius * math.sin(theta - alpha) + self.center.y
			], [
				other.radius * math.cos(theta - alpha) + other.center.x,
				other.radius * math.sin(theta - alpha) + other.center.y
		]]

p = Circle2d(Vector2d(1.0,1.0), 1.0).polygon_join(Circle2d(Vector2d(5.0,-2.0), 4.0))
#p = Circle2d(Vector2d(1.0,1.0), 1.0).polygon_join(Circle2d(Vector2d(5.0,-2.0), 0))
print(p)
