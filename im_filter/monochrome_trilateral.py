#!/usr/bin/env python3

from PIL import Image

import math

import numpy as np
import numpy.ma as ma

img = Image.open("img/1744gg.jpg")
r, g, b = (np.asarray(i) / 255.0  for i in img.split())

y = 0.2126 * r + 0.7152 *g + 0.0722 * b

#img = Image.fromarray(np.uint8(y * 255.0))
#img.show()

print(type(r), r.shape, r.dtype)

def mask(width, radius, norm) :
	r = (width-1)//2
	a, b = np.power(np.abs(np.mgrid[-r:r+1,-r:r+1]), norm)
	d = (np.power(a + b, 1.0 / norm) / radius)
	return np.where(d < 1.0, 0, 1)
	
class Patch(ma.MaskedArray) :
	def __init__(self, radius, norm=2.0) :
		width = (2 * int(math.ceil(radius))) + 1
		
		m = mask(width, radius, norm)
		v = np.zeros((width, width), dtype=np.double)
			
		ma.MaskedArray.__init__(self, v, m)
		
		
		
p = Patch(3.5)
print(p)
		
		
