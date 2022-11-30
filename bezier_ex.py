import matplotlib.pyplot as mpl
import numpy as np

p = np.array([
	[1,1],
	[2,1],
	[2,2],
	[1,3],
], dtype=np.float)

def bezier_curve(p, res=10) :
	curve = np.zeros((res + 1, 2))
	for i in xrange(res + 1) :
		t = i / float(res)
		curve[i,:] = (((1-t)**3)*p[0]
			+ 3*(t)*((1-t)**2)*p[1]
			+ 3*(t**2)*(1-t)*p[2]
			+ (t**3)*p[3])
	return curve

def bezier_curve2(p, res=10) :
	curve = np.zeros((res + 1, 2))
	for i in xrange(res + 1) :
		t = i / float(res)
		curve[i,:] = ((p[3]-3*p[2]+3*p[1]-p[0])*(t**3)
			+ (3*p[2]-6*p[1]+3*p[0])*(t**2)
			+ (3*p[1]-3*p[0])*(t)
			+ p[0])
	return curve
	
def bezier_reframe(p, m) :
	p0, p1, p2, p3 = p[0,:], p[1,:], p[2,:], p[3,:]
	q = np.zeros_like(p)
	q[0,:] = p0
	q[1,:] = m*p1+(1-m)*p0
	q[2,:] = (m**2)*p2+(2*m*(1-m))*p1+((1-m)**2)*p0
	q[3,:] = (m**3)*p3+(3*(m**2)*(1-m))*p2+(3*(m)*(1-m)**2)*p1+((1-m)**3)*p0
	return q
	
def bezier_reframe2(p, a, b) :
	#not good
	p0, p1, p2, p3 = p[0,:], p[1,:], p[2,:], p[3,:]
	q = np.zeros_like(p)
	q[0,:] = ((1-a)**3)*p0+3*a*((1-a)**2)*p1+3*(a**2)*(1-a)*p2+(a**3)*p3
	q[1,:] = (2*(1-a)/(b-a))*(p1 - p0) + q[0,:]
	q[2,:] = p2
	q[3,:] = ((1-b)**3)*p0+3*b*((1-b)**2)*p1+3*(b**2)*(1-b)*p2+(b**3)*p3
	return q
	
q = bezier_reframe2(p, 0.1, 0.7)
print q
u = bezier_curve2(p,500)
v = bezier_curve2(q,500)

mpl.plot(u[:,0], u[:,1], p[:,0], p[:,1],v[:,0], v[:,1], q[:,0], q[:,1])

mpl.show()
