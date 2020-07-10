import sys

class Cursor:
	def __init__(self):
		self.left = []
		self.right = []
		self.current = self.left
		self.other = self.right
		self.active = self.left
		self.inactive = self.right
		self.activeDepth = 0
		self.otherDepth = 0
	
	def _push(self, ele):
		self.current.append(ele)
	
	def _pop(self):
		return self.current.pop()
	
	def new(self):
		self._push([])
	
	def pop(self):
		self._pop()
	
	def enter(self):
		self.activeDepth += 1
		self.active = self.current
		i = self.activeDepth
		while i > 0:
			for e in self.active:
				if len(e):
					self.active = e
					break
			i -= 1
	
	def exit(self):
		self.activeDepth -= 1
		self.active = self.current
		i = self.activeDepth
		while i > 0:
			for e in self.active:
				if len(e):
					self.active = e
					break
			i -= 1
	
	def warp(self):
		self.current, self.other = self.other, self.current
		self.active, self.inactive = self.inactive, self.active
		self.activeDepth, self.otherDepth = self.otherDepth, self.activeDepth
	
	def send(self):
		self.inactive.append(self.active.pop())
	
	def read(self):
		n = []
		for i in range(ord(sys.stdin.read(1))):
			n.append([])
		self.active.append(n)
	
	def write(self):
		print(chr(len(self.active.pop())), end="")