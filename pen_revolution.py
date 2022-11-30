import sys
from pen import *
import Image as im
import ImageChops as imops
import numpy as np

class pen_revolution(pen) :
	def __init__(self, param = None) :
		if param is None :
			self.param = {
				"radius" : 0.030,
				"pxpc" : 1024,
				"shape" : "cone"
			}
		else :
			self.param = param
		
		self.shape = self.param["shape"]
		self.pxpc = self.param["pxpc"]
		self.radius = self.param["radius"] * self.pxpc
		
		self.px_radius = int(np.ceil(self.radius))
		self.px_patch_x = int(np.ceil(self.radius))
		self.px_patch_y = int(np.ceil(self.radius))
		
		self.px_radius = self.px_patch_x
	
	def pen_shape(self, z) :
		if self.shape == "shpere" :
			return np.sqrt(1 - ((1 - z.clip(0,1)) **2)) * self.radius
		elif self.shape == "sqrt" :
			return np.sqrt(1 - ((1 - z.clip(0,1)))) * self.radius
		elif self.shape == "square" :
			return (1 - ((1 - z.clip(0,1)) **2)) * self.radius
		else :
			# cone
			return (1 - z.clip(0,1)) * self.radius
		
	def draw(self, paper, curve, derivate = None) :
		self.grid = np.mgrid[
			-self.px_patch_y:self.px_patch_y+1,
			-self.px_patch_x:self.px_patch_x+1]
			
		patch_shape = np.shape(self.grid[0])
		patch_shape = (patch_shape[1], patch_shape[0])
		
		print >>sys.stderr, "patch_shape\t\t", patch_shape
		
		patch = im.new('L', patch_shape)
		
		curve[:,2] = np.sqrt(1 - ((1 - curve[:,2].clip(0,1)) **2)) * self.radius
		
		curve[:,0] = curve[:,0] * self.pxpc
		curve[:,1] = curve[:,1] * self.pxpc
		
		for p in curve :
			if p[2] > 0 :
				x = int(p[0] + 0.5)
				y = int(p[1] + 0.5)
				delta_x = p[0] - x
				delta_y = p[1] - y
				distance = np.sqrt(
					(self.grid[0] - delta_x) **2 +
					(self.grid[1] - delta_y) **2)

				u = np.array(np.where(distance < p[2], 255, 0), dtype= np.int8)
				
				patch = im.fromstring('L', patch_shape, u.tostring())
				
				patch_pos = (
					x - self.px_patch_x - self.px_orig_x,
					y - self.px_patch_y - self.px_orig_y )
				
				paper.paste(patch, patch_pos, patch)
				
		paper = imops.invert(paper)
		paper = paper.transpose(im.FLIP_TOP_BOTTOM)
		
		paper.save("a.png")
				
