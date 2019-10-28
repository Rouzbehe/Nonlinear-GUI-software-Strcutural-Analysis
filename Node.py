class Node:
 i = 0
 def __init__(self,x,y):
  self.x=x
  self.y=y
  self.xd=0
  self.yd=0
  Node.i = Node.i+1
  self.i = Node.i
 def getX(self):
  return  self.x

 def getY(self):
  return self.y

 def getNum(self):
  return self.i

 def inputX(self,x):
  self.xd=x

 def inputY(self,y):
  self.yd=y

 def getnewX(self):
  return self.xd

 def getnewY(self):
  return self.yd

