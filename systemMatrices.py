import scipy.sparse as sp
import numpy as np

def buildDofDict(dofList):
    '''Build a dictionary that maps from DOF ID to index in the
    global matrix.  Takes a list of all DOFs, and returns said
    dictionary.'''

    dofSet = set(dofList)    # Weed out duplicates

    dofDict = {}
    for iDof, dof in enumerate(dofSet):
        dofDict[dof] = iDof

    return dofDict


def buildSystemMatrix(matrixData, dofDict):
    '''Build a finite element system matrix.  The first argument is a
    list, structured as follows:
    [(matrix1, [index1_1, index1_2, ...]),
     (matrix2, [index2_1, index2_2, ...]),
     ...]
    Each element of the list is a tuple; the first element of
    the tuple is the the element matrix, and the second is a list
    saying what global DOF IDs correspond to the local DOFs of
    the element.

    The second argument is a dictionary from global DOF IDs to indices
    in the global matrices.'''

    # Build the matrix
    nDofs = len(dofDict.keys())
    mat = sp.lil_matrix((nDofs, nDofs))

    for M, dofs in matrixData:
        idxList = [dofDict[d] for d in dofs]
        for iLocal, iGlobal in enumerate(idxList):
            for jLocal, jGlobal in enumerate(idxList):
                mat[iGlobal, jGlobal] = mat[iGlobal, jGlobal] + M[iLocal, jLocal]

    return mat


def removeRowsCols(M, removeList):
    '''Remove the given rows and columns of the sparse matrix M.
    Returns the modified matrix.'''

    rm = set(removeList)          # Remove duplicates, set up for set operations
    keep = set(range(M.shape[0]))
    keep = keep.difference(rm)    # Remove indices we don't want
    keep = list(keep)             # Convert to a list for indexing
    keep.sort()                   # Sort to keep the result in the original order

    # Remove columns
    M = M.tocsc()
    M = M[:, keep]

    # Remove rows
    M = M.tocsr()
    M = M[keep, :]

    return M
