"""
Created on Tue Nov 23 10:05:58 2021

@author: rhyseshelman
"""
class DES:
	# Permutation/translation table for DES
	pc1 = [
		56, 48, 40, 32, 24, 16, 8, 0,
		57, 49, 41, 33, 25, 17, 9, 1,
		58, 50, 42, 34, 26, 18, 10, 2,
		59, 51, 43, 35, 62, 54, 46, 38,
		30, 22, 14, 6, 61, 53, 45, 37,
		29, 21, 13, 5, 60, 52, 44, 36,
		28, 20, 12, 4, 27, 19, 11, 3]

	# Left rotations of pc1
	left_rotations = [
		1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

	# Permutation table for subkeys
	pc2 = [
		13, 16, 10, 23, 0, 4, 2, 27,
		14, 5, 20, 9, 22, 18, 11, 3,
		25, 7, 15, 6, 26, 19, 12, 1,
		40, 51, 30, 36, 46, 54, 29, 39,
		50, 44, 32, 47, 43, 48, 38, 55,
		33, 52, 45, 41, 49, 35, 28, 31]

	# Initial permutation
	ip = [
		57, 49, 41, 33, 25, 17, 9, 1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8, 0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6]

	# Expansion table which turns 32-bit blocks into 48 bits
	expansion = [
		31, 0, 1, 2, 3, 4, 3, 4,
		5, 6, 7, 8, 7, 8, 9, 10,
		11, 12, 11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20, 19, 20,
		21, 22, 23, 24, 23, 24, 25, 26,
		27, 28, 27, 28, 29, 30, 31, 0]

	# S-boxes
	sbox = [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
	]

	# Permutation function used on S-box outputs
	perm = [
		15, 6, 19, 20, 28, 11, 27, 16,
		0, 14, 22, 25, 4, 17, 30, 9,
		1, 7, 23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10, 3, 24]

	# Final permutation a.k.a. IP^-1
	fp = [
		39, 7, 47, 15, 55, 23, 63, 31,
		38, 6, 46, 14, 54, 22, 62, 30,
		37, 5, 45, 13, 53, 21, 61, 29,
		36, 4, 44, 12, 52, 20, 60, 28,
		35, 3, 43, 11, 51, 19, 59, 27,
		34, 2, 42, 10, 50, 18, 58, 26,
		33, 1, 41, 9, 49, 17, 57, 25,
		32, 0, 40, 8, 48, 16, 56, 24]

	def __init__(self, key):
		self.left = []
		self.right = []
		self.subkeys = [ [0] * 48 ] * 16
		self.final = []
		self.key = self._stringToBytes(key)
		self.__createSubkeys()

	def _stringToBytes(self, data):
		if isinstance(data, str):
			data = str.encode(data)
		return data

	# Converts strings to bit-lists
	def __stringToBitList(self, data):
		l = len(data) * 8
		result = [0] * l
		pos = 0
		for c in data:
			i = 7
			while i >= 0:
				if c & (1 << i) != 0:
					result[pos] = 1
				pos += 1
				i -= 1

		return result

	# Converts bit-lists to strings
	def __bitListToString(self, data):
		result = []
		pos = 0
		c = 0
		while pos < len(data):
			c += data[pos] << (7 - (pos % 8))
			if (pos % 8) == 7:
				result.append(c)
				c = 0
			pos += 1
		
		return bytes(result)

	# Pads data using PKCS5 padding
	def _padData(self, data):
		l = 8 - (len(data) % 8)
		data += bytes([l] * l)
		return data
	
	# Unpads data
	def _unpadData(self, data):
		l = data[-1]
		data = data[:-l]
		return data
	
	# Simple permute function that takes a block of data and one of the above permutation tables as inputs
	def __permute(self, table, block):
		return list(map(lambda x: block[x], table))

	# Creates the subkeys for each of the 16 rounds
	def __createSubkeys(self):
		key = self.__permute(DES.pc1, self.__stringToBitList(self.key))

		self.left = key[:28]
		self.right = key[28:]

		i = 0
		while i < 16:
			j = 0
			while j < DES.left_rotations[i]:
				self.left.append(self.left[0])
				del self.left[0]

				self.right.append(self.right[0])
				del self.right[0]

				j += 1
			
			self.subkeys[i] = self.__permute(DES.pc2, self.left + self.right)

			i += 1

	# Encrypt/decrypt a single block of data
	def __blockCrypt(self, block, crypt_type):
		block = self.__permute(DES.ip, block)
		self.left = block[:32]
		self.right = block[32:]

		if crypt_type == 'encrypt':
			iteration = 0
			iteration_adj = 1

		else:
			iteration = 15
			iteration_adj = -1

		# Rounds of encryption/decryption
		i = 0
		while i < 16:
			temp_right = self.right[:]

			self.right = self.__permute(DES.expansion, self.right)
			self.right = list(map(lambda x, y: x ^ y, self.right, self.subkeys[iteration]))
			A = [self.right[:6], self.right[6:12], self.right[12:18],self.right[18:24],
				self.right[24:30], self.right[30:36], self.right[36:42], self.right[42:]]

			j = 0
			A_n = [0] * 32
			pos = 0
			while j < 8:
				# Offsets
				r = (A[j][0] << 1) + A[j][5]
				s = (A[j][1] << 3) + (A[j][2] << 2) + (A[j][3] << 1) + A[j][4]

				# S-box value
				t = DES.sbox[j][(r << 4) + s]

				A_n[pos] = (t & 8) >> 3
				A_n[pos + 1] = (t & 4) >> 2
				A_n[pos + 2] = (t & 2) >> 1
				A_n[pos + 3] = t & 1

				pos += 4
				j += 1
			
			# Permute A[1] through A[8]
			self.right = self.__permute(DES.perm, A_n)

			# XOR with with left[i - 1]
			self.right = list(map(lambda x, y: x ^ y, self.right, self.left))

			# Swap, so left[i] becomes right[i - 1]
			self.left = temp_right

			i += 1
			iteration += iteration_adj

		self.final = self.__permute(DES.fp, self.right + self.left)
		return self.final

	# Encrypt/decrypt data
	def crypt(self, data, crypt_type):
		i = 0
		result = []

		while i < len(data):
			block = self.__stringToBitList(data[i:i+8])

			processed_block = self.__blockCrypt(block, crypt_type)
			
			result.append(self.__bitListToString(processed_block))

			i += 8
		
		return bytes.fromhex('').join(result)
	
	# DES encryption
	def encrypt(self, data):
		data = self._stringToBytes(data)
		data = self._padData(data)
		return self.crypt(data, 'encrypt')

	# DES decryption
	def decrypt(self, data):
		data = self._stringToBytes(data)
		data = self.crypt(data, 'decrypt')
		return(self._unpadData(data))

class TripleDES(DES):
	# 24-byte key input
	def __init__(self, key):
		self.key1 = DES(key[:8])
		self.key2 = DES(key[8:16])
		self.key3 = DES(key[16:])

	# Triple DES encryption
	def encrypt(self, data):
		data = self._stringToBytes(data)
		data = self._padData(data)
		data = self.key1.crypt(data, 'encrypt')
		data = self.key2.crypt(data, 'decrypt')
		return self.key3.crypt(data, 'encrypt')

	# Triple DES decryption
	def decrypt(self, data):
		data = self.key3.crypt(data, 'decrypt')
		data = self.key2.crypt(data, 'encrypt')
		data = self.key1.crypt(data, 'decrypt')
		return self._unpadData(data).decode('ascii')