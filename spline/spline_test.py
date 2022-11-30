#!/usr/bin/env python

import spline, math

b = spline.Bezier()

b.set_control(((0,0), (2,-1), (0,3), (2,4)))

for i in range(0,5) :
	print float(i)/4, b.position(float(i)/4)

#print b.p
#print b.p0
#print b.p0[:,1]
#
#print b.p1
#
#print math.degrees(b.tangent(0.258497))
#print b.position(0.258497)
#print b.velocity(0.258497)

for i in b.find_tangent(1,1) :
	print i, b.position(i)
#
#print b.position(1.0)
#x, y = b.velocity(1.0)
#print math.atan2(y, x)
 
