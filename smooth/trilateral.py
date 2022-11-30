#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt

a = np.array([(t/9.0) ** 3 / (math.exp((t)/9.0) + 1) for t in range(100)])
b = np.random.standard_normal(100)
c = np.array([0.2 * math.cos(t*6.0 * t*9.0) for t in range(100)])
d = np.array([math.sqrt(t) for t in range(100)])
noisy = (d + 0.2 * ((a*b) + c)) % 5.5
#clean = (d) % 5.5
##plt.plot(noise)
##plt.plot(d)
#plt.plot(noisy)
#plt.plot(clean)
#plt.show()
#
u = [0.2,0.2,0.2,0.9,0.8,0.7]
# 2d

def gaussian(x, sigma=1.0, mu=0.0) :
	
	g = 1.0 / (sigma * np.power(2.0 * math.pi, 0.5))
	h = -1.0 * (2.0 * (sigma ** 2.0))

	return g * np.exp(np.power(x - mu, 2.0) / h)
	
def stack(a, radius, ) :
	s = np.vstack((
		np.hstack((
			np.zeros(radius + i),
			a,
			np.zeros(radius - i)
		))
		for i in range(-1 * radius, radius + 1)
	))
	return s
		
def bilateral_one(a, radius=3, g_sigma=1.0, v_sigma=1.0) :
	
	mask = stack(np.ones_like(a), radius)
	curve = stack(a, radius)
	
	x_dist = np.ogrid[-1 * radius:radius + 1]
	geometric_coef = gaussian(x_dist, g_sigma)[:,np.newaxis] * mask
	
	y_dist = curve - curve[radius,:]
	value_coef = gaussian(y_dist, v_sigma)
		
	n = np.sum(curve * geometric_coef * value_coef, axis=0)
	d = np.sum(geometric_coef * value_coef, axis=0)
	
	return (n/d)[radius:-radius]

def bound_one(a) :
	""" a point can not be higher or lower than it's neighbours """
	

def bilateral_one(a, radius=3, g_sigma=1.0, v_sigma=1.0) :
	
	mask = stack(np.ones_like(a), radius)
	curve = stack(a, radius)
	
	x_dist = np.ogrid[-1 * radius:radius + 1]
	geometric_coef = gaussian(x_dist, g_sigma)[:,np.newaxis] * mask
	
	y_dist = curve - curve[radius,:]
	value_coef = gaussian(y_dist, v_sigma)
		
	n = np.sum(curve * geometric_coef * value_coef, axis=0)
	d = np.sum(geometric_coef * value_coef, axis=0)
	
	return (n/d)[radius:-radius]


smoothed = bilateral_one(noisy, 12, 8.0, 2.0)


plt.plot(noisy)
plt.plot(smoothed)
plt.show()

# 3d min max

""" pour déterminer la pente au point courant :
	x
	y
	P[x,y]
poser U, le vecteur vers le point de coordonnée relative (m, n) :
	m
	n
	P[x+m,y+n] - P[x, y]
poser V, le vecteur 'à plat', perpendiculaire à U
	-n
	m
	0
normaliser U et V et prendre W = (U vectoriel V) * gaussian(distance(m,n))
additionner tous les vecteurs W pour tous les m et n sauf (0,0)
normaliser pour obtenir N"""

"""en s'approchant du bord, on pourrait également faire un rayon dégressif"""

