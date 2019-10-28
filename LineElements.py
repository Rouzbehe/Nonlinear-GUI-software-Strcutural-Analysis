from math import cos,sin,sqrt,atan2
import numpy as np
class LineElement:
 
 def __init__(self, nodeI, nodeJ):
  self.nodeI=nodeI
  self.nodeJ=nodeJ

 def getLength(self):
  
  self.L=sqrt((nodeJ.getX()-nodeI.getX())**2+((nodeJ.getY()-nodeI.getY())**2))
  return self.L

 def getNodeI(self):
  return self.nodeI

 def getNodeJ(self):
  return self.nodeJ
 
 def getAngle(self):

  self.T=atan2((self.nodeJ.getY()-self.nodeI.getY()),(self.nodeJ.getX()-self.nodeI.getX()))
  return self.T
 
 def getCoordinateTransform(self):
  if len(self.getLocalDofList())==4:
   
   i=self.getLocalDofList().index('UXI')
   j=self.getLocalDofList().index('UYI')
   I=self.getLocalDofList().index('UXJ')
   J=self.getLocalDofList().index('UYJ')
   T=np.zeros((4,4))
   
   
   T[i,i]=cos(self.getAngle())
   T[i,j]=-sin(self.getAngle())
   T[j,j]=cos(self.getAngle())
   T[j,i]=sin(self.getAngle())
  
   T[I,I]=cos(self.getAngle())
   T[I,J]=-sin(self.getAngle())
   T[J,J]=cos(self.getAngle())
   T[J,I]=sin(self.getAngle())
  
  else:
 
   i=self.getLocalDofList().index('UXI')
   j=self.getLocalDofList().index('UYI')
   I=self.getLocalDofList().index('UXJ')
   J=self.getLocalDofList().index('UYJ')
   k=self.getLocalDofList().index('RI')
   K=self.getLocalDofList().index('RJ')
   T=np.zeros((6,6))
 
 
   T[i,i]=cos(self.getAngle())
   T[i,j]=-sin(self.getAngle())
   T[j,j]=cos(self.getAngle())
   T[j,i]=sin(self.getAngle())
   T[k,k]=1
   T[K,K]=1
   T[I,I]=cos(self.getAngle())
   T[I,J]=-sin(self.getAngle())
   T[J,J]=cos(self.getAngle())
   T[J,I]=sin(self.getAngle())
 

  return T
   
  
 def getGlobalMatrix(self,localMat):
   T=self.getCoordinateTransform()
   M=np.dot(T,localMat)
   tr=np.transpose(T)
   MM=np.dot(M,tr)

   return MM
 def getDofList(self):
    nodI=self.nodeI
    nodJ=self.nodeJ
    List=self.getLocalDofList()
    ID_i=nodI.getNum()
    ID_j=nodJ.getNum()
    for i in range(0,len(List)):
      if List[i]=='UXI':
         List[i]='UX%s'%str(ID_i)
      elif List[i]=='UXJ':
         List[i]='UX%s'%str(ID_j)
      elif List[i]=='UYI':
         List[i]='UY%s'%str(ID_i)
      elif List[i]=='UYJ':
         List[i]='UY%s'%str(ID_j)
      elif List[i]=='RJ':
         List[i]='R%s'%str(ID_j)
      elif List[i]=='RI':
         List[i]='R%s'%str(ID_i)
    return List
 
 def getMassMatrix(self):
   M =self.getGlobalMatrix(self.getLocalMassMatrix())
   return M
 def getStiffnessMatrix(self):
 
   K =self.getGlobalMatrix(self.getLocalStiffnessMatrix())
   return K


class BeamColumnElement(LineElement):

 def __init__(self, EA, EI, rhoA, nodeI, nodeJ):
  from math import sqrt
  self.EI=EI
  self.EA=EA
  self.rhoA=rhoA
  self.nodeI=nodeI
  self.nodeJ=nodeJ
  self.L=sqrt((nodeJ.getX()-nodeI.getX())**2+((nodeJ.getY()-nodeI.getY())**2))
  
 def getLocalDofList(self):
  nodI=self.nodeI
  nodJ=self.nodeJ
  ID_i=nodI.getNum()
  ID_j=nodJ.getNum()
  return ['UYI', 'RI', 'UYJ', 'RJ','UXI','UXJ']
 
 def getLocalMassMatrix(self):
   import numpy as np
   from math import sqrt
   L = self.L
   Me=self.rhoA*L/420.*np.matrix([[156, 22*L, 54, -13*L],[22*L, 4*L**2, 13*L, -3*L**2],[54,13*L, 156, -22*L],[-13*L,-3*L**2,-22*L,4*L**2]])

   M=np.zeros((6,6))
   M[:4,:4]=Me
   M[4:6,4:6]=self.rhoA*L/6.*np.matrix([[2,1],[1,2]])
   #print 'noo'
  # print M
   return M
 def getLocalStiffnessMatrix(self):
   import numpy as np
   from math import sqrt
   L = self.L
   Ke=2*self.EI/L**3.*np.matrix([[6, 3*L,-6, 3*L],[3*L, 2*L**2, -3*L, L**2],[-6, -3*L, 6, -3*L],[3*L, L**2, -3*L, 2*L**2]])
   K=np.zeros((6,6))
   K[:4,:4]=Ke
   K[4:6,4:6]=self.EA/L*np.matrix([[1,-1],[-1,1]])
   return K

class RodElement(LineElement):
 def __init__(self, EA, rhoA, nodeI, nodeJ):
  from math import sqrt
  self.EA=EA
  self.rhoA=rhoA
  self.nodeI=nodeI
  #print type(nodeI)
  self.nodeJ=nodeJ
  self.L=sqrt((nodeJ.getX()-nodeI.getX())**2+((nodeJ.getY()-nodeI.getY())**2))

 def getLocalDofList(self):
  nodI=self.nodeI
  #print type(nodI)
  nodJ=self.nodeJ
  #print type(nodJ)
  ID_i=nodI.getNum()
  ID_j=nodJ.getNum()
  return ['UXI', 'UYI', 'UXJ', 'UYJ']
 
 def getLocalMassMatrix(self):
  import numpy as np
  from math import sqrt
  L = self.L
  M=self.rhoA*L/6.*np.matrix([[2, 0, 1, 0],[0, 2, 0, 1],[1,0, 2, 0],[0,1,0,2]])
 
  return M
 def getLocalStiffnessMatrix(self):
  import numpy as np
  from math import sqrt
  L = self.L
  K=self.EA/L*np.matrix([[1, 0,-1, 0],[0, 0, 0, 0],[-1, 0, 1, 0],[0, 0, 0, 0]])

  return K
