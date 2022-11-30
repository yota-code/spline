#!/usr/bin/env python3

import numpy as np

import math

def dct_1d(src, normalized=True) :
	row, = src.shape
	dst = np.zeros_like(src, dtype=np.double)
	for u in range(row) :
		z = 0.0
		for x in range(row) :
			z += src[x] * math.cos(math.pi * u * (2*x+1) / (2*row))
		if normalized and u == 0 :
			z *= 1.0 / math.sqrt(2.0)
		dst[u] = z
	return dst * (math.sqrt(2.0 / row) if normalized else 1.0)
	
def dct_2d(src, normalized=True) :
	""" compute the discrete cosine transform of a 2d array
	
	array is not necessarily square nor shape a multiple of 8, should be np.double
	"""
	row, col = src.shape
	
	tmp = np.zeros_like(src, dtype=np.double)
	for i in range(row) :
		tmp[i,:] = dct_1d(src[i,:], normalized)
		
	dst = np.zeros_like(src, dtype=np.double)
	for i in range(col) :
		dst[:,i] = dct_1d(tmp[:,i], normalized)

	return dst

def idct_1d(src, normalized=True) :
	row, = src.shape
	dst = np.zeros_like(src, dtype=np.double)
	for u in range(row) :
		z = src[0] / (math.sqrt(2) if normalized else 2)
		for x in range(1, row) :
			z += src[x] * math.cos(math.pi * x * (2*u+1) / (2*row))
		dst[u] = z
	return dst * (math.sqrt(2.0 / row) if normalized else 2.0 / row)
	
def idct_2d(src, normalized=True) :
	""" compute the discrete cosine transform of a 2d array
	
	array is not necessarily square nor shape a multiple of 8, should be np.double
	"""
	row, col = src.shape
	
	tmp = np.zeros_like(src, dtype=np.double)
	for i in range(row) :
		tmp[i,:] = idct_1d(src[i,:], normalized)
		
	dst = np.zeros_like(src, dtype=np.double)
	for i in range(col) :
		dst[:,i] = idct_1d(tmp[:,i], normalized)

	return dst

if __name__ == '__main__' :

	ref_img = np.array([
		[139, 144, 149, 153, 155, 155, 155, 155],
		[144, 151, 153, 156, 159, 156, 156, 156],
		[150, 155, 160, 163, 158, 156, 156, 156],
		[159, 161, 162, 160, 160, 159, 159, 159],
		[159, 160, 161, 162, 162, 155, 155, 155],
		[161, 161, 161, 161, 160, 157, 157, 157],
		[162, 162, 161, 163, 162, 157, 157, 157],
		[162, 162, 161, 161, 163, 158, 158, 158],
	])
	
	ref_dct = np.array([
		[1260, -1, -12, -5, 2, -2, -3, 1],
		-23, -17, -6, -3, -3, 0, 0, -1],
		-11, -9, -2, 2, 0, -1, -1, 0],
		-7, -2, 0, 1, 1, 0, 0, 0],
		-1, -1, 1, 2, 0, -1, 1, 1],
		2, 0, 2, 0, -1, 1, 1, -1],
		-1, 0, 0, -1, 0, 2, 1, -1],
		-3, 2, -4, -2, 2, 1, -1, 0],
 	])
	
	print(ref_img)
	try_dct = dct_2d(ref_img)
	print(try_dct.round().astype(np.int))
	try_img = idct_2d(try_dct)
	print(try_img.round().astype(np.int))
	
	print(np.sum((try_img - ref_img)) / 64)
	#r = 5
	#d = np.power(np.power(np.absolute(np.mgrid[-r:r+1,-r:r+1]), 2.0).sum(0), 1.0 / 2.0)
	#m = np.where(d <= 3.2, 1000, 0)[0:8,0:8]
	#m[5,3] = 24
	#
	#print(m, m.shape)
	#q = dct_2d(m)
	#print(q, q.shape)
	#r = (idct_2d(q)).round().astype(np.int)
	#print(r, r.shape)
	#print(np.array_equal(m, r))
	
