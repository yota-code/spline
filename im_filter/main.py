#!/usr/bin/env python3

from PIL import Image

import math

import numpy as np
import numpy.ma as ma

#def disk_mask(radius, norm) :
#	r = (width-1)//2
#	a, b = np.power(np.abs(np.mgrid[-r:r+1,-r:r+1]), norm)
#	d = (np.power(a + b, 1.0 / norm) / radius)
#	return np.where(d < 1.0, 0, 1)
#	
#class Patch(ma.MaskedArray) :
#	def __init__(self, radius, norm=2.0) :
#		width = (2 * int(math.ceil(radius))) + 1
#		
#		m = mask(width, radius, norm)
#		v = np.zeros((width, width), dtype=np.double)
#			
#		ma.MaskedArray.__init__(self, v, m)

def dgrid(radius, norm) :
	r = int(radius)
	return np.power(np.power(np.absolute(np.mgrid[-r:r+1,-r:r+1]), norm).sum(0), 1.0 / norm)
	
class MinMax :
	def __init__(self, radius, norm=2.0) :
		self.radius = radius
		d = dgrid(radius, norm)
		r = int(radius)
		v = np.ones_like(d, dtype=np.double)
		m = np.where(d <= radius, 0, 1)
		m[r,r] = 1
		self.kernel = ma.array(v, mask=m)
		
	def apply(self, source) :
		print(self.kernel)
		result = MonoChrome(source.layer)
		r = int(self.radius)
		for x, y, p in source.enumerate(self.radius) :
			q = p * self.kernel
			mini, maxi = q.min(), q.max()
			result.layer[x,y] = np.clip(p[r, r], mini, maxi)
		return result

class SimpleKernel :
	def __init__(self, kernel) :
		self.load(kernel)
		
	def load(self, kernel) :
		if not isinstance(kernel, ma.MaskedArray) :
			raise ValueError("kernel must be a ma.MaskedArray")
		self.kernel = kernel
		
		w, h = self.kernel.shape
		
		assert(w == h)
		assert(w%2 == 1)
		
		self.w = w
		self.r = (self.w-1)//2
	
	def apply(self, src) :
		dst = MonoChrome(src.layer)
		s = self.kernel.sum()
		for x, y, p in src.enumerate(self.r) :
			dst.layer[x,y] = (self.kernel * p).sum() / s
		return dst
		
class DiskKernel(SimpleKernel) :
	def __init__(self, radius, norm=2.0) :
		self.radius = radius
		d = dgrid(radius, norm)
		v = np.ones_like(d, dtype=np.double)
		m = np.where(d <= radius, 0, 1)
		self.load(ma.array(v, mask=m))
		
class GaussianKernel(SimpleKernel) :
	def __init__(self, radius, standard_deviation, norm=2.0) :
		self.radius = radius
		d = dgrid(radius, norm)
		v = 1.0 / (standard_deviation * math.sqrt(2 * math.pi)) * np.exp(-1.0 * (d / standard_deviation)**2 / 2.0)
		m = np.where(d <= radius, 0, 1)
		self.load(ma.array(v / v.max(), mask=m))
		
class SincKernel(SimpleKernel) :
	def __init__(self, radius, zero=math.pi, norm=2.0) :
		""" zero: zero crossing distance """
		self.radius = radius
		d = dgrid(radius, norm)
		v = np.sinc(d * zero / math.pi)
		m = np.where(d <= radius, 0, 1)
		self.load(ma.array(v / v.max(), mask=m))
		
class DistanceKernel(SimpleKernel) :
	def __init__(self, radius, norm) :
		self.radius = radius
		d = dgrid(radius, norm)
		v = (1 + d.max() - d)
		m = np.where(d <= radius, 0, 1)
		self.load(ma.array(v / v.max(), mask=m))
		
class MonoChrome :
	def load(self, layer) :
		if layer.dtype == np.uint8 :
			layer = layer / 255.0
		self.layer = np.array(layer, copy=True, dtype=np.double)
		return self
		
	def enumerate(self, radius) :
		""" radius of the patch """
		
		r = int(radius)
		w = (2 * r) + 1
		
		frame_size = tuple(s+w-1 for s in self.layer.shape)
		
		image_value = np.zeros(frame_size, dtype=np.double)
		image_value[r:-r,r:-r] = self.layer
		
		image_mask = np.ones(frame_size, dtype=np.bool)
		image_mask[r:-r,r:-r] = np.zeros_like(self.layer)
		
		image = ma.array(image_value, mask=image_mask)
		
		for x, y in np.ndindex(* self.layer.shape) :
			yield x, y, image[x:x+w,y:y+w]
		
if __name__ == '__main__' :

	import profile

	img = Image.open("source_small.png")
	r, g, b = (np.asarray(i) / 255.0  for i in img.split())

	src = MonoChrome(0.25 * r + 0.5 *g + 0.25 * b)
	#k = GreyDistanceKernel(5.0, 2.0)
	#k = SincKernel(3.0, math.sqrt(5.0), 2.0)
	k = GaussianKernel(3.0, 1.2, 0.8)
	#k = DiskKernel(3.5, 0.1)
	#k = MinMax(3.5, 2.0)
	dst = k.apply(src)
	
	def display_test(a) :
		mini = a.min()
		maxi = a.max()
		a = (a - mini) / (maxi - mini)
		a = np.uint8(np.clip(a, 0.0, 1.0) * 255.0)
		Image.fromarray(a).show()
		
	display_test(src.layer)
	display_test(dst.layer)
	display_test(src.layer - dst.layer)
	
