#!/usr/bin/env python3

import math
import numpy as np

#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D


		
def manhattan_distance(radius, dim) :
	radius = int(math.ceil(radius))
	if dim == 1 :
		return np.array(range(2 * radius + 1), dtype=np.double) - radius
	if dim == 2 :
		a, b = np.meshgrid(range(-radius, radius+1), range(-radius, radius+1))
		return np.abs(a) + np.abs(b)

def euclidean_distance(radius, dim) :
	radius = int(math.ceil(radius))
	if dim == 1 :
		return np.array(range(2 * radius + 1), dtype=np.double) - radius
	if dim == 2 :
		a, b = np.meshgrid(range(-radius, radius+1), range(-radius, radius+1))
		return np.sqrt(a**2 + b**2)
	
def one_square(kernel_radius, square_radius) :
	kernel_radius = int(math.ceil(kernel_radius))
	return np.ones((2 * kernel_radius + 1, 2 * kernel_radius + 1))
	
def one_circle(kernel_radius, dim, circle_radius=None) :
	# 1D & 2D compatible
	if circle_radius == None :
		circle_radius = float(kernel_radius)
	kernel_radius = int(math.ceil(kernel_radius))
	
	d = euclidean_distance(kernel_radius, dim)
	a_out = np.zeros_like(patch)
	a_in = np.ones_like(patch)
	
	return np.where(d > circle_radius, a_out, a_in)
	
class Kernel :
	def __init__(self, radius, dim) :
		self.radius = radius
		self.dim = dim
		
	def kernel(self, patch=None, mask=None) :
		return self._kernel

class GaussianBlur(Kernel) :
	def __init__(self, radius, dim, sigma=1.0, mu=0.0) :
		Kernel.__init__(self, radius, dim)
		self._kernel = gauss(euclidean_distance(radius, dim))


class CardinalSine(Kernel) :
	def __init__(self, radius, dim, freq=1.0) :
		Kernel.__init__(self, radius, dim)
		
		d = euclidean_distance(radius, dim)
		num = np.sin(freq * d * math.pi)
		den = (freq * d * math.pi)
		err = np.ones_like(d)
		self._kernel = np.where(div != 0.0, num / den, err)
		
class Bilateral(Kernel) :
	def __init__(self, radius, dim, sigma_d=2.5, sigma_r=2.5) :
		Kernel.__init__(self, radius, dim)
		self.sigma_d = sigma_d
		self.sigma_r = sigma_r
		
		d = euclidean_distance(radius, dim)
		self.kernel_d = gauss(d, self.sigma_d)
		
	def kernel(self, patch=None, mask=None) :
		# r = value distance in the patch, compared to the central point
		m = np.ones_like(patch) * patch[self.radius, self.radius]
		r = np.abs(patch - m)
		self.kernel_r = gauss(r, self.sigma_r)
		return self.kernel_r * self.kernel_d
		
class one_d :
	def __init__(self, a) :
		self.array = a
		self.shape = a.shape
		
	def _prepare(self, radius) :
		self._patch = np.hstack((
			np.ones((radius), dtype=np.int32),
			self.array,
			np.ones((radius), dtype=np.int32)
		))
		# to be corrected, 1.6 > ones_like prend l'argument dtype
		self._mask = np.hstack((
			np.zeros(radius),
			np.ones_like(self.array),
			np.zeros(radius)
		)).astype(np.int32)
		
	def _clean(self) :
		del self._patch, self._mask

	def mask(self, i, radius) :
		return self._mask[i:i+2*radius+1]
		
	def patch(self, i, radius) :
		return self._patch[i:i+2*radius+1]
		
	def smooth(self, kernel) :
		self._prepare(kernel.radius)
		result = np.zeros(self.shape)
		for i in np.indices(self.shape) :
			m = self.mask(i, kernel.radius)
			p = self.patch(i, kernel.radius)
			k = kernel.get(p, m)
			result[i] = (p * k * m).sum() / (k * m).sum()
		self._clean
		return one_d(result)

if __name__ == '__main__' :
	u = np.array([abs(math.sin((t/20.0)-5.0)) for t in range(100)])
	v = np.random.standard_normal((100,))
	#u = u + 0.1 * v
	#one = one_d(u)
	#print(one.a)
	#print(one._mask)
	#print(one.mask(0))
	#print(one.mask(1))
	radius = 5
	
	q = CardinalSine(radius, 2, 0.3, 0.0)
	print(q.get())

	#fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')
	
	#print(euclidean_distance(radius=2))
	#print(kernel_gaussian(radius=2))
	#print(kernel_circle(radius=2))
	
	#b = one.smooth(q)
	#x, y = np.meshgrid(range(-radius, radius+1), range(-radius, radius+1))
	#print(x, y)
	#ax.plot_wireframe(x, y, q.get())
	##plt.plot(b.array)
	#plt.show()
