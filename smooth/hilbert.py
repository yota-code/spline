#!/usr/bin/env python3

import math
import numpy as np

# order 1
# B - C
# |   |
# A   D
#
# x y
# 0 0
# 0 1
# 1 1
# 1 0

# order 2
# x  y
#-------
# 00 00
# 00 01
# 01 01
# 01 00
#
# 10 00
# 11 00
# 11 01
# 10 01
#
# 10 10
# 11 10
# 11 11
# 10 11
#
# ...
#
#
# order 2
#[[0 0]
# [0 1]
# [1 1]
# [1 0]
# [2 0]
# [3 0]
# [3 1]
# [2 1]
# [2 2]
# [3 2]
# [3 3]
# [2 3]
# [1 3]
# [1 2]
# [0 2]
# [0 3]]

s = np.array([[0,0], [1,0], [2,0], [2,1], [1,1], [0,1], [0,2], [0,3], [1,3], [1,2], [2,2], [2,3], [3,3], [3,2], [3,1], [3,0]])


# run hilbert curve on a square and remove as many line as needed to get a rectangle

A_0 = np.array([[0,0],[0,1],[1,1],[1,0]])
B_0 = np.array([[0,0],[1,0],[1,1],[0,1]])
C_0 = np.array([[0,0],[1,0],[1,1],[0,1]])
D_0 = np.array([[1,1],[1,0],[0,0],[0,1]])


def translate(array, x, y) :
	size = int(math.sqrt(array.shape[0]))
	return array + np.array([x*size, y*size])
	
def spin(array) :
	# 180 degree rotation
	size = int(math.sqrt(array.shape[0]))
	return np.array([(size-1), (size-1)]) - array
	
def bflip(array) :
	size = int(math.sqrt(array.shape[0]))
	return np.hstack((array[:,1:2], array[:,0:1]))
	
def xflip(array) :
	size = int(math.sqrt(array.shape[0]))
	return np.hstack(((size-1) - array[:,1:2], (size-1) - array[:,0:1]))	
	
def rtilt(array) :
	# +90 degree
	size = int(math.sqrt(array.shape[0]))
	return np.hstack((array[:,1:2], (size-1) - array[:,0:1]))

def ltilt(array) :
	# +90 degree
	size = int(math.sqrt(array.shape[0]))
	return np.hstack(((size-1) - array[:,1:2], array[:,0:1]))

def hflip(array) :
	size = int(math.sqrt(array.shape[0]))
	return np.hstack(((size-1) - array[:,0:1], array[:,1:2]))
	
def vflip(array) :
	size = int(math.sqrt(array.shape[0]))
	return np.hstack((array[:,0:1], (size-1) - array[:,1:2]))	
	
A_1 = np.vstack((A_0+[0,0], B_0+[2,0], C_0+[2,2], D_0+[0,2]))

def hilbert_2d(order=2) :
	if order == 1 :
		return np.array([[0,0],[0,1],[1,1],[1,0]]) # basic staple-like shape
	
	sub = hilbert_2d(order-1)
	
	A = bflip(sub)
	B = translate(sub, 0, 1)
	C = translate(sub, 1, 1)
	D = translate(xflip(sub), 1, 0)
	
	return np.vstack((A, B, C, D))
	
def print_4x4(array) :
	snake = np.zeros((4,4), dtype=np.int32)
	for n, (x, y) in enumerate(array) :
		snake[3-y, x] = n
	
	plot = np.zeros((7,7), dtype=np.str)
	for r in range(7) :
		for c in range(7) :
			plot[r,c] = ' '
			
	for r in range(4) :
		for c in range(3) :
			if abs(snake[r,c] - snake[r,c+1]) == 1 :
				plot[(2*r), (2*c)+1] = '-'
				
	for r in range(3) :
		for c in range(4) :
			if abs(snake[r,c] - snake[r+1,c]) == 1 :
				plot[(2*r)+1, (2*c)] = '|'

	for r in range(4) :
		for c in range(4) :
			plot[2*r, 2*c] = '{0:X}'.format(snake[r,c])
				
	for row in plot :
		print('\t' + ''.join(row))
			
	
def print_s(array) :
	size = int(math.sqrt(array.shape[0]))
	
	snake = np.zeros((size,size), dtype=np.int32)
	for n, (x, y) in enumerate(array) :
		snake[(size-1)-y, x] = n
	
	plot = np.zeros((2*size-1,2*size-1), dtype=np.str)
	for r in range(2*size-1) :
		for c in range(2*size-1) :
			plot[r,c] = ' '
			
	for r in range(size) :
		for c in range(size-1) :
			if abs(snake[r,c] - snake[r,c+1]) == 1 :
				plot[(2*r), (2*c)+1] = '-'
				
	for r in range(size-1) :
		for c in range(size) :
			if abs(snake[r,c] - snake[r+1,c]) == 1 :
				plot[(2*r)+1, (2*c)] = '|'

	for r in range(size) :
		for c in range(size) :
			plot[2*r, 2*c] = ' ' if (snake[r,c] != 0xf and snake[r,c] != 0x0) else '{0:X}'.format(snake[r,c])
				
	for row in plot :
		print('\t' + ''.join(row))	
	
if __name__ == '__main__' :
	
	print("normal")
	print_4x4(s)
	
	#p = spin(s)
	#print("spin")
	#print_4x4(p)
	#
	#p = hflip(s)
	#print("hflip")
	#print_4x4(p)
    #
	#p = vflip(s)
	#print("vflip")
	#print_4x4(p)
    #
	#p = rtilt(s)
	#print("rtilt")
	#print_4x4(p)
    #
	#p = ltilt(s)
	#print("ltilt")
	#print_4x4(p)
	
	print("hilbert")	
	u = hilbert_iterator(4)
	print(u)
	print_s(u)

