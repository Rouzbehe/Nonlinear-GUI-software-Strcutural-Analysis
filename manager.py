import Tkinter,LineElements,Node,lineMesh,systemMatrices

NODES=[]
ELEMENTS=[]
CONSTRAINTS=[]
FREQUENCY=[]
SHAPES=[]
DOFDICT={}

def PLOTNODES():
    import matplotlib.pyplot as plt
    plt.figure('Project')
    plt.close()
    plt.figure('Project')
    for node in NODES:
        plt.plot(node.getX(),node.getY(),'.')
        plt.text(node.getX(),node.getY(),node.getNum())
    plt.show(block=False)


def PLOTSTRUCTURE():
    import matplotlib.pyplot as plt
    import numpy as np
    plt.figure('Project')
    plt.close()
    plt.figure('Project')
    for element in ELEMENTS:
        I = element.getNodeI()
        J = element.getNodeJ()
        plt.plot(np.linspace(I.getX(),J.getX(),num=10),np.linspace(I.getY(),J.getY(),num=10))
    for node in NODES:
        plt.plot(node.getX(),node.getY(),'.')
        plt.text(node.getX(),node.getY(),node.getNum())
    plt.show(block=False)

class GUI(Tkinter.Tk):
    def __init__(self,parent=None):
        Tkinter.Tk.__init__(self,parent)
        self._parent = parent
        self.initialize()


    def initialize(self):
        self.grid()
        self.title('Master Menu')

        title = Tkinter.Label(self, text = 'Master Menu')
        title.grid(column=0, row=0, sticky='EW')

        Nodes = Tkinter.Button(self, text='Create Nodes',command=self.startNodes)
        Nodes.grid(column=0, row=1, sticky='EW')

        Element = Tkinter.Button(self, text='Create Elements',command=self.startElement)
        Element.grid(column=0, row=2, sticky='EW')

        Constraint = Tkinter.Button(self, text='Add Constraints',command=self.startConstraint)
        Constraint.grid(column=0, row=3, sticky='EW')

        Solve = Tkinter.Button(self, text='Solve for modes',command=self.startSolve)
        Solve.grid(column=0, row=4, sticky='EW')

        Results = Tkinter.Button(self, text='Results',command=self.startResults)
        Results.grid(column=0, row=5, sticky='EW')



    def startNodes(self):
        NodesWin()

    def startElement(self):
        ElementsWin()

    def startSolve(self):
        SolveWin()

    def startConstraint(self):
        ConstraintWin()

    def startResults(self):
        ResultsWin()




class NodesWin(Tkinter.Tk):
    def __init__(self,parent=None):
        Tkinter.Tk.__init__(self,parent)
        self.initialize()

    def initialize(self):
        self.grid()
        self.title('Nodes')

        title = Tkinter.Label(self, text = 'Enter Nodal Co-ordinates')
        title.grid(column=0, row=0,sticky='EW')

        x =Tkinter.Label(self,text='X')
        x.grid(column=0,row=1,sticky='EW')
        self.x=Tkinter.Entry(self)
        self.x.grid(column=1,row=1,sticky='EW')

        y =Tkinter.Label(self,text='Y')
        y.grid(column=0,row=2,sticky='EW')
        self.y=Tkinter.Entry(self)
        self.y.grid(column=1,row=2,sticky='EW')

        click=Tkinter.Button(self,text='Create Nodes',command=self.click)
        click.grid(column=0,row=3,sticky='EW')

    def click(self):
        NODES.append(Node.Node(float(self.x.get()),float(self.y.get())))
        print NODES
        PLOTNODES()


class ElementsWin(Tkinter.Tk):
    def __init__(self,parent=None):
        Tkinter.Tk.__init__(self,parent)
        self.initialize()

    def initialize(self):
        self.grid()
        self.title('Create Elements')


        title= Tkinter.Label(self, text = 'Enter Material properties')
        title.grid(column=0, row=0,sticky='EW')

        E = Tkinter.Label(self, text = 'Modulus of Elasticity')
        E.grid(column=0, row=1, sticky='EW')
        self.E=Tkinter.Entry(self)
        self.E.grid(column=1,row=1,sticky='EW')

        d = Tkinter.Label(self, text = 'Density')
        d.grid(column=0, row=2, sticky='EW')
        self.d=Tkinter.Entry(self)
        self.d.grid(column=1,row=2,sticky='EW')


        SP = Tkinter.Label(self, text = 'Section Properties')
        SP.grid(column=0, row=4, sticky='EW')

        A = Tkinter.Label(self, text = 'Area')
        A.grid(column=0, row=5, sticky='EW')
        self.A=Tkinter.Entry(self)
        self.A.grid(column=1,row=5,sticky='EW')

        I = Tkinter.Label(self, text = 'Moment of Inertia')
        I.grid(column=0, row=6, sticky='EW')
        self.I=Tkinter.Entry(self)
        self.I.grid(column=1,row=6,sticky='EW')

        MG = Tkinter.Label(self, text = 'Meshing')
        MG.grid(column=0, row=8, sticky='EW')

        t = Tkinter.Label(self, text = 'Element Type')
        t.grid(column=0, row=9, sticky='EW')
        options = ['Rod','Beam Column']
        self.t = Tkinter.StringVar(self)
        self.t.set('Beam Column')
        menu=Tkinter.OptionMenu(self,self.t,*options)
        menu.grid(column=1,row=9,sticky='EW')


        N = Tkinter.Label(self, text = 'Number of elements between nodes')
        N.grid(column=0, row=10, sticky='EW')
        self.N=Tkinter.Entry(self)
        self.N.grid(column=1,row=10,sticky='EW')

        start = Tkinter.Label(self, text = 'Start Node')
        start.grid(column=0, row=11, sticky='EW')
        self.start=Tkinter.Entry(self)
        self.start.grid(column=1,row=11,sticky='EW')

        self._endnodeLabel = Tkinter.Label(self, text = 'End Node')
        self._endnodeLabel.grid(column=0, row=12, sticky='EW')
        self.end=Tkinter.Entry(self)
        self.end.grid(column=1,row=12,sticky='EW')

        self.click=Tkinter.Button(self,text='Create Elements',command=self.mesh)
        self.click.grid(column=0,row=14,sticky='EW')

    def mesh(self):
        global NODES
        global  ELEMENTS
        for node in NODES:
            if node.getNum()==int(self.start.get()):
                nodeStart=node
            elif node.getNum()==int(self.end.get()):
                nodeEnd=node

        if self.t.get()=='Rod':
            # elemlist,newnodes=lineMesh.meshLine(nodeI,nodeJ,numelems,self.create_beam_elements)
            xStart = nodeStart.getX()
            yStart = nodeStart.getY()
            xEnd = nodeEnd.getX()
            yEnd = nodeEnd.getY()

            dx = (xEnd - xStart)/int(self.N.get())
            dy = (yEnd - yStart)/int(self.N.get())

            # Create a list of nodes from which to define the elements
            nodes = [nodeStart]
            for i in range(1, int(self.N.get())):
                nodes.append(Node.Node(xStart + i*dx, yStart + i*dy))
            nodes.append(nodeEnd)

            # elements = [elementMaker(nodes[i], nodes[i+1]) for i in range(numElements)]
            for i in range(0,len(nodes)-1):
                ELEMENTS.append( LineElements.BeamColumnElement(float(self.E.get())*float(self.A.get()), float(self.E.get())*float(self.I.get()),float(self.d.get())*float(self.A.get()), nodes[i], nodes[i+1]))
            NODES=NODES+nodes[1:-1]

        elif self.t.get()=='Beam Column':
            # elemlist,newnodes=lineMesh.meshLine(nodeI,nodeJ,numelems,self.create_beam_elements)
            xStart = nodeStart.getX()
            yStart = nodeStart.getY()
            xEnd = nodeEnd.getX()
            yEnd = nodeEnd.getY()

            dx = (xEnd - xStart)/int(self.N.get())
            dy = (yEnd - yStart)/int(self.N.get())

            # Create a list of nodes from which to define the elements
            nodes = [nodeStart]
            for i in range(1, int(self.N.get())):
                nodes.append(Node.Node(xStart + i*dx, yStart + i*dy))
            nodes.append(nodeEnd)

            # elements = [elementMaker(nodes[i], nodes[i+1]) for i in range(numElements)]
            for i in range(0,len(nodes)-1):
                ELEMENTS.append( LineElements.BeamColumnElement(float(self.E.get())*float(self.A.get()), float(self.E.get())*float(self.I.get()),float(self.d.get())*float(self.A.get()), nodes[i], nodes[i+1]))

            NODES=NODES+nodes[1:-1]
        # print NODES
        # print ELEMENTS
        for element in ELEMENTS:
            print(element.getNodeI().getNum(),element.getNodeJ().getNum())
            # print(element.getNodeJ().getNum())
        for node in NODES:
            print node.getNum()
        PLOTSTRUCTURE()


class ConstraintWin(Tkinter.Tk):
    def __init__(self,parent=None):
        Tkinter.Tk.__init__(self,parent)
        self.initialize()

    def initialize(self):
        self.grid()
        self.title('Constraint Window')

        title = Tkinter.Label(self, text = 'Set Constraint')
        title.grid(column=0, row=0, sticky='EW')

        node = Tkinter.Label(self, text = 'Node to Constrain')
        node.grid(column=0, row=1, sticky='EW')
        self.n=Tkinter.Entry(self)
        self.n.grid(column=1,row=1,sticky='EW')


        dofs = ELEMENTS[0].getLocalDofList()


        if len(dofs)==4:
            self.dofs=['UX','UY']
        elif len(dofs)==6:
            self.dofs=['UX','UY','R']


        if len(self.dofs)==2:
            self.v1 = Tkinter.IntVar(self)
            c1 = Tkinter.Checkbutton(self,text='UX',variable=self.v1)
            c1.grid(column=0,row=3,sticky='EW')
            self.v2 = Tkinter.IntVar(self)
            c2 = Tkinter.Checkbutton(self,text='UY',variable=self.v2)
            c2.grid(column=1,row=3,sticky='EW')

        elif len(self.dofs)==3:
            self.v1 = Tkinter.IntVar(self)
            c1 = Tkinter.Checkbutton(self,text='UX',variable=self.v1)
            c1.grid(column=0,row=3,sticky='EW')
            self.v2 = Tkinter.IntVar(self)
            c2 = Tkinter.Checkbutton(self,text='UY',variable=self.v2)
            c2.grid(column=1,row=3,sticky='EW')
            self.v3 = Tkinter.IntVar(self)
            c3 = Tkinter.Checkbutton(self,text='R',variable=self.v3)
            c3.grid(column=2,row=3,sticky='EW')

        self.click=Tkinter.Button(self,text='Constrain',command=self.Constrain)
        self.click.grid(column=0, row=4,sticky='EW')


    def Constrain(self):
        global CONSTRAINTS
        print len(self.dofs)
        if len(self.dofs)==2:
            if self.v1.get():
                CONSTRAINTS=CONSTRAINTS+['UX'+str(self.n.get())]
            if self.v2.get():
                CONSTRAINTS=CONSTRAINTS+['UY'+str(self.n.get())]

        if len(self.dofs)==3:
            if self.v1.get()==True:
                CONSTRAINTS=CONSTRAINTS+['UX'+str(self.n.get())]
            if self.v2.get()==True:
                CONSTRAINTS=CONSTRAINTS+['UY'+str(self.n.get())]
            if self.v3.get()==True:
                CONSTRAINTS=CONSTRAINTS+['R'+str(self.n.get())]

        print CONSTRAINTS


class SolveWin(Tkinter.Tk):
    def __init__(self,parent=None):
        Tkinter.Tk.__init__(self,parent)
        self.initialize()

    def initialize(self):
        self.grid()
        self.title('Solve for Modes')

        title = Tkinter.Label(self, text = 'Solve')
        title.grid(column=0, row=0, sticky='EW')

        nM = Tkinter.Label(self, text = 'Enter number of Modes')
        nM.grid(column=0, row=1, sticky='EW')
        self.nM=Tkinter.Entry(self)
        self.nM.grid(column=1,row=1,sticky='EW')

        click=Tkinter.Button(self,text='Solve',command=self.solvemodes)
        click.grid(column=0,row=2,sticky='EW')

    def solvemodes(self):
        import LineElements,systemMatrices
        import numpy as np
        import scipy.sparse.linalg as spla
        global DOFDICT
        global  FREQUENCY
        global SHAPES

        massMatrixData = []
        stiffnessMatrixData = []
        dofList = []

        print ELEMENTS

        for element in ELEMENTS:
            # DOF IDs of this element
            dofs = element.getDofList()
            print 'Hello'
            print dofs

            # Element mass and stiffness matrices
            Me = element.getMassMatrix()
            Ke = element.getStiffnessMatrix()

            # Package for assembly
            massMatrixData.append((Me, dofs))
            stiffnessMatrixData.append((Ke, dofs))
            dofList = dofList + dofs
            print dofList
            print 'Bye'

        # Assemble system matrices
        dofDict = systemMatrices.buildDofDict(dofList)
        M = systemMatrices.buildSystemMatrix(massMatrixData, dofDict)
        K = systemMatrices.buildSystemMatrix(stiffnessMatrixData, dofDict)
        DOFDICT= dofDict

        # Remove the DOFs constrained by the beam being fixed at the bottom
        # nodeBaseNum = nodeBase.getNum()
        # removeDofs = ['UX%d'%nodeBaseNum, 'UY%d'%nodeBaseNum, 'R%d'%nodeBaseNum]
        removeList = [dofDict[d] for d in CONSTRAINTS]
        print removeList
        M = systemMatrices.removeRowsCols(M, removeList)
        K = systemMatrices.removeRowsCols(K, removeList)
        # print M.todense()
        # print K.todense()
        print M

        # Make sure K and M are in CSR format for efficient matrix-vector
        # multiplication
        M = M.tocsr()
        K = K.tocsr()
        n=int(self.nM.get())
        print 'n',n

        # Solve for the first three vibration modes and frequencies
        w, v = spla.eigsh(K, n, M, sigma=0.)

        print 'Natural frequencies:'
        print np.sqrt(w)
        w=np.sqrt(w)
        FREQUENCY.append(w)
        SHAPES.append(v)


# Superclass for results listing windows
class TextWindow(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)

        # Grid layout, with custom row/column resizing
        self.grid()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Central text box
        self._textBox = Tkinter.Text(self)
        self._textBox['wrap'] = Tkinter.NONE
        self._textBox.grid(row=0, column=0, sticky='NSEW')

        # Vertical scroll bar
        self._yScroll = Tkinter.Scrollbar(self, command=self._textBox.yview)
        self._yScroll.grid(row=0, column=1, sticky='NSEW')
        self._textBox['yscrollcommand'] = self._yScroll.set

        # Horizontal scroll bar
        self._xScroll = Tkinter.Scrollbar(self, orient=Tkinter.HORIZONTAL, command=self._textBox.xview)
        self._xScroll.grid(row=1, column=0, sticky='NSEW')
        self._textBox['xscrollcommand'] = self._xScroll.set

    def appendText(self, textString):
        self._textBox.insert(Tkinter.END, textString)


class ResultsWin(TextWindow):
    def __init__(self,parent=None):
        TextWindow.__init__(self,parent)
        self.initialize()

    def initialize(self):
        import numpy as np
        global  SHAPES
        self.grid()
        self.title('Results')

        click=Tkinter.Button(self,text='Show Frequencies',command=self.showf)
        click.grid(column=0,row=1,sticky='EW')

        m=Tkinter.Label(self,text='Select Mode')
        m.grid(column=0,row=3)

        mn = []
        SHAPES=np.array(SHAPES[0])
        print SHAPES
        # print len(SHAPES[0])
        for i in range(len(SHAPES[0,:])):
            mn.append(str(i+1))
            print mn

        self.mode=Tkinter.IntVar(self)
        self.mode.set(1)
        mm =Tkinter.OptionMenu(self,self.mode,*mn)
        mm.grid(column=1,row=3,sticky='EW')

        click=Tkinter.Button(self,text='Print mode shape',command=self.shows)
        click.grid(column=2,row=3,sticky='EW')

        click=Tkinter.Button(self,text='Plot mode shape',command=self.mplot)
        click.grid(column=3,row=3,sticky='EW')


    def showf(self):
        global  FREQUENCY
        print FREQUENCY
        for i in range(len(FREQUENCY[0])):
            f=FREQUENCY[0]
            self.appendText('%f\n'%f[i])

    def shows(self):
        n=int(self.mode.get())
        self.appendText('Mode %d\n'%n)
        for s in SHAPES:
            self.appendText(str(s[n-1]))
            self.appendText('\n')

    def mplot(self):
        import numpy as np
        global  DOFDICT
        global CONSTRAINTS
        global NODES
        global SHAPES
        ddict={}
        cindex=[]
        SHAPES=np.array(SHAPES)
        S = SHAPES[:,int(self.mode.get())-1]
        print DOFDICT
        print CONSTRAINTS
        for ck in CONSTRAINTS:
            cindex.append(DOFDICT[ck])

        print cindex

        for k, v in DOFDICT.iteritems():
            if k in CONSTRAINTS:
                print 'daffffffffffffffffffffffffffffffffffffff'
            else:
                ddict[k]=v

        print(ddict)

        for i in cindex:
            for k,v in ddict.iteritems():
                # print v,i
                if v>i:
                    ddict[k]=v-1

        print ddict

        for k,v in ddict.iteritems():
            if k[:2]=='UX':
                nodenum=k[2:]
                jk = 'UX'+nodenum
                print jk,type(jk)
                j=ddict[jk]
                for i in range(len(NODES)):
                    if NODES[i].getNum()== int(nodenum):
                        x=NODES[i].getX()+S[j]
                        # y=NODES[i].getY()
                        NODES[i].inputX(x)

        for k,v in ddict.iteritems():
            if k[:2]=='UY':
                nodenum=k[2:]
                j=ddict['UY'+nodenum]
                for i in range(len(NODES)):
                    if NODES[i].getNum()== int(nodenum):
                        y=NODES[i].getY()+S[j]
                        # y=NODES[i].getY()
                        NODES[i].inputY(y)

        import matplotlib.pyplot as plt
        import numpy as np
        plt.figure('Project')
        plt.close()
        plt.figure('Project')
        for element in ELEMENTS:
            I = element.getNodeI()
            # Inum = I.getNum()
            J = element.getNodeJ()
            # Jnum = J.getNum()

            x=np.linspace(I.getnewX(),J.getnewX(),num=10)
            y=np.linspace(I.getnewY(),J.getnewY(),num=10)
            plt.plot(x,y)
        plt.show(block=False)
