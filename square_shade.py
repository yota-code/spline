import math
import matplotlib.pyplot as mpl

math.sqrt_2 = math.sqrt(2.0)
math.pi_4 = math.pi / 4.0
math.pi_2 = math.pi / 2.0

def square_shade1(alpha, d) :
	alpha = abs(alpha) % math.pi_4
	theta = alpha + math.pi_2
	if 0.5 > abs(d / math.cos(alpha)) + (0.5 * math.tan(alpha)) :
		#print "case 1"
		return 0.5 + d * (1 / math.cos(alpha))
	else :
		#print "case 2"	
		y = max(0.5 - ((0.5 * math.sin(theta) - abs(d)) / math.cos(theta)), 0)
		x = max(0.5 - ((0.5 * math.cos(theta) + abs(d)) / math.sin(theta)), 0)
		if d > 0 :
			return 1 - x * y / 2
		else :
			return x * y / 2
			
def square_shade2(alpha, delta) :
	alpha = abs(alpha) % math.pi_4
	a_t = 0.5 * math.tan(alpha)
	a_p = 1 - 2 * a_t
	print "a_t =", a_t
	print "a_p =", a_p
	if abs(x) < math.cos(alpha + math.pi_4) :
		return a_p / ( math.sqrt_2 * math.cos(alpha + math.pi_4)) * delta + 0.5
	else :
		pass
		
def square_shade3(alpha, delta) :
	alpha = abs(alpha) % math.pi_4
	if abs(delta) < math.cos(alpha + math.pi_4) :
		#print "case 1"
		return 0.5 + delta * (1 / math.cos(alpha))
	else :
		#print "case 2"	
		y = max(0.5 + ((0.5 * math.cos(alpha) - abs(delta)) / math.sin(alpha)), 0)
		x = max(0.5 - ((- 0.5 * math.sin(alpha) + abs(delta)) / math.cos(alpha)), 0)
		if delta > 0 :
			return 1 - x * y / 2
		else :
			return x * y / 2

def square_shade4(alpha, delta) :
	alpha = abs(alpha) % math.pi_4
	if abs(delta) < 0.5 * math.sqrt_2 * math.sin(alpha) :
		#print "case 1"
		return 0.5 + delta * (1 / math.cos(alpha))
	else :
		#print "case 2"
		h = 0.5 * math.sqrt_2 * math.cos(math.pi_4 - alpha) - abs(delta)
		a = 0.5 * max(h / math.cos(alpha),0) * max(h / math.sin(alpha),0)
		if delta > 0 :
			return 1 - a
		else :
			return a
			
def square_shade(alpha, delta) :
	alpha = abs(alpha) % math.pi_4
	
	sin_alpha = math.sin(alpha)
	cos_alpha = math.cos(alpha)
	abs_delta = abs(delta)
	
	if abs_delta < 0.5 * math.sqrt_2 * sin_alpha :
		return 0.5 + delta * (1 / cos_alpha)
	else :
		h = 0.5 * math.sqrt_2 * math.cos(math.pi_4 - alpha) - abs_delta
		a = 0.5 * max(h / cos_alpha,0) * max(h / sin_alpha,0)
		return ((1 - a) if (delta > 0) else (a))

