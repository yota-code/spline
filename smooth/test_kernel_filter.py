#!/usr/bin/env python3

import numpy as np
import png


def load_png(path) :
	width, height, image, info = png.Reader(path).read()
	nb_layer = 1 if info['greyscale'] else 3
	nb_layer += 1 if info['alpha'] else 0
	image = np.vstack(image)[:,:,np.newaxis].reshape(height, width, nb_layer)
	return width, height, image, info
	

	
width, height, rgb, info = load_png("hel_vinci.png")

red = rgb[:,:,0]
print(red.shape)
#s = list()
#for i in u[2] :
#	s.append(i)
#print(type(i))
#print(len(i)/3)
#
#print(len(s))

##.reshape(u[0], u[1])
#
w = png.Writer(width, height, greyscale=True)
with open("hel_red.png", 'wb') as fid :
	w.write(fid, rgb[:,:,0])
	
with open("hel_green.png", 'wb') as fid :
	w.write(fid, rgb[:,:,1])
	
with open("hel_blue.png", 'wb') as fid :
	w.write(fid, rgb[:,:,2])	
