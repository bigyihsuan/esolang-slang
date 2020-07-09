import sys

class Stack:
	# actually a linked list in disguise
	def __init__(self, depth, parent):
		self.children = [] # children[-1] is the top of the stack
		self.depth = depth
		self.parent = parent
	
	def push(self, ele):
		self.children.append(ele)
	
	def pop(self):
		return self.children.pop()
	
class Cursor:
	def __init__(self):
		self.left = Stack(0, None)
		self.right = Stack(0, None)
		self.active = self.left
		self.inactive = self.right
		self.currentDepth = 0
	
	def new(self):
		self.active.push(Stack(self.depth+1, self))
	
	def pop(self):
		self.active.pop()
	
	def enter(self):
		self.active = self.active.children[-1]
		self.currentDepth += 1
	
	def exit(self):
		self.active = self.active.parent
		self.currentDepth -= 1
	
	def warp(self):
		if self.active == self.left:
			self.active = self.right
			self.inactive = self.left
		else:
			self.active = self.left
			self.inactive = self.right
	
	def send(self):
		self.inactive.push(self.active.pop())
	
	def read(self):
		new = Stack(self.currentDepth+1, self.active)
		num = ord(sys.stdin.buffer.read1())
		for i in range(num):
			new.push(Stack(new.depth+1, new))
		self.active.push(new)
	
	def write(self):
		out = self.active.pop()
		print(bytes(len(out.children)))
