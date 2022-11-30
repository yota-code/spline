from spline import *
import matplotlib.pyplot as plt

b = spline([[0,1],[2,1],[1,2],[0,2],[1,3],[3,2]], order=3)

print b.__dict__

#cpts = np.array([[1,3],[2,0],[3,4],[4,1],[5,3],[4,5],[2,4]], dtype=np.float64)

#cpts = np.array([[1,3,0],[2,0,0],[4,4,0],[1,5,0]], dtype=np.float64)


#b.timeline=np.array([0,0,0,0,2,2,2,2], dtype=np.float64)

print b.__dict__

b.trace()

#plt.subplot(2,1,1)
plt.plot(b.curve[:,0], b.curve[:,1],'.')
plt.plot(cpts[:,0], cpts[:,1], '--')

print plt.axis('scaled')

#l = np.sqrt(np.power(d[:,0],2) + np.power(d[:,1],2))
#
#plt.subplot(2,1,2)
#plt.plot(t, d[:,0], t, d[:,1], t, l,'.',t,max(l)/l)
plt.show()

