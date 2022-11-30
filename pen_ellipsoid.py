from pen import *

import Image as im
import numpy as np

class pen_ellipsoid(pen) :
	def __init__(self, image, param = None) :
		self.image = image
		self.param = {
			"radius" : 20.0,
			"w-coef" : 0.8,
			"l-coef" : 1.0
		}
		
	def set_pressure(self, p) :
		if p > 1 :
			p = 1
		self.radius = np.sin(p) * self.param["radius"]
	
	def dist_2d(self, a, b) :
		return np.sqrt(((float(a[0]) - float(b[0]))**2) + ((float(a[1]) - float(b[1]))**2))
	
	def norm(self, vect, k = 2) :
		return np.power(np.sum(np.power(np.asarray(vect),k)), 1.0 / k)

	def draw(self, curve, derivate = None) :
		self.set_pressure(curve[2, 0])
		
		rot_z = self.rotation_matrix('z', np.arctan2(derivate[1], derivate[0]))

		r = self.radius
		
		region = (
			int(np.floor(curve[0] - r - 1)),
			int(np.ceil(curve[1] + r + 1)),
			int(np.ceil(curve[0] + r + 1)),
			int(np.floor(curve[1] - r - 1))
		)
		
		for i in range(region[0], region[2]) :
			for j in range(region[3], region[1]) :
				pixel = np.array([[i], [j], [0]])
				pixel = pixel - curve 
				pixel = rot_z * pixel
				if self.dist_2d((i,j), (curve[0], curve[1])) < r :
					self.image[i,j] = 0
