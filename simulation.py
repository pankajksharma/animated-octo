
import cv2, numpy as np
from huang import *


def printmat(mat):
	(h,w) = mat.shape
	print ''' size 12{ left ( matrix {'''
	for i in range(h):
		for j in range(w):
			print '"%d" {}' %mat[i][j],
			if j != w-1:
				print '#',
		if i != h-1:
			print '##'
	print '''}  right )} {}'''

def printbinmat(mat):
	(h,w) = mat.shape
	print ''' size 12{ left ( matrix {'''
	for i in range(h):
		for j in range(w):
			s = ""
			p = int(mat[i][j])
			while p > 0:
				s = str(p%2)+s
				p /= 2
			print '"%08s" {}' %s,
			if j != w-1:
				print '#',
		if i != h-1:
			print '##'
	print '''}  right )} {}'''


P = [[102, 57, 43], [69, 29, 93], [21,167, 82]]

p = np.array(P)
# print p
printmat(p)
printbinmat(p)
h = HuangEnc(p)
e = h.encrypt()
printmat(e)
print e
printbinmat(e)
h = HuangDec(e)
print h.decrypt()


#Constants for attack. Only change image name.
image_name = 'baboon_small.png'
enc_image_name = 'baboon_small_enc.png'
ret_img_name = 'baboon_small_from_attack.png'

P = [[102, 57, 43], [69, 29, 93], [21,167, 82]]

p = np.array(P)
print p
# printmat(p)
# printbinmat(p)
h = HuangEnc(p)
e = h.encrypt()
print e
# printmat(e)
# printbinmat(e)
# h = HuangDec(e)
# print h.decrypt()

img = e # cv2.imread(enc_image_name, 0)
orig_img = p # cv2.imread(image_name, 0)
shape = img.shape
(h,w) = shape

pixel_vals = [128, 64, 32, 16, 8, 4, 2, 1]

def get_pos(enc_img):
	non_zero = np.transpose(np.nonzero(enc_img))[0]
	val = enc_img[non_zero[0]][non_zero[1]]
	return non_zero[0]+1, non_zero[1]+1, pixel_vals.index(val)+1

poses = []
mposes = {}

for i in range(h):
	for j in range(w):
		for k in range(len(pixel_vals)):
			print((i+1,j+1,k+1))
			mod_zero = np.zeros(shape, dtype='uint8')
			mod_zero[i][j] = pixel_vals[k]
			huang = HuangEnc(mod_zero)
			enc_img = huang.encrypt()
			pos = get_pos(enc_img)
			# poses.append((pos))
# 			print(pos)
			poses.append((i+1,j+1,k+1))
			mposes[(i+1,j+1,k+1)] = pos
print
print
for p in poses:
	print mposes[p]
