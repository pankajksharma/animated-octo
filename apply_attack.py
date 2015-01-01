from huang import *
import numpy as np, cv2

#Constants for attack. Only change image name.
image_name = 'baboon_small.png'
enc_image_name = 'baboon_small_enc.png'
ret_img_name = 'baboon_small_from_attack.png'

img = cv2.imread(enc_image_name, 0)
orig_img = cv2.imread(image_name, 0)
shape = img.shape
(h,w) = shape

pixel_vals = [128, 64, 32, 16, 8, 4, 2, 1]

def get_pos(enc_img):
	non_zero = np.transpose(np.nonzero(enc_img))[0]
	val = enc_img[non_zero[0]][non_zero[1]]
	return non_zero[0], non_zero[1], pixel_vals.index(val)

poses = []

for i in range(h):
	for j in range(w):
		for k in range(len(pixel_vals)):
			mod_zero = np.zeros(shape, dtype='uint8')
			mod_zero[i][j] = pixel_vals[k]
			huang = HuangEnc(mod_zero)
			enc_img = huang.encrypt()
			pos = get_pos(enc_img)
			poses.append((pos))
print len(poses)

ret_img = np.zeros(h*w, dtype='uint8')
orig_img = np.reshape(orig_img, h*w)

s,c,n = 0,0,0

for pos in poses:
	(i,j,k) = pos
	bit = 0 if (img[i][j]&pixel_vals[k]) == 0 else 1
	s += bit*pixel_vals[c%8]
	c += 1
	if c%8 == 0:
		print s, orig_img[n],n
		ret_img[n] = s
		s = 0
		n += 1

ret_img = np.resize(ret_img, shape)
cv2.imwrite(ret_img_name, ret_img)
