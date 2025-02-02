from constants import *
from math import atan2, degrees, cos, sin, radians, pi
from copy import deepcopy
import os

class Node: 
    def __init__(self, nodeID, nodeCap, X, Y, incomingEdges = [], outgoingEdges = []):
        self._type = "Node"
        self.__nodeID = nodeID
        self._label = FONT.render(self.__nodeID, 1, BLACK)

        # Rectangle not blitted - giudeline for text to be centred in middle of node
        self._guideRect = pg.Rect(X-RADIUS, Y-RADIUS, 2*RADIUS, 2*RADIUS)
        self._textRect = self._label.get_rect(center = self._guideRect.center)

        self.__nodeCap = nodeCap
        if nodeCap > 0:
            # Marks flow that has been added to path but not incremented on the edges
            self._flowThroughNodeCap = 0
        self.__nodeCapRef = ""

        self._coords = (X, Y)
        
        self.__incomingEdges = deepcopy(incomingEdges)
        self.__outgoingEdges = deepcopy(outgoingEdges)

    def updateType(self, nodeType):
        self._type = nodeType

    def updateNodeCapRef(self, idx):
        self.__nodeCapRef = idx

    def updateFlowThroughNodeCap(self, flow):
        self._flowThroughNodeCap += flow

    def addIncomingEdge(self, edge):
        self.__incomingEdges.append(edge)

    def addOutgoingEdge(self, edge):
        self.__outgoingEdges.append(edge)

    def delIncomingEdge(self, edgeID):
        for idx, edge in enumerate(self.__incomingEdges):
            if edgeID == edge:
                self.__incomingEdges.pop(idx)

    def delOutgoingEdge(self, edgeID):
        for idx, edge in enumerate(self.__outgoingEdges):
            if edgeID == edge:
                self.__outgoingEdges.pop(idx)

    def replaceCoords(self, X, Y):
        self._coords = (X, Y)

        self._guideRect = pg.Rect(X-RADIUS, Y-RADIUS, 2*RADIUS, 2*RADIUS)
        self._textRect = self._label.get_rect(center = self._guideRect.center)

    def resetPossFlow(self):
        self._flowThroughNodeCap = 0
        
    def draw(self):
        pg.draw.circle(SCREEN, BLUE, self._coords, RADIUS, width = 0)
        pg.draw.circle(SCREEN, BLACK, self._coords, RADIUS, width = 2)

        SCREEN.blit(self._label, self._textRect)

    def getType(self):
        return self._type

    def getNodeID(self):
        return self.__nodeID

    def getNodeCap(self):
        return self.__nodeCap

    def getCoords(self):
        return self._coords[0], self._coords[1]

    def getNoOutgoingEdges(self):
        return len(self.__outgoingEdges)
    
    def getNoIngoingEdges(self):
        return len(self.__incomingEdges)
    
    def getIncomingEdges(self):
        return self.__incomingEdges
    
    def getOutgoingEdges(self):
        return self.__outgoingEdges

    def getNodeCapRef(self):
        return self.__nodeCapRef

    def getFlowThroughNodeCap(self):
        return self._flowThroughNodeCap

    # Checks if nodeID for 2 nodes is the same
    def __eq__(self, nodeID):
        if self.__nodeID == nodeID:
            return True
        return False

class SourcesOrSinks(Node):
    def __init__(self, nodeID, nodeCap, X, Y, incomingEdges = [], outgoingEdges = []):
        super().__init__(nodeID, nodeCap, X, Y, incomingEdges, outgoingEdges)
        self._type = "Source/sink"

    # Overrides draw function from class Node
    def draw(self):
        pg.draw.circle(SCREEN, BLUE, self._coords, RADIUS, width = 0)
        pg.draw.circle(SCREEN, BLACK, self._coords, RADIUS, width = 2)
        pg.draw.circle(SCREEN, BLACK, self._coords, RADIUS+3, width = 2)

        SCREEN.blit(self._label, self._textRect)

class Edge:
    ID = 1
    def __init__(self, fromNode, toNode, minCap, maxCap, startX, startY, endX, endY):
        self.__edgeID = Edge.ID
        Edge.increaseID()
        
        self.__startX, self.__startY = startX, startY
        self.__endX, self.__endY = endX, endY
        
        self.__changeInX, self.__changeInY = endX - startX, endY - startY

        # PG has positive axis in (i, -j), so angle needs to go anti-cw instead of cw
        self.__length = self.__findLength()
        self.__angle = self.__findAngle()
        self.__angle = -self.__angle

        self.__handleTransformations()
        self.__getEdgePositions()

        # Edge components 
        self.__fromNode = fromNode
        self.__toNode = toNode

        self.__fwFlow = 0
        self.__bwFlow = maxCap
        self.__originalMinCap = deepcopy(minCap)
        self.__minCap = deepcopy(minCap)
        self.__tempMinCap = self.__minCap
        self.__maxCap = deepcopy(maxCap)

        # Flow added to edge that hasn't incremented fw flow yet
        self.__addedFlow = 0
        self.__initialMaxFlow = 0

        self.__minCapUpdated = False
        self.__partOfNodeCap = False
        
    @staticmethod
    def increaseID():
        Edge.ID += 1

    @staticmethod
    def __scaleImg(newX, newY, image):
        return pg.transform.scale(image, (newX, newY))

    @staticmethod
    def __rotateImg(image, angle):
        return pg.transform.rotate(image, angle)

    def __getEdgePositions(self):
        self.__angle = radians(self.__angle)

        # X, Y positions for big arrow stem and head
        self.__bigArrowStemX = self.__startX + self.__changeInX/2 - int(self.__bigArrow[0].get_width()/2)
        self.__bigArrowStemY = self.__startY + self.__changeInY/2 - int(self.__bigArrow[0].get_height()/2)
        self.__bigArrowHeadX = self.__endX - int(self.__bigArrow[1].get_width()/2)
        self.__bigArrowHeadY = self.__endY - int(self.__bigArrow[1].get_height()/2)

        # Finding start point for fw and bw flow
        Mx, My = self.__startX + self.__changeInX/2, self.__startY + self.__changeInY/2
        fwArrowX = 2*cos(self.__angle)*ARROWHEIGHT
        fwArrowY = 2*sin(self.__angle)*ARROWHEIGHT
        bwArrowX = 2*cos(self.__angle + pi)*ARROWHEIGHT
        bwArrowY = 2*sin(self.__angle + pi)*ARROWHEIGHT
        
        smallArrowStartX = Mx - fwArrowY - fwArrowX/2 - 5*sin(self.__angle)
        smallArrowStartY = My - fwArrowX - fwArrowY/2 - 5*cos(self.__angle)
        smallArrowEndX = Mx - 1.5*bwArrowY - bwArrowX/2
        smallArrowEndY = My - 1.5*bwArrowX - bwArrowY/2

        # X, Y positions for fw and bw arrows
        self.__fwArrowX = int(smallArrowStartX + fwArrowX/2 - self.__fwArrow.get_width()/2)
        self.__fwArrowY = int(smallArrowStartY - self.__fwArrow.get_height()/2) + fwArrowY/2
        self.__bwArrowX = int(smallArrowEndX + bwArrowX/2 - self.__bwArrow.get_width()/2)
        self.__bwArrowY = int(smallArrowEndY - self.__bwArrow.get_height()/2) + bwArrowY/2

        # Centres for numbers on each arrow. (min and max cap, fw flow and bw flow)
        self.__centreBigArrowX = self.__startX + self.__changeInX/2
        self.__centreBigArrowY = self.__startY + self.__changeInY/2 

        self.__centreFwArrowX = int(smallArrowStartX) - self.__fwArrow.get_width()*sin(self.__angle)/2 + fwArrowX/2
        self.__centreFwArrowY = int(smallArrowStartY) - self.__fwArrow.get_height()*cos(self.__angle)/2 + fwArrowY/2

        self.__centreBwArrowX = int(smallArrowEndX + bwArrowX/2) - self.__bwArrow.get_width()*sin(self.__angle + pi)/2
        self.__centreBwArrowY = int(smallArrowEndY + bwArrowY/2) - self.__bwArrow.get_height()*cos(self.__angle + pi)/2

        # Start and end coordinates for fw and bw arrows
        self.__fwArrowDetectionBoxX = [self.__centreFwArrowX - sin(self.__angle)*2.5*ARROWHEIGHT,
                                       self.__centreFwArrowX + sin(self.__angle)*2.5*ARROWHEIGHT]
        self.__fwArrowDetectionBoxY = [self.__centreFwArrowY - cos(self.__angle)*2.5*ARROWHEIGHT,
                                       self.__centreFwArrowY + cos(self.__angle)*2.5*ARROWHEIGHT]

        self.__bwArrowDetectionBoxX = [self.__centreBwArrowX - sin(self.__angle + pi)*2.5*ARROWHEIGHT,
                                       self.__centreBwArrowX + sin(self.__angle + pi)*2.5*ARROWHEIGHT]
        self.__bwArrowDetectionBoxY = [self.__centreBwArrowY - cos(self.__angle + pi)*2.5*ARROWHEIGHT,
                                       self.__centreBwArrowY + cos(self.__angle + pi)*2.5*ARROWHEIGHT]

    def __handleTransformations(self):
        #Big arrow split into 2 so head remians proportional
        self.__bigArrow = [pg.image.load(os.path.join("Images", "Arrow-stem.png")).convert_alpha(),
                           pg.image.load(os.path.join("Images", "arrowHead.png")).convert_alpha()]
        self.__fwArrow = pg.image.load(os.path.join("Images", "Arrow.png")).convert_alpha()
        self.__bwArrow = pg.image.load(os.path.join("Images","Arrow.png")).convert_alpha()
        
        # Rescaling and rotating
        self.__bigArrow[0] = self.__scaleImg(self.__length, ARROWHEIGHT, self.__bigArrow[0])
        self.__bigArrow[1] = self.__scaleImg(SMALLARROWWIDTH, SMALLARROWWIDTH, self.__bigArrow[1])
        self.__fwArrow = self.__scaleImg(SMALLARROWWIDTH, 2*ARROWHEIGHT, self.__fwArrow)
        self.__bwArrow = self.__scaleImg(SMALLARROWWIDTH, 2*ARROWHEIGHT, self.__bwArrow)
        
        self.__bigArrow[0] = self.__rotateImg(self.__bigArrow[0], self.__angle)
        self.__bigArrow[1] = self.__rotateImg(self.__bigArrow[1], self.__angle)
        self.__fwArrow = self.__rotateImg(self.__fwArrow, self.__angle)
        self.__bwArrow = self.__rotateImg(self.__bwArrow, self.__angle + 180)

    def __findLength(self):
        return int(((self.__changeInX**2) + (self.__changeInY**2))**0.5)
    
    def __findAngle(self):
        if self.__changeInX == 0:
            if self.__changeInY > 0:
                return 90
            else:
                return -90
        else:
            return degrees(atan2(self.__changeInY, self.__changeInX))

    def updateTempMinCap(self, flow):
        self.__tempMinCap += flow

    def updatePartOfNodeCap(self, boolean):
        self.__partOfNodeCap = boolean

    def updateAddedFlow(self, flow):
        self.__addedFlow += flow

    def updateInitialMaxFlow(self, flow):
        self.__initialMaxFlow += flow

    def addFlow(self, flow):
        self.__fwFlow += flow
        self.__bwFlow -= flow

    def raiseMinCap(self, flow):
        self.__minCap += flow
        self.__minCapUpdated = True

    def resetEdge(self):
        self.__minCap = self.__originalMinCap
        self.__tempMinCap = self.__originalMinCap

        self.__fwFlow = 0
        self.__bwFlow = self.__maxCap

        self.__addedFlow = 0
        self.__initialMaxFlow = 0

        self.__minCapUpdated = False

    def hasMinCap(self):
        if self.__minCap > 0:
            return True
        return False
        
    def draw(self, ifMinCap):
        SCREEN.blit(self.__bigArrow[0], (self.__bigArrowStemX, self.__bigArrowStemY))
        SCREEN.blit(self.__bigArrow[1], (self.__bigArrowHeadX, self.__bigArrowHeadY))

        SCREEN.blit(self.__fwArrow, (self.__fwArrowX, self.__fwArrowY))
        SCREEN.blit(self.__bwArrow, (self.__bwArrowX, self.__bwArrowY))

        self.__drawMinAndMaxCap(ifMinCap)
                        
        # Draws fw flow and bw flow values
        label = SMALLFONT.render(f"{self.__fwFlow}", 10, BLACK, WHITE)
        textRect = label.get_rect()
        textRect.center = (self.__centreFwArrowX, self.__centreFwArrowY)
        
        SCREEN.blit(label, textRect)

        if self.__bwFlow == 0:
            label = SMALLFONT.render(f"{self.__bwFlow}", 10, BLACK, YELLOW)
        else:
            label = SMALLFONT.render(f"{self.__bwFlow}", 10, BLACK, WHITE)
        textRect = label.get_rect()
        textRect.center = (self.__centreBwArrowX, self.__centreBwArrowY)
        
        SCREEN.blit(label, textRect)

    def __drawMinAndMaxCap(self, ifMinCap):
        if not self.__minCapUpdated:
            if ifMinCap:
                 text = f" {self.__minCap},{self.__maxCap} "
            else:
                text = f" {self.__maxCap} "
            label = SMALLFONT.render(text, 10, BLACK, WHITE)
            textRect = label.get_rect()
            textRect.center = (self.__centreBigArrowX, self.__centreBigArrowY)
            
            SCREEN.blit(label, textRect)
        else:
            # Splits the label into 2, to change colour of min cap value on screen 
            fullW = WRITINGFONTLETTERWIDTH*len(f" {self.__minCap},{self.__maxCap} ")
            partW = WRITINGFONTLETTERWIDTH*len(f" {self.__minCap}")
            fullW /= 2
            
            minCapLabel = SMALLFONT.render(f" {self.__minCap}", 10, BLACK, YELLOW)
            minCapTextRect = minCapLabel.get_rect()
            minCapTextRect.center = (self.__centreBigArrowX - fullW + partW, self.__centreBigArrowY)
            SCREEN.blit(minCapLabel, minCapTextRect)

            maxCapLabel = SMALLFONT.render(f",{self.__maxCap} ", 10, BLACK, WHITE)
            maxCapTextRect = maxCapLabel.get_rect()
            maxCapTextRect.center = (self.__centreBigArrowX + partW/2, self.__centreBigArrowY)
            
            SCREEN.blit(maxCapLabel, maxCapTextRect)
        
    def getEdgeID(self):
        return self.__edgeID

    def getFromNode(self):
        return self.__fromNode

    def getToNode(self):
        return self.__toNode

    def getMaxCap(self):
        return self.__maxCap

    def getMinCap(self):
        return self.__minCap

    def getBwFlow(self):
        return self.__bwFlow

    def getFwFlow(self):
        return self.__fwFlow

    def getTempMinCap(self):
        return self.__tempMinCap

    def getOriginalMinCap(self):
        return self.__originalMinCap

    def getAddedFlow(self):
        return self.__addedFlow

    def getInitialMaxFlow(self):
        return self.__initialMaxFlow

    def getPartOfNodeCap(self):
        return self.__partOfNodeCap

    def getStartCoords(self):
        return [self.__startX, self.__startY]

    def getEndCoords(self):
        return [self.__endX, self.__endY]

    def getSmallFwArrowCoords(self):
        return [self.__fwArrowDetectionBoxX, self.__fwArrowDetectionBoxY]

    def getSmallBwArrowCoords(self):
        return [self.__bwArrowDetectionBoxX, self.__bwArrowDetectionBoxY]

    def getFwFlowTextRect(self):
        label = SMALLFONT.render(f"{self.__fwFlow}", 10, BLACK, WHITE)
        textRect = label.get_rect()
        textRect.center = (self.__centreFwArrowX, self.__centreFwArrowY)
        return textRect

    def getBwFlowTextRect(self):
        label = SMALLFONT.render(f"{self.__bwFlow}", 10, BLACK, WHITE)
        textRect = label.get_rect()
        textRect.center = (self.__centreBwArrowX, self.__centreBwArrowY)
        return textRect

    def __eq__(self, otherEdgeID):
        if otherEdgeID == self.__edgeID:
            return True
        return False
