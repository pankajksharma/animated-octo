class SkewTentMap(object):
	"""Class for implementing skew tent map."""
	def __init__(self, stm_iv, stm_gf):
		self.stm_iv = stm_iv
		self.stm_gf = stm_gf
		self.present_value = stm_iv

	def reset(self):
		self.present_value = self.stm_iv

	def iterate(self, n=1):
		for i in range(n):
			if self.present_value >= 0 and self.present_value < self.stm_gf:
				self.present_value /= self.stm_gf
			else:
				self.present_value = (1.0-self.present_value) / (1.0-self.stm_gf)
		return self.present_value