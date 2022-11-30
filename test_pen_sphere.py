from pen_sphere import *
from spline import *

s = 255 * np.ones((500,500), dtype = np.int8)

center = (50, 50)


p = pen_sphere()

cpts = ([[180,200,1],
		[90,220,0.5],
		[90,80,0.5],
		[200,120,0.8],
		[200,200,0.0],
		[200,200,0.8],
		[180,80,0.7],
		[230,120,0.0]])



b = spline(dimension = 3, order = 4)

for c in cpts :
	b.add_control(c)

b.trace()

print b.timeline

plt.plot(b.curve[:,0], b.curve[:,1],'.')

print np.shape(b.curve)


p.draw(b.curve)

u = im.fromstring('L', (500,500), s.tostring())

