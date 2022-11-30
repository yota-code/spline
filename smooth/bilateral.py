#!/usr/bin/env python3

import math
import numpy as np



def _prepare_mask(a, radius) :

	#one_a = np.ones_like(a, dtype=np.double)
	one_a = np.ones_like(a.astype(np.double))

	mask_coef = np.vstack((
		np.hstack((
			np.zeros(radius),
			one_a,
			np.zeros(radius)
		))
		for i in range(-1 * radius, radius + 1)
	))
	
	mask_value = np.vstack((
		np.hstack((
			np.zeros(radius + i),
			one_a,
			np.zeros(radius - i)
		))
		for i in range(-1 * radius, radius + 1)
	))

	return mask_value * mask_coef

def gaussian(a, radius=3, sigma=2.5) :
	
	a = np.asarray(a, dtype=np.double)
	#one_a = np.ones_like(a, dtype=np.double)
	one_a = np.ones_like(a.astype(np.double))
	
	mask = _prepare_mask(a, radius)

	coef = np.vstack((
		np.hstack((
			np.zeros(radius),
			one_a * _normal_distribution(i, sigma, 0),
			np.zeros(radius)
		))
		for i in range(-1 * radius, radius + 1)
	))

	value = np.vstack((
		np.hstack((
			np.zeros(radius + i),
			a,
			np.zeros(radius - i)
		))
		for i in range(-1 * radius, radius + 1)
	))

	print("gaussian:\n", coef)
	
	value_sum = (value * coef * mask).sum(axis=0)[radius:-radius]
	coef_sum = (coef * mask).sum(axis=0)[radius:-radius]

	return value_sum / coef_sum
	
def score(a, b) :
	return sum((a - b)**2)

def bilateral(a, radius=3, alpha=2.5, beta=2.5) :
	
	a = np.asarray(a, dtype=np.double)
	
	value = np.vstack((
		np.hstack((
			np.zeros(radius + i),
			a,
			np.zeros(radius - i)
		))
		for i in range(-1 * radius, radius + 1)
	))

	#one_like_a = np.ones_like(a, dtype=np.double)
	one_like_a = np.ones_like(a.astype(np.double))
	regular_coef = np.vstack((
		np.hstack((
			np.zeros(radius),
			one_like_a * _normal_distribution(i, alpha, 0),
			np.zeros(radius)
		))
		for i in range(-1 * radius, radius + 1)
	))
	print("bilateral, regular_coef:\n", regular_coef)

	distance_zero = np.hstack((
		np.zeros(radius),
		a,
		np.zeros(radius)
	))
	distance = np.vstack((
		np.abs(np.hstack((
			np.zeros(radius + i),
			a,
			np.zeros(radius - i)
		)) - distance_zero)
		for i in range(-1 * radius, radius + 1)
	))
	distance_coef = _normal_distribution(distance, beta, 0.0)
	print("bilateral, distance_coef:\n", distance_coef)
	
	coef = (distance_coef * regular_coef)

	mask = _prepare_mask(a, radius)
	value_sum = (value * coef * mask).sum(axis=0)[radius:-radius]
	coef_sum = (coef * mask).sum(axis=0)[radius:-radius]
    
	return value_sum / coef_sum

		
if __name__ == '__main__' :
	import matplotlib.pyplot as plt
	import random
	#u = np.array([math.tanh(x/5.0) + 0.4 * ((random.random()**2) - 0.5) for x in range(-50,50)])
	q = [math.tanh(float(x)) for x in range(-10,10)]
	u = [math.tanh(float(x)) + 0.4 * ((random.random()**2) - 0.5) for x in range(-10,10)]
	g = gaussian(u, 5, 2.5)
	b = bilateral(u, 5, 2.5, 1.0)
	plt.plot(q)
	plt.plot(u)
	plt.plot(b)
	plt.plot(g)
	plt.plot((b-g))
	plt.show()
	print(score(u,b))
	print(score(u,g))
    

