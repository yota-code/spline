from letter import *
from paper import *
from pen_revolution import *
from pen_line import *
import numpy as np

letter_agrave = \
	[[[0.180,0.200,0.1],
	[0.000,0.220,0.5],
	[0.090,0.080,0.5],
	[0.200,0.120,0.8],
	[0.200,0.200,0.7],
	[0.200,0.200,0.8],
	[0.180,0.00,0.7],
	[0.230,0.120,0.0]],
	[[0.100,0.250,0.1],
	
	[0.160,0.220,0.8],
	[0.200,0.230,0.0]]]

#letter_agrave = \
#	[[[0.180,0.200,0.1],
#	[0.000,0.220,0.5],
#	[0.090,0.080,0.5],
#	[0.200,0.120,0.8],
#	[-0.200,-0.200,0.8],
#	[-0.180,-0.00,0.7],
#	[-0.230,-0.120,0.0]]]
	
letter_o = \
	[[[0.0,0.0,0.0],
	[0.0,0.8,0.5],
	[0.8,0.0,0.0],
	[0.8,-0.8,0.5],
	[0.0,-0.8,0.0],
	[-0.8,-0.8,0.5],
	[-0.8,0.0,0.0],
	[-0.8,0.8,0.5]]]	
	
	
letter_alpha = \
	[[[0,1,1],
	[0.3,0.5,1],
	[0.5,0,-0.8],
	[1,0.5,2],
	[0.5,1,-0.8],
	[0.3,0.5,1],
	[0,0,1]]]
	
letter_a = \
	[[[0.180,0.200,0.1],
	[0.180,0.200,0.1],
	[0.180,0.200,0.1],
	[0.000,0.220,0.5],
	[0.000,0.220,0.5],
	[0.000,0.220,0.5],
	[0.090,0.080,0.5],
	[0.090,0.080,0.5],
	[0.090,0.080,0.5],
	[0.200,0.120,0.8],
	[0.200,0.120,0.8],
	[0.200,0.120,0.8],
	[0.200,0.200,0.7],
	[0.200,0.200,0.7],
	[0.200,0.200,0.7],
	[0.180,0.00,0.7],
	[0.180,0.00,0.7],
	[0.180,0.00,0.7],
	[0.230,0.120,0.0],
	[0.230,0.120,0.0],
	[0.230,0.120,0.0]]]
	
kanji_taberu = \
	[[[0.2,0.8,1.0],
	[0.35,0.85,0.0],
	[0.5,0.9,1.0],
	[0.5,0.9,0.0],
	[0.5,0.9,0.0],
	[0.65,0.85,0.2],
	[0.8,0.8,1.0]],
	[[0.55,0.82,1.0],
	[0.45,0.75,0.0]],
	[[0.3,0.75,1.0],
	[0.7,0.75,1.0],
	[0.7,0.75,1.0],
	[0.7,0.45,1.0]],
	[[0.3,0.75,1.0],
	[0.3,0.0,1.0],
	[0.3,0.0,0.2],
	[0.4,0.03,0.1],
	[0.5,0.10,0.0]],
	[[0.3,0.60,1.0],
	[0.7,0.60,1.0]],
	[[0.3,0.45,1.0],
	[0.7,0.45,1.0]],
	[[0.75,0.3,1.0],
	[0.5,0.2,0.0]],
	[[0.45,0.2,1.0],
	[0.8,0.0,0.0]]]
	
kanji_guchi_1 = [[
	[ 0.0, 1.0, 0.0],
	[ 0.0, 1.0, 1.0],
	[ 0.5, 1.0, 0.0],
	[ 1.0, 1.0, 0.8],
	[ 1.0, 1.0, 1.0],
	[ 1.0, 1.0, 0.2],
	[ 1.0, 0.0, 0.2],
	[ 1.0, 0.0, 1.0],
	[ 0.99, 0.0, 0.0],
	[ 0.95, 0.03, 0.0]]]
	
	
p = pen_revolution()
#p = pen_line()
l = letter(kanji_guchi_1)
l_paper = prepare_paper(l,p)

print >>sys.stderr, "l_paper.size\t\t", l_paper.size

l.trace(l_paper, p)