import sys, os
import numpy as np
import Image as im

def prepare_paper(letter, pen) :
	box = np.array([
		letter.strokes[0][0][0],
		letter.strokes[0][0][1],
		letter.strokes[0][0][0],
		letter.strokes[0][0][1]], dtype=np.float64)
	
	for s in letter.strokes :
		box[0] = min(box[0], min([i[0] for i in s]))
		box[1] = max(box[1], max([i[1] for i in s]))
		box[2] = max(box[2], max([i[0] for i in s]))
		box[3] = min(box[3], min([i[1] for i in s]))
		
	px_box = np.array(box * pen.pxpc, dtype=np.int32)
	
	px_margin = 3 * pen.px_radius
	
	print >>sys.stderr, "px_margin\t\t", px_margin
	
	px_box[0] -= px_margin
	px_box[1] += px_margin
	px_box[2] += px_margin
	px_box[3] -= px_margin
		
	width = int(px_box[2] - px_box[0])
	height = int(px_box[1] - px_box[3])
	
	pen.px_box = px_box
	
	print >>sys.stderr, "width\t\t\t", width
	print >>sys.stderr, "height\t\t\t", height
	
	print >>sys.stderr, "px_box\t\t\t", px_box
	
	pen.px_margin = px_margin
	pen.px_orig_x = px_box[0]
	pen.px_orig_y = px_box[3]
	
	return im.new('L', (width, height))
