from spline import *
import matplotlib.pyplot as plt
b = spline(order = 4, step = 0.07)
b.add_control([0.0,0.0,0.0])
b.add_control([1.0,0.0,0.0])
b.add_control([1.0,1.0,0.0])
b.add_control([0.0,2.0,0.0])
b.add_control([1.0,2.0,0.0])
print b.make_timeline()

#b.trace()
#plt.plot(b.curve[:,0], b.curve[:,1],'.')
#plt.show()
#plt.plot(b.derivate[:,0], b.derivate[:,1],'.')
#plt.show()
#b.calculate_curve(0.2)
#print b.N_values
#while True :
t = 1.3
print "--------------- old --------------", t
print b.calculate_curve(t)
print b.calculate_derivate(t)
print "--------------- new --------------"
print b.trace_curve(t)
print b.trace_derivate(t)
#b.calculate_curve(2.5)
#print b.N_values
#b.calculate_curve(3.1)
#print b.N_values
#b.N_values = b.N_values * 0.0
#b.quick_curve(1.3)
#print b.N_values
#b.quick_curve(2.5)
#print b.N_values
#b.quick_curve(3.1)
#print b.N_values
b.trace()
plt.subplot(2,1,1)
plt.plot(b.curve[:,0], b.curve[:,1],'.')
plt.axis('scaled')
plt.subplot(2,1,2)
plt.plot(b.derivate[:,0], b.derivate[:,1],'o')
plt.show()
#print b.timeline
#



