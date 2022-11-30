import pen_revolution as pen
from spline import *
import numpy as np

class letter(object) :
	def __init__(self, strokes, param = None) :
		self.strokes = strokes
		
	def trace(self, paper, pen) :
		b = spline(step = (1.0/ pen.pxpc), order=4)
		for s in self.strokes :
			b.load_controls(s)
			cur, der = b.trace()
			pen.draw(paper, b.curve)
