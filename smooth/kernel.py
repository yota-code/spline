#!/usr/bin/env python3

import math
import numpy as np

def gaussian(x, sigma=1.0, mu=0.0, norm=True) :
	""" return the computed gaussian for a scalar or an array
	"""
	
	a = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
	b = -1.0 * (2.0 * (sigma ** 2))
	g = a * np.exp(((x - mu) ** 2) / b)
	return g / np.max(g) if norm else g


class Kernel_2d() :
	def __init__(self, radius=3.0, norm=2.0) :
		self.radius = radius
		self.norm = norm
		
		self.k = int(self.radius)
		self.s = 2 * self.k + 1
		self.g = np.rollaxis(np.dstack(np.meshgrid(range(-self.k, self.k+1), range(-self.k, self.k+1))), 2, 0)
		
		self.dist = np.power(np.sum(np.power(np.absolute(self.g), self.norm), axis=0), 1 / self.norm)
		
		""" array with 1 in the circle 0 elsewhere """
		self.mask = np.where(self.dist <= self.radius, 1, 0)
			
		""" list of all coordinates contained in the circle """
		self.coord = np.rollaxis(self.g[:, self.dist <= self.radius], 1, 0)
		
		self.ray = np.power(np.sum(np.power(np.absolute(self.coord), self.norm), axis=1), 1 / self.norm)
	
def _grid(radius, dim) :
	radius = int(math.ceil(radius))
	if dim == 1 :
		return np.array(range(2 * radius + 1)) - radius
	if dim == 2 :
		return np.meshgrid(range(-radius, radius+1), range(-radius, radius+1))
	
def manhattan_grid(radius, dim) :
	if dim == 1 :
		x = _grid(radius, dim)
		return x.astype(np.double)
	elif dim == 2 :
		x, y = _grid(radius, dim)
		return (np.abs(x) + np.abs(y)).astype(np.double)
		
def euclidean_grid(radius, dim) :
	if dim == 1 :
		x = _grid(radius, dim)
		return x.astype(np.double)
	elif dim == 2 :
		x, y = _grid(radius, dim)
		return np.sqrt((x**2 + y**2).astype(np.double))
		
if __name__ == '__main__' :
	#print(manhattan_grid(3, dim=1))
	#print(manhattan_grid(3, dim=2))
	#print(euclidean_grid(3, dim=1))
	#print(euclidean_grid(3, dim=2))	
	#print(gaussian(euclidean_grid(3, dim=2)))
	u = Kernel_2d(4.3)
	print(u.dist)
	#print(u.r)
	#print(u.s)
	print(u.mask)
	print(u.coord)
	print(u.ray)
	#print(u.mask())
	#print(u.g.shape)
	
