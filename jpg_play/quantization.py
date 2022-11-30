#!/usr/bin/env python3

import numpy as np

luminance_standard = np.array([
	[ 16, 11, 10, 16,  24,  40,  51,  61],
	[ 12, 12, 14, 19,  26,  58,  60,  55],
	[ 14, 13, 16, 24,  40,  57,  69,  56],
	[ 14, 17, 22, 29,  51,  87,  80,  62],
	[ 18, 22, 37, 56,  68, 109, 103,  77],
	[ 24, 35, 55, 64,  81, 104, 113,  92],
	[ 49, 64, 78, 87, 103, 121, 120, 101],
	[ 72, 92, 95, 98, 112, 100, 103,  99],
])

chrominance_standard = np.array([
	[ 17, 18, 24, 47, 99, 99, 99, 99],
	[ 18, 21, 26, 66, 99, 99, 99, 99],
	[ 24, 26, 56, 99, 99, 99, 99, 99],
	[ 47, 66, 99, 99, 99, 99, 99, 99],
	[ 99, 99, 99, 99, 99, 99, 99, 99],
	[ 99, 99, 99, 99, 99, 99, 99, 99],
	[ 99, 99, 99, 99, 99, 99, 99, 99],
	[ 99, 99, 99, 99, 99, 99, 99, 99],
])

def quantization_matrix(base, quality):
	"""
	scale DCT matrix given quality in [1, 100]
	"""
	if not 1 <= quality <= 100 :
		raise ValueError
	scale = (50.0 / quality) if (quality < 50) else (2.0 - quality / 50.0)
	return (base * scale).clip(1.0, 512.0)
	
if __name__ == '__main__' :
	
	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import axes3d
	
	fig = plt.figure()
	ax = fig.add_subplot('111', projection='3d')
	
	x, y = np.mgrid[0:8, 0:8]
	
	#ax.plot_wireframe(x, y, standard_jpeg_50)
	#plt.show()
	
	for i in range(1, 101) :
		print(i, quantization_matrix(chrominance_standard, i), sep='\n')
	
	
	
	
	
	
	