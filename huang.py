from skewtentmap import *
import cv2, numpy as np

class HuangBase(object):
	def __init__(self, x0, y0, z0, alpha, beta, gamma, m0, m1):
		# self.chua = Chua(x0, y0, z0, alpha, beta, gamma, m0, m1)
		self._xmap = SkewTentMap(x0, alpha)
		self._ymap = SkewTentMap(y0, beta)
		self._zmap = SkewTentMap(z0, gamma)

	def iterate(self, img):
		(h,w) = img.shape
		self.x = np.zeros((h,w))
		self.y = np.zeros((h,w))
		self.z = np.zeros(8*h*w)

		for i in range(h):
			for j in range(w):
				self.x[i][j] = self._xmap.iterate()
				self.y[i][j] = self._ymap.iterate()

		for i in range(8*h*w):
				self.z[i] = self._zmap.iterate()
		# print self.x.tolist(),self.y.tolist(),self.z.tolist()

	def rotate_rows(self, img, mat):
		(h,w) = img.shape
		for i in range(h):
			uimg_row = img[i]
			mat_row = mat[i][:].tolist()
			omat_row = mat_row[:]
			omat_row.sort()
			# print omat_row, mat_row
			hash_map = {}
			for j in range(len(omat_row)):
				hash_map[omat_row[j]] = j
			t_vector = [hash_map[x] for x in mat_row]
			oimg_row = [uimg_row[t] for t in t_vector]
			img[i] = oimg_row
		return img

	def rotate_cols(self, img, mat):
		(h,w) = img.shape
		img = np.reshape(img, (w,h))
		img = self.rotate_rows(img, mat)
		img = np.reshape(img, (h,w))
		return img

	def grey_level_enc(self, img, mat):
		(h,w) = img.shape
		bin_img = np.zeros((h,w,8))
		for i in range(h):
			for j in range(w):
				for k in range(8)[::-1]:
					bin_img[i][j][k] = 0 if (img[i][j] & 2**k) == 0 else 1
		bin_img = np.reshape(bin_img, 8*h*w)
		hash_map = {}
		mat = mat[:].tolist()
		s_mat = mat[:]
		s_mat.sort()
		hash_map = {}
		# print mat, s_mat
		for i in range(len(mat)):
			hash_map[mat[i]] = i
		t_vector = [hash_map[x] for x in s_mat]
		new_bin_img = [ bin_img[t] for t in t_vector]
		new_bin_img = np.asarray(new_bin_img)
		new_bin_img = np.reshape(new_bin_img, (h,w,8))
		new2d = np.zeros((h,w))
		for i in range(h):
			for j in range(w):
				s = 0.0
				for k in range(8)[::-1]:
					s += 2**k*new_bin_img[i][j][k]
				new2d[i][j] = s
		return new2d

class HuangEnc(HuangBase):
	def __init__(self, img, x0=0.1, y0=0.6, z0=0.1, alpha=0.45, beta=0.78,
	gamma=0.385, m0=-1.27, m1=-0.68):
		HuangBase.__init__(self, x0, y0, z0, alpha, beta, gamma, m0, m1)
		if isinstance(img, str):
			self.A = cv2.imread(img, 0)
		else:
			self.A = img

	def encrypt(self, out_file_name=None):
		self.iterate(self.A)
		enc_img = self.rotate_cols(self.A, self.x)
		enc_img = self.rotate_rows(enc_img, self.y)
		enc_img = self.grey_level_enc(enc_img, self.z)
		if out_file_name:
			cv2.imwrite(out_file_name, enc_img)
		return enc_img


class HuangDec(HuangBase):
	def __init__(self, img, x0=0.1, y0=0.6, z0=0.1, alpha=10.0, beta=14.78,
	gamma=0.0385, m0=-1.27, m1=-0.68):
		HuangBase.__init__(self, x0, y0, z0, alpha, beta, gamma, m0, m1)
		if isinstance(img, str):
			self.A = cv2.imread(img, 0)
		else:
			self.A = img

	def decrypt(self, out_file_name=None):
		pass


