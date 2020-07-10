import sys

class Stack:
	# actually a linked list in disguise
	def __init__(self, isNested, parent):
		self.children = [] # children[-1] is the top of the stack
		self.isNested = isNested
		self.parent = parent

	def __len__(self):
		return len(self.children)
	
	def __repr__(self):
		return "<Stack: children: {}, parent: {}>".format(self.children, self.parent)

	def push(self, ele):
		self.children.append(ele)
	
	def pop(self):
		return self.children.pop()
	
class Cursor:
	def __init__(self):
		self.left = Stack(0, False)
		self.right = Stack(0, False)
		self.active = self.left
		self.inactive = self.right
		self.leftDepth = 0
		self.rightDepth = 0
		self.currentDepth = self.leftDepth
		self.currentStack = self.active
		self.inactiveStack = self.inactive
	
	def incrementDepth(self):
		if self.active == self.left:
			self.leftDepth += 1
			self.currentDepth = self.leftDepth
		else:
			self.rightDepth += 1
			self.currentDepth = self.rightDepth
	
	def decrementDepth(self):
		if self.active == self.left:
			self.leftDepth -= 1
			self.currentDepth = self.leftDepth
		else:
			self.rightDepth -= 1
			self.currentDepth = self.rightDepth

	def new(self):
		self.active.push(Stack(True, self))
	
	def pop(self):
		self.active.pop()
	
	def enter(self):
		self.currentStack = self.currentStack.children[-1]
		self.incrementDepth()
	
	def exit(self):
		self.currentStack = self.currentStack.parent
		self.decrementDepth()
	
	def warp(self):
		if self.active == self.left:
			self.active = self.right
			self.inactive = self.left
		else:
			self.active = self.left
			self.inactive = self.right
		self.currentStack = self.active
		self.inactiveStack = self.inactive
	
	def send(self):
		self.inactive.push(self.active.pop())
	
	def read(self):
		new = Stack(True, self.active)
		num = ord(sys.stdin.read(1))
		for i in range(num):
			new.push(Stack(True, new))
		self.active.push(new)
	
	def write(self):
		print(chr(len(self.active.pop())), end="")
