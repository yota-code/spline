#!/usr/bin/env python3

class airplane() :

	dt = 0.0

	def __init__(self) :

		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

		self.phi = 0.0
		self.theta = 0.0
		self.psi

	def run(self, spd, phi, theta) :

		self.phi = phi
		self.theta = theta
		self.psi += self.gravity * math.tan(phi) / (spd * math.cos(theta))

		self.z += v * math.sin(theta) * self.dt


