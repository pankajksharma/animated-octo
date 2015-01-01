
class Chua(object):
	def __init__(self, x0, y0, z0, alpha, beta, gamma, m0, m1):
		self._x0 = x0
		self._y0 = y0
		self._z0 = z0 
		self._alpha = alpha
		self._beta = beta
		self._gamma = gamma
		self._m0 = m0
		self._m1 = m1
		self._x = x0
		self._y = y0
		self._z = z0

	def _geth(self):
		h = self._m1*self._x + 0.5*(self._m0 - self._m1)*(abs(self._x+1)-abs(self._x-1))
		return h

	def _getx(self, h):
		x = self._alpha*(self._y - self._x - h)
		return x

	def _gety(self):
		y = self._x - self._y + self._z
		return y

	def _getz(self):
		z = -self._beta*self._y - self._gamma*self._z
		return z

	def reset(self):
		self._x = self._x0
		self._y = self._y0
		self._z = self._z0

	def iterate(self, n=1):
		for i in range(n):
			h = self._geth()
			x = self._getx(h)
			y = self._gety()
			z = self._getz()
			self._x, self._y, self._z = x, y, z
		return self._x, self._y, self._z
