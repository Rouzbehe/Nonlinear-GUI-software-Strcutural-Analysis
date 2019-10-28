def meshLine(nodeStart, nodeEnd, numElements, elementMaker):
    import Node

    xStart = nodeStart.getX()
    yStart = nodeStart.getY()
    xEnd = nodeEnd.getX()
    yEnd = nodeEnd.getY()

    dx = (xEnd - xStart)/numElements
    dy = (yEnd - yStart)/numElements

    # Create a list of nodes from which to define the elements
    nodes = [nodeStart]
    for i in range(1, numElements):
        nodes.append(Node.Node(xStart + i*dx, yStart + i*dy))
    nodes.append(nodeEnd)

    elements = [elementMaker(nodes[i], nodes[i+1]) for i in range(numElements)]
    return elements
