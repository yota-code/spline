import sys
from pen import *
import Image as im
import ImageChops as imops
import numpy as np

class pen_line(pen) :
	def __init__(self, param = None) :
		if param is None :
			self.param = {
				"pxpc" : 500
			}
		else :
			self.param = param
		self.pxpc = self.param["pxpc"]
		self.px_radius = 5

	def draw(self, paper, curve, derivate = None) :
		r = self.px_radius
		
		patch = im.new('L', (1,1))
		patch = imops.invert(patch)
		
		curve[:,0] = curve[:,0] * self.pxpc + self.px_margin
		curve[:,1] = curve[:,1] * self.pxpc + self.px_margin
		
		for p in curve :
			if p[2] > 0 :
				x = int(p[0] + 0.5)
				y = int(p[1] + 0.5)
				
				paper.paste(patch, (x, y), patch)
				
		for i in range(5) :
			paper.paste(patch, (5*i, 5*i), patch)
		
		h, w = paper.size
		
		for x in range(h) :
			paper.paste(patch, (x, self.px_margin), patch)
			paper.paste(patch, (x, w - self.px_margin), patch)
			
		print >>sys.stderr, "x0_line", self.px_margin
		print >>sys.stderr, "x1_line", w - self.px_margin
		
		for y in range(w) :
			paper.paste(patch, (h - self.px_margin, y), patch)
			paper.paste(patch, (self.px_margin, y), patch)
			
		print >>sys.stderr, "y0_line", self.px_margin
		print >>sys.stderr, "y1_line", h - self.px_margin

		paper = imops.invert(paper)
		paper = paper.transpose(im.FLIP_TOP_BOTTOM)
		
		paper.save("a.png")
				
