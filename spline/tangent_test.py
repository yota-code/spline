#!/usr/bin/env python

import math



def bezier(t) :
	a_x = 1
	b_x = 2
	c_x = -3
	d_x = -4
	
	a_y = 0
	b_y = -1
	c_y = 2
	d_y = 0
	
	return (
		a_x * t**3 + b_x * t**2 + c_x * t +d_x,
		a_y * t**3 + b_y * t**2 + c_y * t +d_y
	)
		
def solve_root_2(a, b, c) :
	delta = (b**2) - (4 * a * c)
	if delta == 0 :
		return (-1 * b) / (2 * a)
	if delta < 0 :
		return None
	if delta > 0 :
		return (
			((-1 * b) - math.sqrt(delta)) / (4 * a),
			((-1 * b) + math.sqrt(delta)) / (4 * a)
		)
		
print(solve_root_2(1, -1, -2))
