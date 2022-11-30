#!/usr/bin/env python2.7

def kernel_distance(radius) :
	# 2D distance
	a, b = np.meshgrid(range(-radius, radius+1), range(-radius, radius+1))
	kernel = np.sqrt(a**2 + b**2)
	return kernel
