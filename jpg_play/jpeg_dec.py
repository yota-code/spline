#!/usr/bin/env python3

from pathlib import Path
import struct
import binascii
import sys

from huffman import HuffmanTable

import numpy as np

def dbg_bin(s, title='') :
	sys.stdout.write('\n --- {0}\n'.format(title))
	for n, c in enumerate(s) :
		if (n % 16) == 0 :
			if n != 0 :
				sys.stdout.write('\n')
			sys.stdout.write('{0:04X}\t'.format(n))
		sys.stdout.write("{0:02X} ".format(c))
	sys.stdout.write('\n --- length: {0}\n\n'.format(len(s)))

def read_struct(fmt, fid) :
	s = struct.Struct(fmt)
	l = s.size
	b = fid.read(l)
	return s.unpack(b)
	
	
class JpegReader() :
	
	def get_marker(self) :
		return binascii.b2a_hex(self.fid.read(2)).decode('utf8').upper()
		
	def get_block(self, title='') :
		(length,) = struct.unpack('!H', self.fid.read(2))
		block = self.fid.read(length - 2)
		dbg_bin(block, title)
		return block

	def __init__(self, pth) :
		self.pth = pth
		
		self.quantization = dict()
		self.huffman_table = dict()		
		with Path(pth).open('rb') as self.fid :
			while True :
				p = self.get_marker()
				if not p :
					break
				getattr(self, "_block_{0}".format(p))()
				
	def _block_FFD8(self) :
		print(" --- FFD8: start of image")
		
	def _block_FFE0(self) :
		data = self.get_block("FFE0: JPEG File Interchange Format")
		
		m = dict()
		m['ident'] = struct.unpack_from('5B', data, 0)
		m['version'] = struct.unpack_from('2B', data, 5)
		m['unit'] = struct.unpack_from('B', data, 7)
		m['density'] = struct.unpack_from('!2H', data, 8)
		x, y = struct.unpack_from('2B', data, 12)
		m['thumbnail'] = np.fromstring(self.fid.read(3 * x * y), dtype=np.uint8)
		
		self.jfif = m
		
	def _block_FFDB(self) :
		data = self.get_block("FFDB: quantization table")
		ident = struct.unpack_from('B', data, 0)
		matrix = np.fromstring(data[1:65], dtype=np.uint8).reshape((8,8))
		self.quantization[ident] = matrix
		
	def _block_FFC0(self) :
		data = self.get_block("FFC0: start of frame")
		
	def _block_FFC4(self) :
		data = self.get_block("FFDB: huffman table")
		ident = unpack('B', data, 0)
		depth = np.fromstring(data[1:17], dtype=np.uint8)
		print(depth.sum(), 17+depth.sum(), len(data))
		value = np.fromstring(data[17:17+depth.sum()], dtype=np.uint8)
		print(len(value))
		self.huffman_table[ident] = HuffmanTable(depth, value)
		
	def _block_FFDA(self) :
		start = fid.tell()
		b = fid.read(1)
		while b :
			if b == '\xFF' :
				n = struct.unpack('B', fid.read(1))
				if n == 0xFF :
					continue
				elif 0xD0 <= n <= 0xD7 :
					continue
				else :
					breaknode
			b = fid.read(1)
		stop = fid.tell() - 2
		fid.seek(start)
		return fid.read(stop - start)

		
		
def unpack(fmt, buf, pos=0) :
	if isinstance(buf, bytes) :
		s = struct.Struct(fmt)
		b = buf[pos:pos+s.size]
		return s.unpack(b)
	
def read_data(fid) :
	(length,) = struct.unpack('!H', fid.read(2))
	return fid.read(length - 2)
	

	

	
def parse_block_FFD9(fid) :
	print("End of Image")
	




	
def get_block(fid, marker=None) :
	pos = fid.tell()
	m = fid.read(2)
	if marker is not None and m != marker :
		fid.seek(pos)
		raise ValueError("marker does not match {0!r} ≠ {1!r}".format(marker, m))
	(length,) = struct.unpack('!H', fid.read(2))
	block = fid.read(length - 2)
	return block
	
def parse_jpeg(fid) :
	while True :
		marker = binascii.b2a_hex(fid.read(2)).decode('utf8').upper()
		if marker :
			print('>', marker)
			globals()["parse_block_{0}".format(marker)](fid)
		else :
			break
				
if __name__ == '__main__' :
	import sys
	
	u = JpegReader(Path(sys.argv[1]))
		
