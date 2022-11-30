import Image as im
import numpy as np

class pen(object) :
	def __init__(self, image, param = None) :
		self.image = image
		self.param = param
		
	def rotation_matrix(axe, angle) :
		if axe =='x' :
			return np.mat([
				[ 1,              0,             0 ],
				[ 0,  np.cos(angle), np.sin(angle) ],
				[ 0, -np.sin(angle), np.cos(angle) ]], dtype=np.float64)
			
		elif axe == 'y' :	
			return np.mat([
				[ np.cos(angle), 0, -np.sin(angle) ],
				[             0, 1,              0 ],
				[ np.sin(angle), 0,  np.cos(angle) ]], dtype=np.float64)
			
		elif axe == 'z' :
			return np.mat([
				[  np.cos(angle), np.sin(angle), 0 ],
				[ -np.sin(angle), np.cos(angle), 0 ],
				[              0,             0, 1 ]], dtype=np.float64)	
		
	def rotate(point, angles) :
		return np.asarray(
			self.rotation_matrix('z', angles[2]) *
			self.rotation_matrix('x', angles[1]) *
			self.rotation_matrix('z', angles[0]) * np.asmatrix(point).reshape((3,1)))

	def draw(self, curve, derivate) :
		pass
