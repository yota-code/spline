#!/usr/bin/env python3

import math
import numpy as np
import numpy.ma as ma

import time

def gaussian(x, sigma=1.0, mu=0.0, norm=False) :
	""" return the computed gaussian for an np-array
	sigma - standard deviation
	mu - mean value
	norm - if norm is True, the highest value of the returned array is 1.0
	"""
	
	a = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
	b = -1.0 * (2.0 * (sigma ** 2))
	g = a * np.exp(((x - mu) ** 2) / b)
	
	return g / np.max(g) if norm else g
	
def add_uniform_border(array, size, value) :
	w, h = array.shape
	b = np.ones((w+2*size, h+2*size)) * value
	b[size:w+size, size:h+size] = array
	return b.astype(array.dtype)
	
def add_pulled_border(array, size) :
	w, h = array.shape
	b = np.ones((w+2*size, h+2*size), dtype=array.dtype)
	b[size:w+size, size:h+size] = array
	
class Base() :
	def __init__(self, radius=3) :
		self.radius = int(radius)
		self.plain = np.ones((2*self.radius+1, 2*self.radius+1), dtype=np.bool)
		self.full = add_border(self.plain, self.radius, 0)
		
	def get_patch(self, x, y) :
		if x == 2*self.radius+1 and y == 2*self.radius+1 :
			return self.plain
		else :
			return self.full[x-self.radius:x+self.radius+1,y-self.radius:y+self.radius+1]
			
	def get_coordinate(self, i, w) :
		if self.radius <= i < w-self.radius :
			result = 2*self.radius
		elif i < self.radius :
			result = i + self.radius
		elif w-self.radius <= i :
			result = i-w+3*self.radius+1
		return result

class Kernel() :
	def __init__(self, radius=3.33, norm=2.0) :
		self.radius = radius
		self.norm = norm
		
		self.k = int(self.radius)
		self.s = 2 * self.k + 1
		
		self.grid = np.rollaxis(np.dstack(np.meshgrid(range(-self.k, self.k+1), range(-self.k, self.k+1))), 2, 0)
		
		self.dist = np.power(np.sum(np.power(np.absolute(self.grid), self.norm), axis=0), 1 / self.norm)
		
		""" array with 1 in the circle 0 elsewhere """
		self.mask = np.where(self.dist <= self.radius, 1, 0).astype(np.float32)

		self.base = Base(self.k)
		
	def get_mask(self, i, j) :
		w, h = self.shape
		x, y = self.base.get_coordinate(i, w), self.base.get_coordinate(j, h)
		return self.base.get_patch(x, y) * self.mask
			
	def get_patch(self, i, j) :
		return self.frame[i:i+2*self.radius+1,j:j+2*self.radius+1]

	def run(self, image) :
		image = image.astype(np.float32)
		self.shape = image.shape
		
		self.frame = add_border(image, self.radius, 0.0)
		self.result = np.zeros_like(image, dtype=np.float32)
		
		self.pre_process()
		
		w, h = self.shape
		for i in range(w) :
			for j in range(h) :
				patch = self.get_patch(i, j)
				mask = self.get_mask(i, j)
				self.result[i,j] = self.process(patch, mask)
		
		self.post_process()
		
		return self.result
		
	def pre_process(self) :
		self.coef = np.ones_like(self.mask)
		
	def post_process(self) :
		pass
	
	def process(self, patch, mask) :
		w, h = patch.shape
		return np.sum(patch * mask) / np.sum(self.coef * mask)

if __name__ == '__main__' :
	import matplotlib.pyplot as plt
	import time, profile
	import sys
	
	np.random.seed(0)
	image = np.absolute(np.random.randn(32, 32))
	image = image / np.max(image)
		
	u = Kernel()
	
	#profile.run("u.run(image)")
	#
	#tick = time.time()
	#u.run(image)
	#tock = time.time()
	#	
	#print("time:", tock - tick)
	#
	#sys.exit(0)
	
	
	v = u.run(image)
	
	print(u.frame.dtype)
	print(v.dtype)
	
	plt.subplot(1,2,1)
	plt.imshow(image, cmap="Greys_r", interpolation="nearest", vmin=0, vmax=1.0)
	plt.subplot(1,2,2)
	plt.imshow(v, cmap="Greys_r", interpolation="nearest", vmin=0, vmax=1.0)
	plt.savefig("512_faster.png")

	#print(u.mask.shape)
	#print(u.base.shape)
	#print(u.base)
	#v = Base()
	#print(v.full)
	#print(v.get_patch(3,4))
	
		
