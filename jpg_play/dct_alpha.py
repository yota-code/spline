#!/usr/bin/env python3

import numpy as np

import math
	
def dct_2d(src) :
	""" compute the discrete cosine transform of a 2d array
	
	\begin{eqnarray*}
	C_i & = & \left\{\begin{array}{ll}
		\frac{1}{\sqrt{2}} & \textrm{if $i=0$}\\
		1 & \textrm{else}
	\end{array}\right.\\
	
	F_{vu} & = & \frac{1}{\sqrt{2N}} C_v C_u
		\sum_{y=0}^{N-1}
		\sum_{x=0}^{N-1}
		S_{yx}
		cos\left(v\pi\frac{2y+1}{2N}\right)
		cos\left(u\pi\frac{2x+1}{2N}\right)
	\end{eqnarray*}
	"""
	
	dst = np.zeros_like(src, dtype=np.double)
	row, col = src.shape
	print(src.shape, math.sqrt(2*row))
	for u in range(row) :
		for v in range(col) :
			Cu = 1.0 / math.sqrt(2.0) if u == 0 else 1.0
			Cv = 1.0 / math.sqrt(2.0) if v == 0 else 1.0
			z = 0.0
			for x in range(row) :
				for y in range(col) :
					z += src[x,y] * (
						math.cos((2*x+1) * u * math.pi / (2*row)) *
						math.cos((2*y+1) * v * math.pi / (2*col))
					)
			dst[u,v] = Cu * Cv * z / math.sqrt(2*row)
	return dst #/ max(src.shape) * min(src.shape)
	
def idct_2d(src) :
	"""
	S_{yx} = \frac{1}{4}
		\sum_{v=0}^{N-1}
		\sum_{u=0}^{N-1}
		C_v C_u F_{vu}
		cos\left(v\pi\frac{2y+1}{2N}\right)
		cos\left(u\pi\frac{2x+1}{2N}\right)
	"""
	dst = np.zeros_like(src, dtype=np.double)
	row, col = src.shape
	for x in range(row) :
		for y in range(col) :
			z = 0.0
			for u in range(row) :
				for v in range(col) :
					Cu = 1.0 / math.sqrt(2.0) if u == 0 else 1.0
					Cv = 1.0 / math.sqrt(2.0) if v == 0 else 1.0
					z += src[u,v] * Cu * Cv * (
						math.cos((2*x+1) * u * math.pi / (2*row)) *
						math.cos((2*y+1) * v * math.pi / (2*col))
					)
			dst[x, y] = z / 4.0
	return dst #/ max(src.shape) * min(src.shape)
					
if __name__ == '__main__' :
	#r = 5
	#d = np.power(np.power(np.absolute(np.mgrid[-r:r+1,-r:r+1]), 2.0).sum(0), 1.0 / 2.0)
	#m = np.where(d <= 3.2, 1000, 0)[0:10,0:10]
	#m[5,3] = 24
	
	
	ref_img = np.array([
		[140, 144, 147, 140, 140, 155, 179, 175],
		[144, 152, 140, 147, 140, 148, 167, 179],
		[152, 155, 136, 167, 163, 162, 152, 172],
		[168, 145, 156, 160, 152, 155, 136, 160],
		[162, 148, 156, 148, 140, 136, 147, 162],
		[147, 167, 140, 155, 155, 140, 136, 162],
		[136, 156, 123, 167, 162, 144, 140, 147],
		[148, 155, 136, 155, 152, 147, 147, 136]
	])
	
	ref_dct = np.array([
		[186, -18, 15, -9, 23, -9, -14, 19],
		[ 21, -34, 26, -9, -11, 11, 14, 7],
		[-10, -24, -2, 6, -18, 3, -20, -1],
		[ -8,  -5, 14, -15, -8, -3, -3, 8],
		[ -3,  10, 8, 1, -11, 18, 18, 15],
		[  4,  -2, -18, 8, 8, -4, 1, -7],
		[  9,   1, -3, 4, -1, -7, -1, -2],
		[  0,  -8, -2, 2, 1, 4, -6, 0]
	])
	
	print(ref_dct)
	
	try_dct = dct_2d(ref_img).round().astype(np.int)
	
	print(try_dct)
	

	#print(m, m.shape)
	#q = dct_2d(m)
	#print(q, q.shape)
	#r = (idct_2d(q)).round().astype(np.int)
	#print(r, r.shape)
	#print(np.array_equal(m, r))
	
