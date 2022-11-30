# -*- coding: UTF-8 -*-

from math import *
import numpy as np
import sys


def rotation(point, angle) :
	rot_x = np.mat([
		[ 1.0,              0.0,               0.0 ],
		[ 0.0,  np.cos(angle[0]), np.sin(angle[0]) ],
		[ 0.0, -np.sin(angle[0]), np.cos(angle[0]) ]], dtype=np.float64)
	
	rot_y = np.mat([
		[ np.cos(angle[1]), 0.0, -np.sin(angle[1]) ],
		[              0.0, 1.0,               0.0 ],
		[ np.sin(angle[1]), 0.0,  np.cos(angle[1]) ]], dtype=np.float64)

	rot_z = np.mat([
		[  np.cos(angle[2]), np.sin(angle[2]), 0.0 ],
		[ -np.sin(angle[2]), np.cos(angle[2]), 0.0 ],
		[               0.0,              0.0, 1.0 ]], dtype=np.float64)

	return np.asarray(rot_y * rot_x * rot_z * np.asmatrix(point))
	

class curve(object) :
	def dot(self, t) :
		pass
	
	def tan(self, t) :
		pass
	
class pen(object) :
	pass

class ellipsoid(pen) : 
	def __init__(self) :
		# self.p = p
		self.p = {
			"e" : np.array([
				[1.0],
				[2.0],
				[1.0]], dtype=np.float64),
			"inclination" : np.pi * np.array([
				[0.0],
				[0.0],
				[0.0]], dtype=np.float64),
			"size" : 3.0
		}
		
	def ellipse(x, y, z) :
		pass
	
	def pressure(self, z) :
		return z * self.p["e"][2,0] * np.cos(self.p["inclination"][1,0])
		
	def plot(self, pos_0, vec = np.array([1,1,1], dtype=np.float64)) :
		for px in range(-10,9) :
			for py in range(-10,9) :
				"""
				px, py : absolute coordinates of the pixel tested in the pixel space
				pos : in absolute coordinates of point on the curve where the pen mark is drawn
				pos_0 : in relative coordinates colinear to the paper scale, where
					the origin is the tip of the pen
				pos_1 : in relative coordinates, same origine but tilded planes
				pos_2 : in relative coordinates, same planes but origin at the center of the ellipse
				
				pour connaitre le périmetre à dessiner, garder une bande de 3 pixel 
				blanc autour, si un des bords est empiété, décaler le cadre du stamp"""
				pos_1 = np.array([
					[ px + int(pos_0[0,0])      ],
					[ py + int(pos_0[1,0])      ],
					[ self.pressure(pos_0[2,0]) ]], dtype=np.float)
				
				pos_2 = rotation(pos_1 , self.p["inclination"][:,0])
				pos_3 = (pos_2 - [[0.0],[0.0],[self.p["e"][2,0]]])
				
				ellipse = ((pos_3**2) / (self.p["e"]**2)).sum()
				
				#print >>sys.stderr, ellipse
				
				if ellipse <= ((self.p["size"])**2) :
					sys.stdout.write("Ü ")
				else :
					sys.stdout.write("  ")
			sys.stdout.write("\n")

class simple_bezier(curve) :
	def __init__(self) :
		self.curr_time = 0
		self.last_point = False
		self.first_point = True
		self.control_points = np.array([[0,0.2],[0.2,0],[1,0.5],[0,1]], dtype=np.float64)
		self.curr_dot = np.array([0,0], dtype=np.float64)
		self.curr_tan = np.array([0,0], dtype=np.float64)
		
		self.step = 0.01
		
	def __str__(self) :
		a = "%0.3f\t" % self.curr_time
		a += "\t".join(["%0.3f" % u for u in self.curr_dot])
		a += "\t" + "\t".join(["%0.3f" % u for u in self.curr_tan])
		#print "%0.3f\t" % self.curr_time, "coin", "\t".join(["%0.3f" % u for u in self.curr_dot]), "bu", "\t" + "\t".join(["%0.3f" % u for u in self.curr_tan])
		return a
	
	def dot(self, t = None) :
		if t == None :
			t = self.curr_time
		self.curr_dot = (((1-t)**3) * self.control_points[0,:] +
			         3*((1-t)**2)*t * self.control_points[1,:] +
			         3*(1-t)*(t**2) * self.control_points[2,:] +
			                 (t**3) * self.control_points[3,:] )
		return self.curr_dot
		
	def next_dot(self) :
		self.tan()
		if self.first_point == True :
			print >>sys.stderr, "first", self.first_point
			t = 0
			self.first_point = False
		else :
			t = self.curr_time + self.step / self.speed()
		if self.last_point == True :
			print >>sys.stderr, "last", self.last_point
			return None
			
		if t > 1 :
			t = 1
			self.last_point = True
			
		self.curr_time = t
		
		self.dot()
		
		return t
	
	def tan(self, t = None) :
		if t == None :
			t = self.curr_time
		self.curr_tan = ((-3+6*t-3*(t**2)) * self.control_points[0,:] +
			                       (3-6*t) * self.control_points[1,:] +
			                (6*t-9*(t**2)) * self.control_points[2,:] +
			                    (3*(t**2)) * self.control_points[3,:] )
		return self.curr_tan
		
	def speed(self) :
		return np.sqrt((self.tan() **2).sum())

#b = simple_bezier()
#
#while b.next_dot() != None :
#	print >>sys.stderr, b.curr_time
#	print b

#k = 0
#step = 0.025
#print "k\tpx\tpy\tsx\tsy\ts"
#while k < 1 :
#	px = calculate_curve(k, axe_(pts,0))
#	py = calculate_curve(k, axe_(pts,1))
#	sy, sx, s = estimate_speed(k, pts)
#	print "%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f" % (k, px,py,sx, sy, s)
#	k += step * 1/s


