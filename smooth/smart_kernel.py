#!/usr/bin/env python3

" tentative d'accélération, en revenant à une image empilée """ 

import math
import numpy as np
import numpy.ma as ma

def gaussian(x, sigma=1.0, mu=0.0, norm=True) :
	""" return the computed gaussian for a scalar or an array
	"""
	
	a = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
	b = -1.0 * (2.0 * (sigma ** 2))
	g = a * np.exp(((x - mu) ** 2) / b)
	
	return g / np.max(g) if norm else g
	
def add_border(image, size, value) :
	w, h = array.shape
	b = np.ones((w+2*size, h+2*size)) * value
	b[size:w+size, size:h+size] = array
	return b.astype(array.dtype)
	
class Base() :
	def __init__(self, radius=3) :
		self.radius = int(radius)
		self.plain = np.zeros((2*self.radius+1, 2*self.radius+1), dtype=np.bool)
		self.full = add_border(self.plain, self.radius, 1)
		
	def get_patch(self, x, y) :
		if x == 2*self.radius+1 and y == 2*self.radius+1 :
			return self.plain
		else :
			return self.full[x-self.radius:x+self.radius+1,y-self.radius:y+self.radius+1]
			
	def get_coordinate(self, i, w) :
		#print("Base.get_coordinate({0}, {1})".format(i,w))
		#print(self.radius, w-self.radius)
		if self.radius <= i < w-self.radius :
			#print("IN")
			result = 2*self.radius
		elif i < self.radius :
			#print("LEFT")
			result = i + self.radius
		elif w-self.radius <= i :
			#print("RIGHT")
			result = i-w+3*self.radius+1
		#print("\t->", result)
		return result


def coordinate(radius) :
	""" retourne une longue liste de toutes les décalages possibles """
	s = list()
	for i in range(radius, radius+1) :
		for j in range(radius, radius+1) :
			s.append([i, j])
	return np.array(s)
	
def stack_image(image, radius=3) :
	for i,j in coordinate(radius) :
		
	

class Kernel() :
	def __init__(self, radius=3.33, norm=2.0) :
		self.radius = radius
		self.norm = norm
		
		self.k = int(self.radius)
		self.s = 2 * self.k + 1
		
		self.grid = np.rollaxis(np.dstack(np.meshgrid(range(-self.k, self.k+1), range(-self.k, self.k+1))), 2, 0)
		
		self.dist = np.power(np.sum(np.power(np.absolute(self.grid), self.norm), axis=0), 1 / self.norm)
		
		""" array with 1 in the circle 0 elsewhere """
		self.mask = np.where(self.dist <= self.radius, False, True)

		self.base = Base(self.k)
		
	def get_base(self, i, j) :
		w, h = self.im_shape
		x, y = self.base.get_coordinate(i, w), self.base.get_coordinate(j, h)
		return self.base.get_patch(x, y)
			
	def get_patch(self, i, j) :
		return self.image[i:i+2*self.radius+1,j:j+2*self.radius+1]

	def run(self, image) :
		self.im_shape = image.shape
		self.image = add_border(image, self.radius, 0.0)
		self.result = np.zeros_like(image)
		
		self.pre_process()
		
		w, h = self.im_shape
		for i in range(w) :
			for j in range(h) :
				patch = self.get_patch(i, j)
				base = self.get_base(i, j)
				self.result[i,j] = self.process(ma.array(patch, mask=base|self.mask))
		
		self.post_process()
		
		return self.result
		
	def pre_process(self) :
		self.coef = np.ones_like(self.mask)
		
	def post_process(self) :
		pass
	
	def process(self, array) :
		w, h = array.shape
		return ma.sum(array) / np.sum(ma.array(self.coef, mask=ma.getmask(array)))

if __name__ == '__main__' :
	import matplotlib.pyplot as plt
	import time, profile
	import sys
	
	np.random.seed(0)
	image = np.absolute(np.random.randn(13, 19))
	image = image / np.max(image)
	
	u = stack_image(image)
	
	print(image.shape)
	print(u.shape)
	
	
	#u = Kernel()
	#
	#profile.run("u.run(image)")
	#
	#tick = time.time()
	#u.run(image)
	#tock = time.time()
	#	
	#print("time:", tock - tick)
	#
	#sys.exit(0)
	
	
	#v = u.run(image)
	#
	#plt.subplot(1,2,1)
	#plt.imshow(image, cmap="Greys_r", interpolation="nearest", vmin=0, vmax=1.0)
	#plt.subplot(1,2,2)
	#plt.imshow(v, cmap="Greys_r", interpolation="nearest", vmin=0, vmax=1.0)
	#plt.savefig("512.png")

	#print(u.mask.shape)
	#print(u.base.shape)
	#print(u.base)
	#v = Base()
	#print(v.full)
	#print(v.get_patch(3,4))
	
		
