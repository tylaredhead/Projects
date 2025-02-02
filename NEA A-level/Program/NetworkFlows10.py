# NEA deadline - 1st March
from constants import *
from functionalTools3 import Border, scrollbar, inputBox, Button
from GraphElements import Node, SourcesOrSinks, Edge
from GeneralComponents import Line, CircularQueue
from math import atan2, cos
from copy import deepcopy
from functools import reduce
from random import randint

class Cut:
    ID = 1
    def __init__(self, boundaryStartX, boundaryEndX, boundaryStartY, boundaryEndY):
        startX, startY = pg.mouse.get_pos()
        Line.changeNextColour()

        self.__cutID = f"C{Cut.ID}"
        self.__label = SMALLFONT.render(self.__cutID, 1, BLACK, WHITE)
        self.__textRect = self.__label.get_rect()
        
        Cut.increaseID()
 
        self.__lines = [Line(startX, startY, startX + 1, startY + 1)]
        
        self.__boundaryStartX, self.__boundaryStartY = boundaryStartX, boundaryStartY
        self.__boundaryEndX, self.__boundaryEndY = boundaryEndX, boundaryEndY

        self.__cutValue = 0

        self.__fixed = False
        self.__canDraw = True

    @staticmethod
    def increaseID():
        Cut.ID += 1

    @staticmethod
    def decreaseID():
        Cut.ID -= 1

    @staticmethod
    def resetCutID():
        Cut.ID = 1

    def handleEvents(self, event):
        X, Y = pg.mouse.get_pos()
        
        if not self.__fixed:
            # Fixes the cut as finished being drawn
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.__lines.pop(-1)
                    self.__fixed = True
                    return True
            # Allows another segment to be added onto the cut
            elif event.type == pg.MOUSEBUTTONDOWN:
                if X > self.__boundaryStartX + SMALLPAD and X < self.__boundaryEndX - SMALLPAD:
                    if Y > self.__boundaryStartY + SMALLPAD and Y < self.__boundaryEndY - SMALLPAD:
                        self.__lines[-1].setFixed()
                        endX, endY = self.__lines[-1].getEndCoords()
                        line = Line(endX, endY, endX+1, endY+1)
                        self.__lines.append(line)
        # Changes end point of current segment            
        if X > self.__boundaryStartX + SMALLPAD and X < self.__boundaryEndX - SMALLPAD:
            if Y > self.__boundaryStartY + SMALLPAD and Y < self.__boundaryEndY - SMALLPAD:
                self.__lines[-1].updatePos(X, Y)
        
        return False

    def validateLineCollisionWithNode(self, X, Y):
        collisions, idx = False, 0

        while not collisions and idx < len(self.__lines): 
            x1, y1 = self.__lines[idx].getStartCoords()
            x2, y2 = self.__lines[idx].getEndCoords()

            # Determines if gradient is in j direction (undefined)
            if x2 != x1: 
                m = (y2 - y1)/(x2 - x1)
                c = -m*x1 + y1

                shortestDist = abs(-m*X + Y -c)//((1+(m)**2)**0.5)
                # Checks if shortest distance collides with node with the edge coordinates
                if shortestDist - RADIUS - SMALLPAD <= 0:
                    if X >= min(x1,x2) - RADIUS and X <= max(x1, x2) + RADIUS:
                        if Y >= min(y1, y2) - RADIUS and Y <= max(y1, y2) + RADIUS:
                            collisions = True
            else:
                m, x = "Inf", x2
        
                # checks if node intersects within the edge coordinates
                if x <= X + RADIUS + SMALLPAD and x >= X - RADIUS - SMALLPAD:
                    if y1 >= Y - RADIUS - SMALLPAD and y2 <= Y + RADIUS + SMALLPAD:
                        collisions = True

            idx += 1

        return collisions
    
    def validateLineCollisionWithEdge(self, startX, startY, endX, endY):
        collisions, idx = False, 0
        
        if startX != endX:
            m1 = (endY - startY)/(endX - startX)
            c1 = -m1*startX + startY
        else:
            m1 = "Inf"
            c1 = startX
                
        while not collisions and idx < len(self.__lines):
            x1, y1 = self.__lines[idx].getStartCoords()
            x2, y2 = self.__lines[idx].getEndCoords()

            # Determines if gradient is in j direction (undefined)
            if x2 != x1:
                m2 = (y2 - y1)/(x2 - x1)
                c2 = -m2*x2 + y2
            else:
                m2, c2 = ["Inf", x2]

            # Checks if 2 vertical lines collides 
            if m2 == "Inf" and m2 == m1:
                if abs(c2 - c1) <= MEDIUMPAD:
                    collisions = True
            # Checks if the vertical cut line drawn intersects edge 
            elif m2 == "Inf" and m1 != "Inf":
                x = c2
                y = m1*x + c1
                if x >= min(startX, endX) and x <= max(startX, endX):
                    if y >= min(startY, endY) and y <= max(startY, endY):
                        if x >= min(x1, x2) and x <= max(x1, x2) and y >= min(y1, y2) and y <= max(y1, y2):
                            collisions = True
            # Checks if the vertical edge intersects edge
            elif m1 == "Inf" and m2 != "Inf":
                x = c1
                y = m2*x + c2
                if x >= min(x1, x2) and x <= max(x1, x2) and y >= min(y1, y2) and y <= max(y1, y2):
                    if x >= min(startX, endX) and x <= max(startX, endX):
                        if y >= min(startY, endY) and y <= max(startY, endY):
                            collisions = True
            # Checks if collision is within the range of the edge
            elif m1 != m2:
                x = (c1 - c2)/(m2 - m1)
                y = (m2*c1 - m1*c2)/(m2 - m1)
                
                if x >= min(x1, x2) and x <= max(x1, x2) and y >= min(y1, y2) and y <= max(y1, y2):
                    if x >= min(startX, endX) and x <= max(startX, endX):
                        if y >= min(startY, endY) and y <= max(startY, endY):
                            collisions = True

            idx += 1
                
        return collisions

    def updateCanDraw(self):
        self.__canDraw = not self.__canDraw
    
    def setFixed(self):
        self.__fixed = True

    def setCutNotation(self, nodesOnSourceSide, nodesOnSinkSide):
        self.__cutNotation = "{ " + nodesOnSourceSide + " } / { " + nodesOnSinkSide + " }"
    
    def setCutValues(self, valuesOnSourceSide, valuesOnSinkSide, source2SinkTotal, sink2SourceTotal):
        self.__valuesOnSourceSide, self.__valuesOnSinkSide = valuesOnSourceSide, valuesOnSinkSide
        self.__source2SinkTotal, self.__sink2SourceTotal = source2SinkTotal, sink2SourceTotal
        
        self.__cutValue = source2SinkTotal - sink2SourceTotal        
    
    def draw(self):
        if self.__canDraw:
            for line in self.__lines:
                line.draw()
                
            X1, Y1 = self.__lines[0].getStartCoords()
            X2, Y2 = self.__lines[0].getEndCoords()
            if Y2 - Y1 > 0:
                self.__textRect.center = (X1, Y1 - 10)
            else:
                self.__textRect.center = (X1, Y1 + 10)
            SCREEN.blit(self.__label, self.__textRect)

    def getCutID(self):
        return self.__cutID

    def getIfFixed(self):
        return self.__fixed

    def getNoOfLines(self):
        return len(self.__lines)

    def getCutNotation(self):
        return self.__cutNotation

    def getCutValue(self):
        return self.__cutValue

    def __eq__(self, other):
        if self.__cutID == other:
            return True
        return False

class NetworkFlows:
    def __init__(self):
        self.__phase = "EditPhase"

        self.__edges, self.__nodes = [], []
        self.__sources, self.__sinks = [], []
        self.__cuts = []

        self.__reservedNodeIDs = ["T", "S", ",", ",,"]
        
        # [0] ==> relates to supersources, [1] ==> relates to supersinks, [2] ==> relates to node cap
        # For each augmented path: [0] ==> path, [1] ==> flow
        self.__addedNodes = [[], [], []]
        self.__addedEdges = [[], [], []]
        self.__addedFlows = []

        self.__minimumPaths, self.__maximumPaths, self.__pathsToRemove = [], [], []  
        self.__maxFlowTotal, self.__minCutTotal = 0, 0
        self.__minFlowTotal, self.__additionalTotal = 0, 0

        self.__createBorders()
        self.__createInputBoxes()
        self.__createScrollbars()
        self.__createButtons()

        self.__invalidInput = False
        self.__ifMinCap, self.__ifNodeCap = False, False
        self.__isSupersource, self.__isSupersink = False, False
        self.__ammendment = False
   
    def __createBorders(self):
        self.__dispInfoBorder = Border(0, 0, 300, 275)
        self.__inpNodeBorder = Border(0, 280, 300, 55)
        self.__inpEdgeBorder = Border(0, 340, 300, 55)
        self.__inpFlowBorder = Border(0, 400, 300, 45)
        self.__dispCutBorder = Border(0, 450, 60, 255)
        self.__maxFlowBorder = Border(65, 450, 355, 255)
        self.__minCutBorder = Border(425, 450, 530, 255)
        self.__aidBorder = Border(960, 450, 245, 125)
        self.__errorBorder = Border(960, 580, 245, 120)
        self.__graphDispBorder = Border(305, 0, 895, 445, LIGHTGREY)
        self.__theoremProvedBorder = Border(50, 100, 200, 75, LIGHTGREY)

    def __createInputBoxes(self):
        self.__nodeInpBoxes = [inputBox("Node ID", self.__inpNodeBorder.getX() + 55, self.__inpNodeBorder.getY() + LARGEPAD,
                                      STRBUTTONWIDTH, BUTTONHEIGHT, "Node ID", "Str"), 
                             inputBox("Node Cap", self.__inpNodeBorder.getX() + 155, self.__inpNodeBorder.getY() + LARGEPAD,
                                      INTBUTTONWIDTH, BUTTONHEIGHT, "0", "Int"), 
                             inputBox("X", self.__inpNodeBorder.getX() + 210, self.__inpNodeBorder.getY() + LARGEPAD,
                                      INTBUTTONWIDTH, BUTTONHEIGHT, "0", "Float"), 
                             inputBox("Y", self.__inpNodeBorder.getX() + 265, self.__inpNodeBorder.getY() + LARGEPAD,
                                      INTBUTTONWIDTH, BUTTONHEIGHT, "0", "Float")]
        
        self.__edgeInpBoxes = [inputBox("From Node", self.__inpEdgeBorder.getX() + 40, self.__inpEdgeBorder.getY() + LARGEPAD,
                                      STRBUTTONWIDTH, BUTTONHEIGHT, "Node ID", "Str"),
                             inputBox("To Node", self.__inpEdgeBorder.getX() + 103, self.__inpEdgeBorder.getY() + LARGEPAD,
                                      STRBUTTONWIDTH, BUTTONHEIGHT, "Node ID", "Str"),
                             inputBox("Min Cap", self.__inpEdgeBorder.getX() + 190, self.__inpEdgeBorder.getY() + LARGEPAD,
                                      INTBUTTONWIDTH, BUTTONHEIGHT, "0", "Int"),
                             inputBox("Max Cap", self.__inpEdgeBorder.getX() + 265, self.__inpEdgeBorder.getY() + LARGEPAD,
                                      INTBUTTONWIDTH, BUTTONHEIGHT, "0", "Int")]

        self.__flowInpBoxes = [inputBox("Path", self.__inpFlowBorder.getX() + 40, self.__inpFlowBorder.getY() + MEDIUMPAD,
                                      175, BUTTONHEIGHT, "A,B,C,...", "Str"),
                             inputBox("Flow", self.__inpFlowBorder.getX() + 245, self.__inpFlowBorder.getY() + MEDIUMPAD + 2,
                                      INTBUTTONWIDTH, BUTTONHEIGHT, "0", "Int")]

    def __createScrollbars(self):
        self.__dispInfoScrollbar = scrollbar(SMALLPAD, SMALLPAD, self.__dispInfoBorder.getW() - LARGEPAD,
                                        self.__dispInfoBorder.getH() - LARGEPAD, "", 12, "U")
        self.__errorScrollbar = scrollbar(self.__errorBorder.getX() + SMALLPAD, self.__errorBorder.getY(),
                                        self.__errorBorder.getW() - LARGEPAD, self.__errorBorder.getH() - SMALLPAD, "Errors", 5, "R")
        self.__cutIDScrollbar = scrollbar(self.__dispCutBorder.getX() + SMALLPAD, self.__dispCutBorder.getY(),
                                        self.__dispCutBorder.getW() - LARGEPAD, self.__dispCutBorder.getH() - LARGEPAD,
                                        "Cut ID's", 10, "U")
        self.__dispCutInfoScrollbar = scrollbar(self.__minCutBorder.getX() + SMALLPAD, self.__minCutBorder.getY(),
                                        self.__minCutBorder.getW() - LARGEPAD, self.__minCutBorder.getH() - SMALLPAD,
                                        "Cut Info", 11, "R", [0, 180,300,420], 2)
        
        self.__aidScrollbar = scrollbar(self.__aidBorder.getX() + SMALLPAD, self.__aidBorder.getY(),
                                        self.__aidBorder.getW() - LARGEPAD, self.__aidBorder.getH() - SMALLPAD, "Tips", 5, "R")
        self.__minFlowScrollbar = scrollbar(self.__maxFlowBorder.getX() + SMALLPAD, self.__maxFlowBorder.getY() + SMALLPAD,
                                        self.__maxFlowBorder.getW()/2 - LARGEPAD, self.__maxFlowBorder.getH() - 2*LARGEPAD,
                                        "Min Flow - Total = 0", 7, "U", [0, self.__maxFlowBorder.getW()/4 + SMALLPAD])
        self.__maxFlowScrollbar = scrollbar(self.__maxFlowBorder.getX() + self.__maxFlowBorder.getW()/4 + SMALLPAD,
                                            self.__maxFlowBorder.getY() + SMALLPAD,
                                        self.__maxFlowBorder.getW()/2 - LARGEPAD, self.__maxFlowBorder.getH() - 2*LARGEPAD,
                                        "Additional Flow - Total = 0", 7, "U", [0, self.__maxFlowBorder.getW()/4 + SMALLPAD])
        
        self.__maxFlowCoordsPoss = [self.__maxFlowBorder.getX() + self.__maxFlowBorder.getW()/4 + SMALLPAD,
                                  self.__maxFlowBorder.getX() + self.__maxFlowBorder.getW()/2 + SMALLPAD]

        self.__minFlowCoordsPoss = [self.__maxFlowBorder.getX() + self.__maxFlowBorder.getW()/4 + SMALLPAD,
                                    self.__maxFlowBorder.getX() + SMALLPAD]

        self.__aidScrollbar.insertRecords(0, f"Node - circle with node ID at centre")
        self.__aidScrollbar.insertRecords(-1, f"Sources/sinks - circle with black outline")
        self.__aidScrollbar.insertRecords(-1, f"Edge - arrow with main arrow showing direction")
        self.__aidScrollbar.insertRecords(-1, f"Graph made must be planar")

    def __createButtons(self):
        self.__addNodeButton = Button(self.__inpNodeBorder.getX() + self.__inpNodeBorder.getW() - STRBUTTONWIDTH - SMALLPAD,
                                    self.__inpNodeBorder.getY() + SMALLPAD, STRBUTTONWIDTH, BUTTONHEIGHT, "Add", BLACK)
        self.__addEdgeButton = Button(self.__inpEdgeBorder.getX() + self.__inpEdgeBorder.getW() - STRBUTTONWIDTH - SMALLPAD,
                                    self.__inpEdgeBorder.getY() + SMALLPAD, STRBUTTONWIDTH, BUTTONHEIGHT, "Add", BLACK)
        self.__addFlowButton = Button(self.__inpFlowBorder.getX() + self.__inpFlowBorder.getW() - STRBUTTONWIDTH - SMALLPAD,
                                    self.__inpFlowBorder.getY() + SMALLPAD - 2, STRBUTTONWIDTH - SMALLPAD,
                                    BUTTONHEIGHT - SMALLPAD, "Add", BLACK)
        
        self.__solveOrEditButton = Button(self.__graphDispBorder.getX(), self.__graphDispBorder.getY(),
                                        STRBUTTONWIDTH, BUTTONHEIGHT, ["Solve", "Edit"], BLACK, 2)
        
        self.__nodeCapButton = Button(self.__graphDispBorder.getX() + STRBUTTONWIDTH + 6*LARGEPAD, self.__graphDispBorder.getY(),
                                      3*LARGEPAD, BUTTONHEIGHT, ["Show Node Cap", "Hide Node Cap"], BLACK, 2)
        self.__supersourceButton = Button(self.__graphDispBorder.getX() + STRBUTTONWIDTH, self.__graphDispBorder.getY(),
                                      3*LARGEPAD, BUTTONHEIGHT, ["Show Supersource", "Hide Supersource"], BLACK, 2)
        self.__supersinkButton = Button(self.__graphDispBorder.getX() + STRBUTTONWIDTH + 3*LARGEPAD,
                                      self.__graphDispBorder.getY(), 3*LARGEPAD, BUTTONHEIGHT,
                                      ["Show Supersink", "Hide Supersink"], BLACK, 2)
        self.__nextButton = Button(self.__graphDispBorder.getX() + STRBUTTONWIDTH + 9*LARGEPAD,
                                      self.__graphDispBorder.getY(), 3*LARGEPAD, BUTTONHEIGHT, "Next", BLACK)

        self.__delButtons = []
        for i in range(12):
            button = Button(self.__dispInfoScrollbar.getX() + self.__dispInfoScrollbar.getW(),
                            self.__dispInfoScrollbar.getY() + i*20, INTBUTTONWIDTH, BUTTONHEIGHT, "Del", BLACK)
            
            self.__delButtons.append(button)

        self.__showCutIDButtons = []

        self.__nodeCapButton.setHideButton()
        self.__supersourceButton.setHideButton()
        self.__supersinkButton.setHideButton()

    def main(self, eventList):
        invalidGraph = False
        ifClicked = self.setPhase(eventList)

        # If going from solve phase ==> edit phase
        if ifClicked and self.__phase == "EditPhase":
            self.__initialEditPhase()
        # If going from edit phase ==> solve phase
        elif ifClicked and self.__phase == "SolvePhase":
            invalidGraph = self.__initialSolvePhase(invalidGraph)
        elif self.__phase == "EditPhase":
            self.__editPhase(eventList)
        else:
            self.__solvePhase(eventList)                            
                
        if not invalidGraph:
            self.__errorScrollbar.handleEvents(eventList)
            self.__aidScrollbar.handleEvents(eventList)
            self.__dispInfoScrollbar.handleEvents(eventList)
            self.__minFlowScrollbar.handleEvents(eventList)
            self.__maxFlowScrollbar.handleEvents(eventList)

        self.__draw()

    def setPhase(self, eventList):
        ifClicked = self.__solveOrEditButton.handleEvents(eventList)
  
        if ifClicked:
            if self.__solveOrEditButton.getCurrentPhase() == "Edit":
                self.__phase = "SolvePhase"
            elif self.__solveOrEditButton.getCurrentPhase() == "Solve":
                self.__phase = "EditPhase"

        return ifClicked
    
    def __initialEditPhase(self):
        # Deletes all edge IDs related to supersource/supersinks
        if self.__addedNodes[0] != []:
            edgeIDs = self.__addedNodes[0].getOutgoingEdges()
            for node in self.__nodes:
                for edgeID in edgeIDs:
                    node.delIncomingEdge(edgeID)
                    
        if self.__addedNodes[1] != []:
            edgeIDs = self.__addedNodes[1].getIncomingEdges()
            for node in self.__nodes:
                for edgeID in edgeIDs:
                    node.delOutgoingEdge(edgeID)

        self.__sources, self.__sinks, self.__cuts = [], [], []
        self.__addedNodes = deepcopy([[], [], []])
        self.__addedEdges = deepcopy([[], [], []])

        self.__minimumPaths, self.__maximumPaths, self.__pathsToRemove = [], [], []
        self.__maxFlowTotal, self.__minCutTotal = 0, 0
        self.__minFlowTotal, self.__additionalTotal = 0, 0

        self.__minFlowScrollbar.reset()
        self.__maxFlowScrollbar.reset()

        if self.__maxFlowScrollbar.getLenDispData() == 0 and self.__addedFlows != []:
            self.__maxFlowScrollbar.insertRecords(0, ["Path", "Flow"])

        for node in self.__nodes:
            node.resetPossFlow()
            node.updateNodeCapRef("")

        for edge in self.__edges:
            edge.resetEdge()
            edge.updatePartOfNodeCap(False)

        self.__checkMinCap()

        # Resets/ Re-adds initial flow by user 
        for addedFlow in self.__addedFlows:
            path, flow = addedFlow
            if "T" in path:
                path.remove("T")
            if "S" in path:
                path.remove("S")

            idx = 0
            while idx < len(path) - 1:
                edge = self.__getEdgeFromNodeIDs(path, idx)
                edge.addFlow(int(flow))

                idx += 1

            self.__maxFlowScrollbar.insertRecords(-1, [",".join(path), str(flow)])
            self.__additionalTotal += flow
            self.__maxFlowScrollbar.updateHeader(f"Max Flow - Total = {self.__additionalTotal}")

        self.__isSupersource, self.__isSupersink, self.__ifNodeCap = False, False, False
        self.__supersourceButton.setHideButton()
        self.__supersinkButton.setHideButton()
        self.__nodeCapButton.setHideButton()

        self.__cutIDScrollbar.reset()
        self.__dispCutInfoScrollbar.reset()
        Cut.resetCutID()

        self.__showCutIDButtons = []

    def __initialSolvePhase(self, invalidGraph):
        self.__sources, self.__sinks = [], []
        
        # Dictionaries: ID ==> idx of where they are stored
        self.__edgeRelDict, self.__nodeRelDict = {}, {}
        for idx, edge in enumerate(self.__edges):
            self.__edgeRelDict[edge.getEdgeID()] = idx
        
        connected = True
        for idx, node in enumerate(self.__nodes):
            if self.__nodeRelDict.get(node.getNodeID(), False) == False:
                self.__nodeRelDict[node.getNodeID()] = idx
            if node.getType() != "Node":
                if node.getNoOutgoingEdges() > 0:
                    self.__sources.append(node)
                elif node.getNoIngoingEdges() > 0:
                    self.__sinks.append(node)
                else:
                    connected = False
                    if not (len(self.__nodes) == 1 and self.__nodes[0].getNodeCap() != 0):
                        self.__errorScrollbar.insertRecords(-1, "Graph not connected")

        if connected and len(self.__nodes) > len(self.__edges) + 1:
            connected = False
            if not (len(self.__nodes) == 1 and self.__nodes[0].getNodeCap() != 0):
                        self.__errorScrollbar.insertRecords(-1, "Graph not connected")
            

        if all([len(self.__sources) > 0, len(self.__sinks) > 0, len(self.__nodes) > 0, connected]):
            self.__handleAddedElements()
                
            sourceID, sinkID = [], []
            for source in self.__sources:
                sourceID.append(source.getNodeID())
            for sink in self.__sinks:
                sinkID.append(sink.getNodeID())
                                                                                                             
            self.__removeInvalidFlows(sourceID, sinkID)

            # Checks nodes to see if the minimum flow is greater than the maximum flow
            for node in self.__nodes:
                minInFlow, maxInFlow = 0, 0
                minOutFlow, maxOutFlow = 0, 0
                
                incomingEdgeIDs, outgoingEdgeIDs = node.getIncomingEdges(), node.getOutgoingEdges()
                for incomingEdgeID in incomingEdgeIDs:
                    edge = self.__getEdge(self.__edgeRelDict[incomingEdgeID])
                    minInFlow += edge.getMinCap()
                    maxInFlow += edge.getMaxCap()

                for outgoingEdgeID in outgoingEdgeIDs:
                    edge = self.__getEdge(self.__edgeRelDict[outgoingEdgeID])
                    minOutFlow += edge.getMinCap()
                    maxOutFlow += edge.getMaxCap()

                nodeCap = node.getNodeCap()
                if (minOutFlow > maxInFlow and maxInFlow > 0) or (minInFlow > maxOutFlow and maxOutFlow > 0):
                    invalidGraph = True
                    self.__addErrorMsg("Graph drawn is invalid")
                elif (nodeCap > 0 and (nodeCap < minOutFlow or nodeCap < minInFlow)):
                    invalidGraph = True
                    self.__addErrorMsg("Graph drawn is invalid")

            if not invalidGraph:
                self.__getMaxAndMinFlows()
            else:
                self.__phase = "EditPhase"
                if self.__solveOrEditButton.getCurrentPhase() == "Edit":
                    self.__solveOrEditButton.changePhase()
                self.__initialEditPhase()
                
        elif len(self.__nodes) == 1 and self.__nodes[0].getNodeCap() != 0:
            self.__createNodeCap(self.__nodes[0])
            self.__maximumPaths.append([[self.__nodes[0].getNodeID()], self.__nodes[0].getNodeCap()])

            edge = self.__addedEdges[2][0][0]
            self.__edgeRelDict[edge.getEdgeID()] = 0
                
            self.__sources.append(self.__addedNodes[2][0][0])
            self.__sinks.append(self.__addedNodes[2][0][1])                
        else:
            self.__phase = "EditPhase"
            self.__solveOrEditButton.changePhase()
            if connected:
                self.__errorScrollbar.insertRecords(-1, "No source and/or sink")

        if self.__aidScrollbar.getLenData() < 5 and self.__phase == "SolvePhase":
            self.__aidScrollbar.insertRecords(-1, f"Next allows a new path and flow to be added")
            self.__aidScrollbar.insertRecords(-1, f"Min cap highlighted means it is temporarily")
            self.__aidScrollbar.insertRecords(-1, f"raised for min flow through graph")
            self.__aidScrollbar.insertRecords(-1, f"Backward flow highlighted means all possible")
            self.__aidScrollbar.insertRecords(-1, f"flow sent down edge")
            self.__aidScrollbar.insertRecords(-1, f"Min cuts can be ended by space bar")

        return invalidGraph

    def __handleAddedElements(self):
        for node in self.__nodes:
            if node.getNodeCap() != 0:
                self.__createNodeCap(node)

        # Removes edge from 1 node cap to another as first node cap doesnt account for seccond node cap being possible 
        for edge in self.__edges:
            fromNodeID, toNodeID = edge.getFromNode(), edge.getToNode()
            fromNodeIdx, toNodeIdx = self.__nodeRelDict[fromNodeID], self.__nodeRelDict[toNodeID]
            fromNode, toNode = self.__getNode(fromNodeIdx), self.__getNode(toNodeIdx)
            
            if fromNode.getNodeCapRef() != "" and toNode.getNodeCapRef() != "":
                for idx, addedFromEdge in enumerate(self.__addedEdges[2][fromNode.getNodeCapRef()]):
                    if fromNode.getNodeID() in addedFromEdge.getFromNode() and toNode.getNodeID() == addedFromEdge.getToNode():
                        edge = self.__addedEdges[2][fromNode.getNodeCapRef()].pop(idx)
                        for node in self.__addedNodes[2][fromNode.getNodeCapRef()]:
                            node.delIncomingEdge(edge.getEdgeID())
                            node.delOutgoingEdge(edge.getEdgeID())
                            
                for idx, addedToEdge in enumerate(self.__addedEdges[2][toNode.getNodeCapRef()]):
                    if toNode.getNodeID() in addedToEdge.getToNode() and fromNode.getNodeID() == addedFromEdge.getFromNode():
                        edge = self.__addedEdges[2][toNode.getNodeCapRef()].pop(idx)
                        for node in self.__addedNodes[2][toNode.getNodeCapRef()]:
                            node.delIncomingEdge(edge.getEdgeID())
                            node.delOutgoingEdge(edge.getEdgeID())
                
        if len(self.__sources) > 1:
            self.__createSupersource()

        if len(self.__sinks) > 1:
            self.__createSupersink()

        # Adds all added edges to dict accounting if other edges are added to node cap by supersource and supersink
        for addedEdges in self.__addedEdges[2]:
            for edge in addedEdges:
                self.__edgeRelDict[edge.getEdgeID()] = len(self.__edgeRelDict)

        for edge in self.__addedEdges[0]:
            self.__edgeRelDict[edge.getEdgeID()] = len(self.__edgeRelDict)

        for edge in self.__addedEdges[1]:
            self.__edgeRelDict[edge.getEdgeID()] = len(self.__edgeRelDict)

    def __removeInvalidFlows(self, sourceID, sinkID):
        removedIdx = []

        # Checks if start or end of path is still a source or sink
        for idx, flow in enumerate(self.__addedFlows):
            if not flow[0][0] in sourceID or not flow[0][-1] in sinkID:
                removedIdx.append(idx)
                for j, edge in enumerate(self.__edges):
                    for i in range(len(flow[0]) - 1):
                        if edge.getFromNode() == self.__addedFlows[idx][0][i] and edge.getToNode() == self.__addedFlows[idx][0][i+1]:
                            self.__edges[j].addFlow(-int(self.__addedFlows[idx][1]))
            
        removedIdx[::-1]
        for idx in removedIdx:
            recordIdx = self.__maxFlowScrollbar.findElement(",".join(self.__addedFlows[idx][0]))
            self.__maxFlowScrollbar.delRecord(recordIdx)
            self.__additionalTotal -= int(self.__addedFlows[idx][1])
            self.__maxFlowScrollbar.updateHeader(f"Max Flow - Total = {self.__additionalTotal}")

            if self.__maxFlowScrollbar.getLenDispData() == 1:
                self.__maxFlowScrollbar.delRecord(0)
            self.__addedFlows.pop(idx)

    def __getMaxAndMinFlows(self):
        self.__paths, path = [], []

        if self.__isSupersource:
            self.__paths = self.__DFS(path, self.__addedNodes[0], [])
        else:
            for source in self.__sources:  
                paths = self.__DFS(path, source, [])
                self.__paths += paths
                                    
        self.__minimumPaths, self.__maximumPaths, self.__pathsToRemove = [], [], []
        bestTotal = 0
        paths = self.__paths

        for i in range(len(self.__paths)*2):
            maximumPaths = []
            newTotal = 0

            minimumPaths, newTotal = self.__getMinimumFlows(paths, newTotal)
            maximumPaths, newTotal = self.__getMaximumFlows(paths, newTotal)

            if (minimumPaths == [] and maximumPaths == []) or (newTotal > bestTotal):
                self.__minimumPaths, self.__maximumPaths = minimumPaths, maximumPaths
                bestTotal = newTotal

            for edge in (self.__edges + self.__addedEdges[0] + self.__addedEdges[1]):
                edge.updateAddedFlow(-edge.getAddedFlow())

            for node in self.__nodes:
                if node.getNodeCap() > 0:
                    node.resetPossFlow()

            paths = self.__shuffle(self.__paths) 

        # Finds possible paths to remove if not in flow found
        flowsToDel = {}
        delMinPathIdxs, removeMaxPathIdxs, maxPathIns = [], [], []

        for userAddedFlows in self.__addedFlows:
            minPathFound = False
            
            userAddedPath, userAddedFlow = userAddedFlows
            userAddedPath = self.__updatePath(userAddedPath)

            flowsToDel[userAddedPath] = userAddedFlow

            for idx, minFlow in enumerate(self.__minimumPaths):
                minPath, minFlowVal = minFlow
                minPath = ",".join(minPath)
                
                # Shifts min path from max flow to min flow scrollbar, removing from minimum paths if already exists
                if minPath == userAddedPath:
                    minPathFound, maxPathIns, delMinPathIdxs, flowsToDel = self.__shiftMax2MinFlows(
                        userAddedPath, minFlowVal, maxPathIns, delMinPathIdxs, idx, flowsToDel)

            if not minPathFound:
                maxPathIns.append([userAddedPath, userAddedFlow])            

            delMinPathIdxs = delMinPathIdxs[::-1]
            for each in delMinPathIdxs:
                self.__minimumPaths.pop(each)
                
            for idx, maxFlow in enumerate(self.__maximumPaths):
                maxPath, maxFlowValue = maxFlow
                maxPath = ",".join(maxPath)

                for each in maxPathIns:
                    if maxPath == each[0]:
                        self.__maximumPaths[idx][1] -= each[1]
                        if self.__maximumPaths[idx][1] <= 0:
                            removeMaxPathIdxs.append(idx)
                        
                if maxPath == userAddedPath:
                    maxPath = maxPath.split(",")
                    flowsToDel[userAddedPath] -= maxFlowValue
                    for idx in range(len(userAddedPath.split(",")) - 1):
                        edge = self.__getEdgeFromNodeIDs(userAddedPath.split(","), idx)
                        # Gets the flow assigned that isnt to do with min flow
                        edge.updateInitialMaxFlow(maxFlowValue)
                    
                    if flowsToDel[userAddedPath] <= 0:
                        del flowsToDel[userAddedPath]

            removeMaxPathIdxs = removeMaxPathIdxs[::-1]
            for each in removeMaxPathIdxs:
                self.__maximumPaths.pop(each)

        for path in flowsToDel:
            if flowsToDel[path] != 0:
                self.__pathsToRemove.insert(0, [path, -flowsToDel[path]])
            
    def __getEdge(self, edgeIdx):
        # Idx based on order added: edges ==> node cap edges ==> supersource edges ==> supersink edges
        if edgeIdx < len(self.__edges):
            currentEdge = self.__edges[edgeIdx]
        else:
            found, i = False, 0
            edgeIdx -= len(self.__edges)
         
            while not found and i < len(self.__addedEdges[2]):
                addedEdges = self.__addedEdges[2][i]
                if edgeIdx < len(addedEdges):
                    currentEdge = self.__addedEdges[2][i][edgeIdx]
                    found = True
                else:
                    edgeIdx -= len(addedEdges)
                    
                i += 1

            if not found:
                if edgeIdx < len(self.__addedEdges[0]) and self.__isSupersource:
                    currentEdge = self.__addedEdges[0][edgeIdx]
                elif edgeIdx < len(self.__addedEdges[0]) + len(self.__addedEdges[1]) and self.__isSupersink:
                    currentEdge = self.__addedEdges[1][edgeIdx - len(self.__addedEdges[0])]

        return currentEdge

    def __getNode(self, nodeIdx):
        # Idx based on order added: nodes ==> node cap nodes ==> supersource nodes ==> supersink nodes
        if nodeIdx < len(self.__nodes):
            currentNode = self.__nodes[nodeIdx]
        else:
            nodeIdx -= len(self.__nodes)

            found, i = False, 0
            while i < len(self.__addedNodes[2]) and not found:
                addedNodes = self.__addedNodes[2][i]
                if nodeIdx < len(addedNodes):
                    currentNode = self.__addedNodes[2][i][nodeIdx]
                    found = True
                else:
                    nodeIdx -= len(addedNodes)

                i += 1

            if not found:
                if nodeIdx < 1 and self.__isSupersource:
                    currentNode = self.__addedNodes[0]
                elif nodeIdx < 1 and not self.__isSupersource and self.__isSupersink:
                    currentNode = self.__addedNodes[1]
                elif nodeIdx < 2 and self.__isSupersink:
                    currentNode = self.__addedNodes[1]

        return currentNode

    def __DFS(self, path, node, paths):
        path.append(node.getNodeID())

        if (node in self.__sinks and not self.__isSupersink) or node.getType() == "Supersink":
            paths.append(deepcopy(path))
        else:
            for idx, edgeID in enumerate(node.getOutgoingEdges()):
                edgeIdx = self.__edgeRelDict[edgeID]
                edge = self.__getEdge(edgeIdx)

                nodeIdx = self.__nodeRelDict[edge.getToNode()]
                adjacentNode = self.__getNode(nodeIdx)

                paths = self.__DFS(path, adjacentNode, paths)
        path.pop(-1)

        return paths

    def __getEdgeFromNodeIDs(self, path, idx):
        nodeIdx = self.__nodeRelDict[path[idx]]
        outgoingNode = self.__getNode(nodeIdx)
        outgoingEdgeIDs = outgoingNode.getOutgoingEdges()

        nodeIdx = self.__nodeRelDict[path[idx + 1]]
        ingoingNode = self.__getNode(nodeIdx)
        ingoingEdgeIDs = ingoingNode.getIncomingEdges()

        found, i = False, 0
        while not found and i < len(outgoingEdgeIDs):
            ID = outgoingEdgeIDs[i]
            if ID in ingoingEdgeIDs:
                found = True
                edgeID = ID
                edgeIdx = self.__edgeRelDict[edgeID]
                edge = self.__getEdge(edgeIdx)

            i += 1

        for setOfEdges in self.__addedEdges[2]:
            for each in setOfEdges:
                if each.getFromNode() == path[idx] and each.getToNode() == path[idx + 1]:
                    edge = each

        return edge

    def __getMinimumFlows(self, paths, newTotal):
        minimumPaths = []
        
        for path in paths:
            tempMinFlow = 1000
            idx = 0

            while idx < len(path) - 1:               
                edge = self.__getEdgeFromNodeIDs(path, idx)
                if edge.getTempMinCap() - edge.getAddedFlow() < tempMinFlow:
                    tempMinFlow = edge.getTempMinCap() - edge.getAddedFlow()
                idx += 1

            if tempMinFlow != 1000 and tempMinFlow != 0:
                minimumPaths.append([path, tempMinFlow])
                self.__updateAddedFlows(path, tempMinFlow)
                newTotal += tempMinFlow

        changesMade = True
        while changesMade:
            changesMade = False
            bestFlow = []
            
            for path in paths:
                tempMinFlow, maxFlowLeft = 0, -1
                idx, count = 0, 0
                
                # Gets highest tempMinFlow that does not exceed any maximum capacities of the edge
                while idx < len(path) - 1:
                    edge = self.__getEdgeFromNodeIDs(path, idx)
                    tempMinCap, addedFlow = edge.getTempMinCap(), edge.getAddedFlow()
                    
                    if maxFlowLeft == -1:
                        maxFlowLeft = edge.getMaxCap() - addedFlow
                        tempMinFlow = tempMinCap - addedFlow
                    elif tempMinCap - addedFlow > tempMinFlow and tempMinCap - addedFlow - tempMinFlow <= maxFlowLeft:
                        originalTempMinFlow = tempMinFlow
                        tempMinFlow = tempMinCap - addedFlow
                        maxFlowLeft -= (tempMinFlow - originalTempMinFlow)
                    elif tempMinCap - addedFlow > tempMinFlow and tempMinCap - addedFlow - tempMinFlow > maxFlowLeft:
                        tempMinFlow += maxFlowLeft
                        maxFlowLeft = 0
                    elif edge.getMaxCap() - addedFlow < maxFlowLeft:
                        maxFlowLeft = edge.getMaxCap() - addedFlow

                    if edge.getMaxCap() - addedFlow - tempMinFlow < 0:
                        tempMinFlow -= abs(edge.getMaxCap() - addedFlow - tempMinFlow)
                        maxFlowLeft += abs(edge.getMaxCap() - addedFlow - tempMinFlow)

                    if tempMinCap - addedFlow > 0:
                        count += 1

                    idx += 1

                for nodeID in path:
                    node = self.__getNode(self.__nodeRelDict[nodeID])
                    if node.getNodeCap() > 0 and node.getNodeCap() - node.getFlowThroughNodeCap() < tempMinFlow:
                        tempMinFlow = node.getNodeCap() - node.getFlowThroughNodeCap()
                        maxFlowLeft = 0
                        
                if tempMinFlow > 0 and maxFlowLeft >= 0:
                    changesMade = True

                    # Finds the path which goes through the most edges that is valid
                    if bestFlow == []:
                        bestFlow = [path, tempMinFlow, count]
                    elif bestFlow[2] < count or (bestFlow[2] == count and bestFlow[1] < tempMinFlow):
                        bestFlow = [path, tempMinFlow, count]

            if changesMade:
                found = False
                path, tempMinFlow, count = bestFlow
                
                self.__updateAddedFlows(path, tempMinFlow)
                newTotal += tempMinFlow
                    
                for idx, (existingPath, existingFlow) in enumerate(minimumPaths):
                    if existingPath == path:
                        found = True
                        minimumPaths[idx][1] += tempMinFlow
                
                if not found:  
                    minimumPaths.append([path, tempMinFlow])

        return [minimumPaths, newTotal]

    def __getMaximumFlows(self, paths, newTotal):
        maximumPaths = []
        
        for path in paths:
            tempMaxFlow = 1000
            idx = 0

            while idx < len(path) - 1:
                edge = self.__getEdgeFromNodeIDs(path, idx)

                if edge.getMaxCap() - edge.getAddedFlow() < tempMaxFlow:
                    tempMaxFlow = edge.getMaxCap() - edge.getAddedFlow()
                
                idx += 1

            for nodeID in path:
                node = self.__getNode(self.__nodeRelDict[nodeID])
                if node.getNodeCap() > 0 and node.getNodeCap() - node.getFlowThroughNodeCap() < tempMaxFlow:
                    tempMaxFlow = node.getNodeCap() - node.getFlowThroughNodeCap()

            if tempMaxFlow > 0:
                maximumPaths.append([deepcopy(path), tempMaxFlow])
                newTotal += tempMaxFlow

                self.__updateAddedFlows(path, tempMaxFlow)

        return [maximumPaths, newTotal]

    def __updateAddedFlows(self, path, flow):
        for i in range(len(path) - 1):
            edge = self.__getEdgeFromNodeIDs(path, i)
            edge.updateAddedFlow(flow)

        for nodeID in path:
            node = self.__getNode(self.__nodeRelDict[nodeID])
            if node.getNodeCap() > 0:
                node.updateFlowThroughNodeCap(flow)

    def __shuffle(self, paths):
        oldOrder = deepcopy(paths)
        newOrder = []

        while len(oldOrder) != 0:
            randIdx = randint(0, len(oldOrder) - 1)
            element = oldOrder.pop(randIdx)
            newOrder.append(element)

        return newOrder

    def __shiftMax2MinFlows(self, userAddedPath, minFlowVal, maxPathIns, delMinPathIdxs, idx, flowsToDel):
        minPathFound = True
        
        recordIdx = self.__maxFlowScrollbar.findElement(userAddedPath)
        path, flow = self.__maxFlowScrollbar.getElement(recordIdx)
        self.__maxFlowScrollbar.delRecord(recordIdx)
        self.__additionalTotal -= min(minFlowVal, int(flow))
        
        if self.__additionalTotal == 0:
            self.__maxFlowScrollbar.delRecord(0)
        self.__maxFlowScrollbar.updateHeader(f"Max Flow - Total = {self.__additionalTotal}")
        
        if self.__minFlowScrollbar.getLenDispData() == 0:
            self.__minFlowScrollbar.insertRecords(0, ["Path", "Flow"])
            
        path = self.__updatePath(path.split())
        self.__minFlowScrollbar.insertRecords(-1, [path, str(min(minFlowVal, int(flow)))])
        self.__minFlowTotal += min(minFlowVal, int(flow))
        self.__minFlowScrollbar.updateHeader(f"Min Flow - Total = {self.__minFlowTotal}")
        newFlow = int(flow) - min(minFlowVal, int(flow))
        
        if newFlow > 0:
            self.__maxFlowScrollbar.insertRecords(recordIdx, [path, str(newFlow)])
            maxPathIns.append([path, newFlow])
            
        self.__minimumPaths[idx][1] -= min(minFlowVal, int(flow))
        if self.__minimumPaths[idx][1] <= 0:
            delMinPathIdxs.append(idx)
            
        flowsToDel[userAddedPath] -= minFlowVal

        return [minPathFound, maxPathIns, delMinPathIdxs, flowsToDel]

    def __updatePath(self, path):
        if self.__isSupersource:
            path.insert(0, self.__addedNodes[0].getNodeID())
        if self.__isSupersink:
            path.append(self.__addedNodes[1].getNodeID())

        path = ",".join(path)
            
        return path
        
    def __editPhase(self, eventList):
        for idx, inputBox in enumerate(self.__nodeInpBoxes):
            change = inputBox.updateInputs(eventList)
            if inputBox.getActive() and change:
                self.__resetOtherActiveNodes(idx)
    
        for idx, inputBox in enumerate(self.__edgeInpBoxes):
            change = inputBox.updateInputs(eventList)
            if inputBox.getActive() and change:
                self.__resetOtherActiveEdges(idx)

        for idx, inputBox in enumerate(self.__flowInpBoxes):
            change = inputBox.updateInputs(eventList)
            if inputBox.getActive() and change:
                self.__resetOtherActiveFlows(idx)

        if self.__addNodeButton.handleEvents(eventList):
            self.__createNode()
            for inputBox in self.__nodeInpBoxes:
                inputBox.resetTxt()
            
        if self.__addEdgeButton.handleEvents(eventList):
            self.__createEdge()
            for inputBox in self.__edgeInpBoxes:
                inputBox.resetTxt()

        if self.__addFlowButton.handleEvents(eventList):
            self.__updateFlow()
            for inputBox in self.__flowInpBoxes:
                inputBox.resetTxt()

        self.__handleDelButtons(eventList)
        self.__shiftScrollbars()

    def __resetOtherActiveNodes(self, activeIdx):
        for idx, inputBox in enumerate(self.__nodeInpBoxes):
            if idx != activeIdx:
                inputBox.resetActive()

    def __resetOtherActiveEdges(self, activeIdx):
        for idx, inputBox in enumerate(self.__edgeInpBoxes):
            if idx != activeIdx:
                inputBox.resetActive()

    def __resetOtherActiveFlows(self, activeIdx):
        for idx, inputBox in enumerate(self.__flowInpBoxes):
            if idx != activeIdx:
                inputBox.resetActive()

    def __handleDelButtons(self, eventList):
        for k, delButton in enumerate(self.__delButtons):
            if delButton.handleEvents(eventList) and k + 1 <= self.__dispInfoScrollbar.getLenData():
                # Converts Y ==> record no vertically down
                Y = delButton.getY()
                idx = ((Y - self.__dispInfoScrollbar.getY())//20) + self.__dispInfoScrollbar.getStartIdx()
                ID = self.__getIDFromRecord(self.__dispInfoScrollbar.getElement(idx))
                self.__dispInfoScrollbar.delRecord(idx - self.__dispInfoScrollbar.getStartIdx())
                
                edgeref, idxToDel = [], []
                # Flags any associated edges to node or edge
                for idx, edge in enumerate(self.__edges):
                    edgeInfoStr = f"{SMALLPAD*EMPTYSTRING}EDGE - From:  {edge.getFromNode()}"
                    edgeInfoStr += f"To:  {edge.getToNode()} Min cap:  {edge.getMinCap()} Max cap:  {edge.getMaxCap()}"
                    if ID == (edge.getFromNode() + edge.getToNode()):
                        edgeref.append([edge.getFromNode(), edge.getToNode(), edge.getEdgeID()])
                        idxToDel.append(idx)

                    elif edge.getFromNode() == ID or edge.getToNode()==ID:
                        edgeref.append([edge.getFromNode(), edge.getToNode(), edge.getEdgeID()])
                        j = self.__dispInfoScrollbar.findElement(edgeInfoStr)
                        self.__dispInfoScrollbar.delRecord(j - self.__dispInfoScrollbar.getStartIdx())
                        idxToDel.append(idx)

                # Deletes node/ incoming or outgoing edges
                nodeIdxToRemove = []
                for idx, node in enumerate(self.__nodes):
                    if node == ID:
                        nodeIdxToRemove.append(idx)
                    for i, edgeInfo in enumerate(edgeref):
                        fromNode, toNode, edgeID = edgeInfo
                        if node.getNodeID() == toNode:
                            self.__nodes[idx].delIncomingEdge(edgeID)
                        elif node.getNodeID() == fromNode:
                            self.__nodes[idx].delOutgoingEdge(edgeID)

                nodeIdxToRemove = nodeIdxToRemove[::-1]
                for idx in nodeIdxToRemove:
                    del self.__nodes[idx]

                # Removes added flow if node/ edge is in path
                removeIdx = []
                for idx in range(len(self.__addedFlows)):
                    for node in self.__addedFlows[idx][0]:
                        if ID == node:
                            removeIdx.append(idx)

                    for i in range(len(self.__addedFlows[idx][0])-1):
                        if ID == self.__addedFlows[idx][0][i] + self.__addedFlows[idx][0][i+1]:
                            removeIdx.append(idx)
                            
                removeIdx = removeIdx[::-1]
                for each in removeIdx:
                    path, flow = self.__addedFlows[each]
                    recordIdx = self.__maxFlowScrollbar.findElement(",".join(path))
                    self.__additionalTotal -= int(flow)
                    self.__maxFlowScrollbar.delRecord(recordIdx)
                    if self.__maxFlowScrollbar.getLenDispData() == 1:
                        self.__maxFlowScrollbar.delRecord(0)
                    
                    for idx in range(len(self.__addedFlows[each][0])-1):
                        for edge in self.__edges:
                            fromNodeID, toNodeID = self.__addedFlows[each][0][idx], self.__addedFlows[each][0][idx + 1]
                            if edge.getFromNode() == fromNodeID and edge.getToNode() == toNodeID:
                                edge.addFlow(-self.__addedFlows[each][1])
                    self.__addedFlows.pop(each)

                idxToDel = idxToDel[::-1]
                for each in idxToDel:
                    del self.__edges[each]

                self.__checkMinCap()

                # Converts Node type if required
                for idx, node in enumerate(self.__nodes):
                    if ((node.getNoOutgoingEdges() >= 1 and node.getNoIngoingEdges() == 0) or
                        (node.getNoOutgoingEdges() == 0 and node.getNoIngoingEdges() >= 1)):
                        if node.getType() == "Node":
                            X, Y = node.getCoords()
                            sourceOrSink = SourcesOrSinks(node.getNodeID(), node.getNodeCap(),
                                                          X, Y, node.getIncomingEdges(), node.getOutgoingEdges())
                            self.__nodes.insert(idx + 1, sourceOrSink)
                            self.__nodes.pop(idx)

    def __getIDFromRecord(self, string):
        info = string.lstrip()
        infoInParts = info.replace(":", " ").split()
        if info[:4] == "NODE":
            return infoInParts[4]
        elif info[:4] == "EDGE":
            edgeID = infoInParts[3] + infoInParts[5]
            return edgeID
        
    def __solvePhase(self, eventList):
        buttonPressed = False
        # Enable stepped max flows to be added 
        if self.__nextButton.handleEvents(eventList): 
            buttonPressed = self.__addNextFlow()

        if self.__supersourceButton.handleEvents(eventList) and not self.__supersourceButton.getIfHidden():
            buttonPressed = True

        if self.__supersinkButton.handleEvents(eventList) and not self.__supersinkButton.getIfHidden():
            buttonPressed = True

        if self.__nodeCapButton.handleEvents(eventList) and not self.__nodeCapButton.getIfHidden():
            buttonPressed = True

        # Handles ammendments to cuts on screen
        if not buttonPressed:
            self.__handleAmmendments2Cut(eventList)
            
            if self.__isSupersource and self.__ammendment:
                if self.__supersourceButton.getCurrentPhase() == "Show Supersource":
                    self.__supersourceButton.changePhase()
            if self.__isSupersink and self.__ammendment:
                if self.__supersinkButton.getCurrentPhase() == "Show Supersink":
                    self.__supersinkButton.changePhase()
            if self.__ifNodeCap and self.__ammendment:
                if self.__nodeCapButton.getCurrentPhase() == "Show Node Cap":
                    self.__nodeCapButton.changePhase()
            self.__ammendment = False

        # Hides/shows cuts                    
        collision = False
        for cutIDButton in self.__showCutIDButtons:
            if cutIDButton.handleEvents(eventList) and not collision:
                Y = cutIDButton.getY()
                idx = (Y-self.__cutIDScrollbar.getY())//20
                
                ID = self.__cutIDScrollbar.getElement(idx + self.__cutIDScrollbar.getStartIdx() - 1) 
                collision = True

                for i, cut in enumerate(self.__cuts):
                    if ID == cut.getCutID():
                        self.__cuts[i].updateCanDraw()

        self.__cutIDScrollbar.handleEvents(eventList)
        self.__dispCutInfoScrollbar.handleEvents(eventList)
        self.__shiftScrollbars()

    def __addNextFlow(self):
        buttonPressed = True
        if len(self.__pathsToRemove) != 0:
            path, flow = self.__pathsToRemove.pop(0)
            self.__addRecordToMaxFlow(path.split(","), flow)
        elif len(self.__minimumPaths) != 0:
            path, flow = self.__minimumPaths.pop(0)

            # Update edges within current path
            idx = 0
            while idx < len(path) - 1:
                edge = self.__getEdgeFromNodeIDs(path, idx)
                edge.addFlow(flow)
                if edge.getFwFlow() - edge.getMinCap() - edge.getInitialMaxFlow() > 0:
                    edge.raiseMinCap(edge.getFwFlow() - edge.getMinCap() - edge.getInitialMaxFlow())

                idx += 1

            path = self.__handleAddedNodeCaps(path, flow)

            # Changes scrollbar to account for added path
            if self.__minFlowScrollbar.getLenDispData() == 0:
                self.__minFlowScrollbar.insertRecords(0, ["Path", "Flow"])
            pathStr = ",".join(path)
            self.__minFlowScrollbar.insertRecords(-1, [pathStr, str(flow)])
            self.__minFlowTotal += flow
            self.__minFlowScrollbar.updateHeader(f"Min Flow - Total = {self.__minFlowTotal}")
                
        elif len(self.__maximumPaths) != 0:
            path, flow = self.__maximumPaths.pop(0)
            self.__addRecordToMaxFlow(path, flow)

        if len(self.__pathsToRemove) == 0 and len(self.__minimumPaths) == 0 and len(self.__maximumPaths) == 0:
            self.__maxFlowTotal = self.__additionalTotal + self.__minFlowTotal

        return buttonPressed

    def __addRecordToMaxFlow(self, path, flow):
        # Update edges within current path
        idx = 0
        while idx < len(path) - 1:
            edge = self.__getEdgeFromNodeIDs(path, idx)
            edge.addFlow(flow)

            idx += 1
            
        path = self.__handleAddedNodeCaps(path, flow)
        
        if self.__maxFlowScrollbar.getLenDispData() == 0:
            self.__maxFlowScrollbar.insertRecords(0, ["Path", "Flow"])
        pathStr = ",".join(path)

        # Changes scrollbar to account for added path
        if self.__maxFlowScrollbar.getElement(self.__maxFlowScrollbar.findElement(pathStr))[0] != pathStr:
            self.__maxFlowScrollbar.insertRecords(-1, [pathStr, str(flow)])
        else:
            existingRecordID = self.__maxFlowScrollbar.findElement(pathStr)
            existingPath, existingFlow = self.__maxFlowScrollbar.getElement(existingRecordID)
            newFlow = int(existingFlow) + int(flow)
            self.__maxFlowScrollbar.delRecord(existingRecordID)
            if newFlow > 0:
                self.__maxFlowScrollbar.insertRecords(existingRecordID, [pathStr, str(newFlow)])
            elif self.__maxFlowScrollbar.getLenData() == 1:
                self.__maxFlowScrollbar.delRecord(0)

        self.__additionalTotal += flow
        self.__maxFlowScrollbar.updateHeader(f"Max Flow - Total = {self.__additionalTotal}")

    def __handleAddedNodeCaps(self, path, flow):
        # Updates path to include node cap ID's
        i = 0
        while i < len(path):
            node = self.__getNode(self.__nodeRelDict[path[i]])
            if node.getNodeCapRef() != "" and node.getNodeCap() > 0:
                path[i] = f"{node.getNodeID()}-1"
                path.insert(i + 1, f"{node.getNodeID()}-2")

            i += 1

        # Only updates the flow of edges with node cap ID
        edgesAdded = []
        idx = 0
        while idx < len(path) - 1:
            if ("-1" in path[idx] or "-2" in path[idx] or "-1" in path[idx + 1] or "-2" in path[idx + 1]):
                if not [path[idx], path[idx + 1]] in edgesAdded:
                    edge = self.__getEdgeFromNodeIDs(path, idx)
                    edgesAdded.append([path[idx], path[idx + 1]])
                    edge.addFlow(flow)

            idx += 1

        return path

    def __handleAmmendments2Cut(self, eventList):
        mousePosX, mousePosY = pg.mouse.get_pos()
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and (len(self.__cuts) == 0 or self.__cuts[-1].getIfFixed()):
                smallestXPos = self.__graphDispBorder.getX() + SMALLPAD
                largestXPos = self.__graphDispBorder.getX() + self.__graphDispBorder.getW() - SMALLPAD
                smallestYPos = self.__graphDispBorder.getY() + SMALLPAD
                largestYPos = self.__graphDispBorder.getY() + self.__graphDispBorder.getH() - SMALLPAD
                
                if mousePosX >= smallestXPos and mousePosX <= largestXPos:
                    if mousePosY >= smallestYPos and mousePosY <= largestYPos:
                        cut = Cut(smallestXPos, largestXPos, smallestYPos, largestYPos)
                        self.__cuts.append(cut)
                        self.__ammendment = True
                        
            elif len(self.__cuts) > 0 and not self.__cuts[-1].getIfFixed():
                ifFixed = self.__cuts[-1].handleEvents(event)
                if ifFixed:
                    if self.__cuts[-1].getNoOfLines() == 0:
                        Cut.decreaseID()
                        self.__cuts.pop(-1)
                    else:
                        invalid = self.__analyseCut()
                        if not invalid:
                            if self.__minCutTotal == 0 or self.__minCutTotal > self.__cuts[-1].getCutValue():
                                self.__minCutTotal = self.__cuts[-1].getCutValue()
                else:
                    self.__ammendment = True

    def __shiftScrollbars(self):
        if self.__ifMinCap and self.__minFlowScrollbar.getLenDispData() != 0 and self.__maxFlowScrollbar.getLenDispData() != 0:
            self.__minFlowScrollbar.changeX(self.__minFlowCoordsPoss[1])
            self.__maxFlowScrollbar.changeX(int(self.__maxFlowCoordsPoss[1]))
        else:
            if self.__minFlowScrollbar.getLenDispData() == 0:
                self.__maxFlowScrollbar.changeX(self.__maxFlowCoordsPoss[0])
            else:
                self.__minFlowScrollbar.changeX(int(self.__minFlowCoordsPoss[0]))
    
    def __draw(self):
        self.__drawBorders()
        self.__drawInputBoxHeadings()

        for inputBox in self.__nodeInpBoxes:
            inputBox.draw()

        for inputBox in self.__edgeInpBoxes:
            inputBox.draw()

        for inputBox in self.__flowInpBoxes:
            inputBox.draw()

        self.__addNodeButton.draw()
        self.__addEdgeButton.draw()
        self.__addFlowButton.draw()
        
        if self.__phase == "EditPhase":
            # Draws graph to guide user to correct coordinates for each node/edge
            self.__drawGraphAxes()

            for idx in range(self.__dispInfoScrollbar.getLenDispData()):
                self.__delButtons[idx].draw()
                
        elif self.__phase == "SolvePhase":
            self.__nextButton.draw()
            if self.__isSupersource:
                self.__supersourceButton.draw()
            if self.__isSupersink:
                self.__supersinkButton.draw()
            if self.__ifNodeCap:
                self.__nodeCapButton.draw()

            if len(self.__cuts) != 0:
                for cut in self.__cuts:
                    cut.draw()
    
            self.__cutIDScrollbar.display()
            self.__dispCutInfoScrollbar.display()

            startIdx = 0       
            for idx in range(self.__cutIDScrollbar.getLenDispData()):
                if self.__cutIDScrollbar.getStartIdx() != 0:
                    startIdx = self.__cutIDScrollbar.getStartIdx()
                self.__showCutIDButtons[startIdx + idx].changePos(self.__cutIDScrollbar.getX() + self.__cutIDScrollbar.getW(),
                                                self.__cutIDScrollbar.getY() + (idx + 1)*20)
                self.__showCutIDButtons[startIdx + idx].draw()
                
        # Drawn in both phases
        self.__drawEdgesAndNodes()
        self.__drawThereomProved()

        self.__minFlowScrollbar.display()
        self.__maxFlowScrollbar.display()
        self.__errorScrollbar.display()
        self.__aidScrollbar.display()
        self.__dispInfoScrollbar.display()

        if self.__additionalTotal > 0 or self.__minFlowTotal > 0:  
            totalFlowLabel = TITLEFONT.render(f"Total flow = {self.__minFlowTotal + self.__additionalTotal}", 2, BLACK)
            textRect = totalFlowLabel.get_rect()
            centreX = self.__maxFlowBorder.getX() + self.__maxFlowBorder.getW()/2
            centreY = self.__maxFlowBorder.getY() + self.__maxFlowBorder.getH() - 3*SMALLPAD
            textRect.center = (centreX, centreY)
            SCREEN.blit(totalFlowLabel, textRect)

        self.__solveOrEditButton.draw()

    def __drawBorders(self):
        self.__dispInfoBorder.draw()
        self.__inpNodeBorder.draw()
        self.__inpEdgeBorder.draw()
        self.__inpFlowBorder.draw()
        self.__dispCutBorder.draw()
        self.__maxFlowBorder.draw()
        self.__minCutBorder.draw()
        self.__graphDispBorder.draw()
        self.__aidBorder.draw()
        self.__errorBorder.draw()

    def __drawInputBoxHeadings(self):
        # Displays all titles for input box sections
        nodeLabel, edgeLabel = TITLEFONT.render("Node:", 2, BLACK), TITLEFONT.render("Edge:", 2, BLACK)
        flowLabel = MEDIUMFONT.render("Augmented flow:", 2, BLACK)
        
        SCREEN.blit(nodeLabel, (self.__inpNodeBorder.getX() + SMALLPAD, self.__inpNodeBorder.getY() + SMALLPAD))
        SCREEN.blit(edgeLabel, (self.__inpEdgeBorder.getX() + SMALLPAD, self.__inpEdgeBorder.getY() + SMALLPAD))
        SCREEN.blit(flowLabel, (self.__inpFlowBorder.getX() + SMALLPAD, self.__inpFlowBorder.getY()))

        # Displays node headings for boxes
        nodeIDLabel, nodeCapLabel = FONT.render("Node ID:", 2, BLACK), FONT.render("Node Cap:", 2, BLACK)
        XCoordLabel, YCoordLabel = FONT.render("X:", 2, BLACK), FONT.render("Y:", 2, BLACK)
        
        SCREEN.blit(nodeIDLabel, (self.__inpNodeBorder.getX() + 15, self.__inpNodeBorder.getY() + LARGEPAD))
        SCREEN.blit(nodeCapLabel, (self.__inpNodeBorder.getX() + 105, self.__inpNodeBorder.getY() + LARGEPAD))
        SCREEN.blit(XCoordLabel, (self.__inpNodeBorder.getX() + 195, self.__inpNodeBorder.getY() + LARGEPAD))
        SCREEN.blit(YCoordLabel, (self.__inpNodeBorder.getX() + 250, self.__inpNodeBorder.getY() + LARGEPAD))

        # Displays edge headings for input boxes
        fromNodeIDLabel, toNodeIDLabel = FONT.render("From:", 2, BLACK), FONT.render("To:", 2, BLACK)
        minCapLabel, maxCapLabel = FONT.render("Min Cap:", 2, BLACK), FONT.render("Max Cap:", 2, BLACK)
        
        SCREEN.blit(fromNodeIDLabel, (self.__inpEdgeBorder.getX() + 12, self.__inpEdgeBorder.getY() + LARGEPAD))
        SCREEN.blit(toNodeIDLabel, (self.__inpEdgeBorder.getX() + 88, self.__inpEdgeBorder.getY() + LARGEPAD))
        SCREEN.blit(minCapLabel, (self.__inpEdgeBorder.getX() + 150, self.__inpEdgeBorder.getY() + LARGEPAD))
        SCREEN.blit(maxCapLabel, (self.__inpEdgeBorder.getX() + 223, self.__inpEdgeBorder.getY() + LARGEPAD))

        #Displays augmented flow headings for input boxes
        pathLabel, flowLabel = FONT.render("Path:", 2, BLACK), FONT.render("Flow:", 2, BLACK)
        SCREEN.blit(pathLabel, (self.__inpFlowBorder.getX() + 12, self.__inpFlowBorder.getY() + MEDIUMPAD))
        SCREEN.blit(flowLabel, (self.__inpFlowBorder.getX() + 220, self.__inpFlowBorder.getY() + MEDIUMPAD))

    def __drawGraphAxes(self):
        startX, startY = self.__graphDispBorder.getX() + LARGEPAD, self.__graphDispBorder.getY() - LARGEPAD

        # Draw vertical lines in horizontal directions with numbering 
        for i in range(self.__graphDispBorder.getW()//GRIDLINEGAPS + 1):
            line = pg.Rect(startX + i*GRIDLINEGAPS, startY, 1, self.__graphDispBorder.getH())
            if i == 0:
                pg.draw.rect(SCREEN, LIGHTERGREY, line)
            else:
                pg.draw.rect(SCREEN, DARKGREY, line)

            num = FONT.render(str(i), 2, BLACK)
            SCREEN.blit(num, (startX + i*GRIDLINEGAPS, startY + self.__graphDispBorder.getH() + SMALLPAD))

        # Resets start Y coordinate as vertical lines can only be drawn down the screen 
        startY = self.__graphDispBorder.getY() + self.__graphDispBorder.getH() - LARGEPAD

        # Draw horizontal lines in vertical directions with numbering 
        for i in range(self.__graphDispBorder.getH()//(GRIDLINEGAPS)+1):
            line = pg.Rect(startX, startY - i*GRIDLINEGAPS, self.__graphDispBorder.getW(), 1)
            if i == 0:
                pg.draw.rect(SCREEN, LIGHTERGREY, line)
            else:
                pg.draw.rect(SCREEN, DARKGREY, line)

            num = FONT.render(str(i), 2, BLACK)
            SCREEN.blit(num, (startX - 2*SMALLPAD, startY - i*GRIDLINEGAPS))

    def __drawEdgesAndNodes(self):
        nodeCapDrawn = False
        for node in self.__nodes:
            # Allows added node cap nodes and edges to be drawn without associated nodes and edges also being drawn
            if self.__phase == "SolvePhase" and node.getNodeCapRef() != "" and self.__nodeCapButton.getCurrentPhase() == "Hide Node Cap":
                nodeCapDrawn = True
                for each in self.__addedNodes[2][node.getNodeCapRef()]:
                    each.draw()
                for each in self.__addedEdges[2][node.getNodeCapRef()]:
                    if any([(each.getToNode() == "T" and self.__supersinkButton.getCurrentPhase() == "Hide Supersink"),
                            (each.getFromNode() == "S" and self.__supersourceButton.getCurrentPhase() == "Hide Supersource"),
                            (each.getFromNode() != "S" and each.getToNode() != "T")]):
                        
                        each.draw(self.__ifMinCap)
         
            else:  
                node.draw()

        for edge in self.__edges:
            if (not edge.getPartOfNodeCap() and nodeCapDrawn) or not nodeCapDrawn:
                edge.draw(self.__ifMinCap)
        
        if self.__isSupersource:
            if self.__supersourceButton.getCurrentPhase() == "Hide Supersource":
                self.__addedNodes[0].draw()
                for each in self.__addedEdges[0]:
                    # Only draws if assoiated node cap edge if one, is not drawn
                    if not (self.__ifNodeCap and self.__nodeCapButton.getCurrentPhase() == "Hide Node Cap" and each.getPartOfNodeCap()):
                        each.draw(self.__ifMinCap)
                    
        if self.__isSupersink:
            if self.__supersinkButton.getCurrentPhase() == "Hide Supersink":
                self.__addedNodes[1].draw()
                for each in self.__addedEdges[1]:
                    # Only draws if assoiated node cap edge if one, is not drawn
                    if not (self.__ifNodeCap and self.__nodeCapButton.getCurrentPhase() == "Hide Node Cap" and each.getPartOfNodeCap()):
                        each.draw(self.__ifMinCap)

    def __drawThereomProved(self):
        if self.__maxFlowTotal == self.__minCutTotal and self.__maxFlowTotal != 0:
            self.__theoremProvedBorder.draw()
            self.__theoremProvedBorder.drawOutline()
            msgLabel = TITLEFONT.render(f"Optimal flow is: {self.__minCutTotal}", 2, BLACK)
            textRect = msgLabel.get_rect()
            centreX = self.__theoremProvedBorder.getX() + self.__theoremProvedBorder.getW()/2
            centreY = self.__theoremProvedBorder.getY() + self.__theoremProvedBorder.getH()/2
            textRect.center = (centreX, centreY)
            SCREEN.blit(msgLabel, textRect)

    def __createNode(self):
        self.__invalidInput, collisions = False, False
        nodeInfo = []

        for inputBox in self.__nodeInpBoxes:
            if inputBox.getTxt() != "":
                nodeInfo.append(inputBox.getTxt())
            elif inputBox.getID() == "Node Cap":
                nodeInfo.append(inputBox.getDefaultTxt())
            else:
                self.__addErrorMsg("Not all required node inputs were completed")
                return
        
        # nodeInfo[0] = node ID, nodeInfo[1] = node cap, nodeInfo[3] = X, nodeInfo[4] = Y
        match = False
        for each in self.__reservedNodeIDs:
            if each == nodeInfo[0]:
                match = True
        if match:
            self.__addErrorMsg("ID reserved")
            
        for node in self.__nodes:
            if node == nodeInfo[0]:
                self.__addErrorMsg("Node ID can't be repeated")
                
        nodeInfo[1] = int(nodeInfo[1])
        if nodeInfo[1] > 30:
            self.__addErrorMsg("Node cap is too high")
            
        try:
            nodeInfo[2], nodeInfo[3] = self.__validateCoords(nodeInfo[2], nodeInfo[3])
            if self.__validateNewNodeWithOtherNodes(nodeInfo[2], nodeInfo[3], True):
                collisions = True
            if self.__validateNewNodeWithEdge(nodeInfo[2], nodeInfo[3], True):
                collisions = True
        except TypeError:
            self.__addErrorMsg("Coords are not within given paramaters")

        if not self.__invalidInput and not collisions:
            node = SourcesOrSinks(nodeInfo[0], nodeInfo[1], nodeInfo[2], nodeInfo[3])
            self.__nodes.append(node)
            self.__dispInfoScrollbar.insertRecords(-1, f"NODE - Node ID: {nodeInfo[0]} Node cap: {nodeInfo[1]}")
                
    def __addErrorMsg(self, errorMsg):
        self.__invalidInput = True
        self.__errorScrollbar.insertRecords(-1, errorMsg)
            
    def __validateCoords(self, strX, strY):
        if strX != "0" and strY != "0":
            X, Y = float(strX), float(strY)
            X, Y = self.__convertX2Pixels(X), self.__convertY2Pixels(Y)
            
            if all([X < self.__graphDispBorder.getX() + self.__graphDispBorder.getW() - RADIUS,
                    X > self.__graphDispBorder.getX() + RADIUS,
                    Y < self.__graphDispBorder.getH() - RADIUS,
                    Y > RADIUS]):
                
                return [X, Y]

    # Arbitary x coord ==> coord in pixels
    def __convertX2Pixels(self, X):
        return (X * GRIDLINEGAPS) + self.__graphDispBorder.getX() + LARGEPAD

    # Arbitary y coord ==> coord in pixels
    def __convertY2Pixels(self, Y):
        return self.__graphDispBorder.getH() - (Y * GRIDLINEGAPS) - LARGEPAD

    def __validateNewNodeWithEdge(self, X, Y, userInput, nodeCapID = False):
        collisions = False
        idx = 0

        # Gets a list of all edges
        allEdges = []
        for edge in self.__edges:
            if edge.getToNode() != nodeCapID and edge.getFromNode() != nodeCapID:
                allEdges.append(edge)

        for i, edges in enumerate(self.__addedEdges):
            for edge in edges:
                if i != 2:
                    allEdges.append(edge)
                else:
                    for each in edge:
                        allEdges.append(each)
        
        while idx < len(allEdges) and not collisions:
            edge = allEdges[idx]

            # Checks collision with main arrow
            x1, y1 = edge.getStartCoords()
            x2, y2 = edge.getEndCoords()  
            if self.__collisionDetectionNodeAndEdge(x1, y1, x2, y2, X, Y):
                collisions = True

            # Checks collision with fw arrow
            detectionBoxCoordsX, detectionBoxCoordsY = edge.getSmallFwArrowCoords()
            vertices = []
            for coordX in detectionBoxCoordsX:
                for coordY in detectionBoxCoordsY:
                    vertices.append([coordX, coordY])

            for j, vertex1 in enumerate(vertices):
                for k in range(j + 1, len(vertices)):
                    vertex2 = vertices[k]
                    if (vertex1[0] in vertex2 and not vertex1[1] in vertex2) or (
                        not vertex1[0] in vertex2 and vertex1[1] in vertex2):
                        
                        x1, y1 = vertex1
                        x2, y2 = vertex2
                        if self.__collisionDetectionNodeAndEdge(x1, y1, x2, y2, X, Y):
                            collisions = True

            # Checks collision with bw arrow
            detectionBoxCoordsX, detectionBoxCoordsY = edge.getSmallBwArrowCoords()
            vertices = []
            for coordX in detectionBoxCoordsX:
                for coordY in detectionBoxCoordsY:
                    vertices.append([coordX, coordY])

            for j, vertex1 in enumerate(vertices):
                for k in range(j + 1, len(vertices)):
                    vertex2 = vertices[k]
                    if (vertex1[0] in vertex2 and not vertex1[1] in vertex2) or (
                        not vertex1[0] in vertex2 and vertex1[1] in vertex2):
                        
                        x1, y1 = vertex1
                        x2, y2 = vertex2
                        if self.__collisionDetectionNodeAndEdge(x1, y1, x2, y2, X, Y):
                            collisions = True

            idx += 1

        if collisions and userInput:
            self.__addErrorMsg("Node collides with atleast one edge")

        return collisions

    def __collisionDetectionNodeAndEdge(self, x1, y1, x2, y2, X, Y):
        # Determines if gradient is in j direction (undefined)
        if x2 != x1:
            m = (y2 - y1)/(x2 - x1)
            c = -m*x1 + y1

            shortestDist = abs(-m*X + Y - c)//((1 + (m)**2)**0.5)
            # checks if shortest distance collides with node with the edge coordinates
            if shortestDist - RADIUS - SMALLPAD <= 0 and X >= min(x1,x2) - RADIUS and X <= max(x1, x2) + RADIUS:
                if Y >= min(y1, y2) - RADIUS and Y <= max(y1, y2) + RADIUS:          
                    return True
        else:
            m, c = "Inf", x2
    
            # checks if node intersects within the edge coordinates
            if c <= X + RADIUS + SMALLPAD and c >= X - RADIUS - SMALLPAD and y1 >= Y - RADIUS - SMALLPAD and y2 <= Y + RADIUS + SMALLPAD:
                return True

    def __validateNewNodeWithOtherNodes(self, newNodeX, newNodeY, userInput, minDistance = 40, otherNodes = [], nodeCapID = False):
        idx = 0
        collisions = False

        # Gets a list of all nodes
        if otherNodes == []:
            allNodes = self.__nodes
        else:
            allNodes = self.__nodes + otherNodes

        if self.__addedNodes[2] != []:
            for setOfNodes in self.__addedNodes[2]:
                allNodes = allNodes + setOfNodes
            
        while idx < len(allNodes) and not collisions:
            if allNodes[idx].getNodeID() != nodeCapID:
                oldNodeX, oldNodeY = allNodes[idx].getCoords()

                # Checks if shortest distance is too small
                distBetweenNodes = ((newNodeX - oldNodeX)**2 + (newNodeY - oldNodeY)**2)**0.5
                if distBetweenNodes < 2*RADIUS + minDistance:
                    collisions = True     

            idx += 1

        if userInput and collisions:
            self.__addErrorMsg("Nodes must not touch")
            
        return collisions

    def __createEdge(self):
        self.__invalidInput = False
        edgeInfo = []

        for inputBox in self.__edgeInpBoxes:
            if inputBox.getTxt() != "":
                edgeInfo.append(inputBox.getTxt())
            elif inputBox.getID() == "Min Cap":
                edgeInfo.append(inputBox.getDefaultTxt())
            else:
                self.__addErrorMsg("Not all required edge inputs were completed")
                return

        # edgeInfo[0] = from Node ID, edgeInfo[1] = to Node ID, edgeInfo[2] = min cap, edgeInfo[3] = max cap
        nodeIdxs = self.__validateEdgeInp(edgeInfo)

        if not self.__invalidInput:
            for idx in nodeIdxs:
                if self.__nodes[idx] == edgeInfo[0]:
                    startX, startY = self.__nodes[idx].getCoords()
                elif self.__nodes[idx] == edgeInfo[1]:
                    endX, endY = self.__nodes[idx].getCoords()

            startX, startY, endX, endY = self.__shiftStartEndCoordsOfEdge(startX, startY, endX, endY)

            collisions = False
            if self.__validateNewEdgeWithNode(startX, startY, endX, endY, True):
                collisions = True
            if self.__validateNewEdgeWithOtherEdges(startX, startY, endX, endY, True):
                collisons = True 

            if not collisions:
                edge = Edge(edgeInfo[0], edgeInfo[1], edgeInfo[2], edgeInfo[3], startX, startY, endX, endY)
                self.__edges.append(edge)

                for node in self.__nodes:
                    if node == edgeInfo[0]:
                        nodeCap = node.getNodeCap()

                edgeInfoStr = f"{SMALLPAD*EMPTYSTRING}EDGE - From:  {edgeInfo[0]}"
                edgeInfoStr += f" To:  {edgeInfo[1]} Min cap:  {edgeInfo[2]} Max cap:  {edgeInfo[3]}"  
                nodeIdx = self.__dispInfoScrollbar.findElement(f"NODE - Node ID: {edgeInfo[0]} Node cap: {nodeCap}")
                self.__dispInfoScrollbar.insertRecords(nodeIdx + 1, edgeInfoStr)

                if edgeInfo[2] > 0:
                    self.__ifMinCap = True
                    
                for idx in nodeIdxs:
                    currentNode = self.__nodes[idx]
                    if currentNode == edgeInfo[0]:
                        currentNode.addOutgoingEdge(self.__edges[-1].getEdgeID())
                    elif currentNode == edgeInfo[1]:
                        currentNode.addIncomingEdge(self.__edges[-1].getEdgeID())                

                    # Converts to a normal node based on edges
                    if currentNode.getNoOutgoingEdges() >= 1 and currentNode.getNoIngoingEdges() >= 1:
                        if currentNode.getType() == "Source/sink":
                            X, Y = currentNode.getCoords()
                            IncomingEdges = deepcopy(currentNode.getIncomingEdges())
                            OutgoingEdges = deepcopy(currentNode.getOutgoingEdges())
                            node = Node(currentNode.getNodeID(), currentNode.getNodeCap(), X, Y, IncomingEdges, OutgoingEdges)
                            self.__nodes.insert(idx + 1, node)
                            self.__nodes.pop(idx)

    def __validateEdgeInp(self, edgeInfo):
        if edgeInfo[0] == edgeInfo[1]:
            self.__addErrorMsg("An edge can't go to itself")

        # Validates if from and to nodes exist
        nodeIdxs = []
        idx, existingNodesCount = 0, 0
        while idx < len(self.__nodes):
            if self.__nodes[idx] == edgeInfo[0] or self.__nodes[idx] == edgeInfo[1]:
                if not idx in nodeIdxs:
                    existingNodesCount += 1
                    nodeIdxs.append(idx)

            idx += 1
            
        if existingNodesCount != 2:
            self.__addErrorMsg("1 or more of Node ID's do not exist")

        for edge in self.__edges:
            if edge.getFromNode() == edgeInfo[0] and edge.getToNode() == edgeInfo[1]:
                self.__addErrorMsg("Edge already exists")

        edgeInfo[2], edgeInfo[3] = int(edgeInfo[2]), int(edgeInfo[3])
        if edgeInfo[3] == 0 or edgeInfo[3] > 99:
            self.__addErrorMsg("Max cap is either 0 or too high")
        if edgeInfo[2] > 99:
            self.__addErrorMsg("Min cap is too high")
        if edgeInfo[2] > edgeInfo[3]:
            self.__addErrorMsg("Min cap must be less than or equal to max cap")

        return nodeIdxs

    def __shiftStartEndCoordsOfEdge(self, startX, startY, endX, endY):
        # Updates start and end coord of edge based on radius from centre of node
        if startX == endX:
            if startY > endY:
                startY -= RADIUS+SMALLPAD
                endY += RADIUS+SMALLPAD
            elif startY < endY:
                startY += RADIUS+SMALLPAD
                endY -= RADIUS+SMALLPAD
        else:
            m = (endY - startY)/(endX - startX)
            c = -m*startX + startY
            
            angle = atan2(endY - startY, endX - startX)
            if startX > endX:
                startX += (RADIUS + SMALLPAD)*cos(angle)
                endX -= (RADIUS + SMALLPAD)*cos(angle)
            elif startX < endX:
                startX += (RADIUS + SMALLPAD)*cos(angle)
                endX -= (RADIUS + SMALLPAD)*cos(angle)
            startY = m*startX + c
            endY = m*endX + c

        return startX, startY, endX, endY

    def __validateNewEdgeWithOtherEdges(self, startX, startY, endX, endY, userInput, nodeCapID = False):
        collisions = False
        idx = 0

        # Gets a list of all edges
        allEdges = self.__edges + self.__addedEdges[0] + self.__addedEdges[1]
        if self.__addedEdges[2] != []:
            for i, setOfEdges in enumerate(self.__addedEdges[2]):
                #if (nodeCapID != False and i != len(self.__addedEdges[2]) - 1) or nodeCapID == False:
                    allEdges += setOfEdges
        
        if startX != endX:
            m1 = (endY - startY)/(endX - startX)#ckeck for y axis lines
            c1 = -m1*startX + startY
        else:
            m1 = "Inf"
            c1 = startX
                
        while idx < len(allEdges) and not collisions:
            edge = allEdges[idx]

            # Accounts for associated edges to be drawn at different times but collide
            if nodeCapID != edge.getFromNode() and nodeCapID != edge.getToNode():
                x1, y1 = edge.getStartCoords()
                x2, y2 = edge.getEndCoords()

                # Checks collision with main arrow
                if self.__collisionDetectionBetweenEdges(x1, y1, x2, y2, m1, c1, startX, startY, endX, endY):
                    collisions = True

                # Checks collision with fw arrow
                detectionBoxCoordsX, detectionBoxCoordsY = edge.getSmallFwArrowCoords()
                vertices = []
                for coordX in detectionBoxCoordsX:
                    for coordY in detectionBoxCoordsY:
                        vertices.append([coordX, coordY])

                for j, vertex1 in enumerate(vertices):
                    for k in range(j + 1, len(vertices)):
                        vertex2 = vertices[k]
                        if (vertex1[0] in vertex2 and not vertex1[1] in vertex2) or (
                            not vertex1[0] in vertex2 and vertex1[1] in vertex2):
                            
                            x1, y1 = vertex1
                            x2, y2 = vertex2
                            if self.__collisionDetectionBetweenEdges(x1, y1, x2, y2, m1, c1, startX, startY, endX, endY):
                                collisions = True                            

                # Checks collision with bw arrow
                detectionBoxCoordsX, detectionBoxCoordsY = edge.getSmallBwArrowCoords()
                vertices = []
                for coordX in detectionBoxCoordsX:
                    for coordY in detectionBoxCoordsY:
                        vertices.append([coordX, coordY])

                for j, vertex1 in enumerate(vertices):
                    for k in range(j + 1, len(vertices)):
                        vertex2 = vertices[k]
                        if (vertex1[0] in vertex2 and not vertex1[1] in vertex2) or (
                            not vertex1[0] in vertex2 and vertex1[1] in vertex2):
                            
                            x1, y1 = vertex1
                            x2, y2 = vertex2
                            if self.__collisionDetectionBetweenEdges(x1, y1, x2, y2, m1, c1, startX, startY, endX, endY):
                                collisions = True

                fwFlowTextRect, bwFlowTextRect = edge.getFwFlowTextRect(), edge.getBwFlowTextRect()
                if fwFlowTextRect.clipline((startX, startY), (endX, endY)) or bwFlowTextRect.clipline((startX, startY), (endX, endY)):
                    collisions = True

            idx += 1

        if collisions and userInput:
            self.__addErrorMsg("Edge collides with other edges")

        return collisions

    def __collisionDetectionBetweenEdges(self, x1, y1, x2, y2, m1, c1, startX, startY, endX, endY):
        if x2 != x1:
            m2 = (y2 - y1)/(x2 - x1)
            c2 = -m2*x1 + y1
        else:
            m2, c2 = "Inf", x2

        # Checks if 2 vertical lines collides 
        if m2 == "Inf" and m2 == m1:
            if abs(c2 - c1) <= LARGEPAD:
                if (startY >= min(y1, y2) and startY <= max(y1, y2)) or (endY >= min(y1, y2) and endY <= max(y1, y2)):
                    return True
        # Checks if the vertical cut line drawn intersects edge 
        elif m2 == "Inf" and m1 != "Inf":
            x = c2
            y = m1*x + c1
            if x >= min(startX, endX) and x <= max(startX, endX):
                if y >= min(startY, endY) and y <= max(startY, endY):
                    if x >= min(x1, x2) and x <= max(x1, x2) and y >= min(y1, y2) and y <= max(y1, y2):
                        return True
        # Checks if the vertical edge intersects edge
        elif m1 == "Inf" and m2 != "Inf":
            x = c1
            y = m2*x + c2
            if x >= min(x1, x2) and x <= max(x1, x2) and y >= min(y1, y2) and y <= max(y1, y2):
                if x >= min(startX, endX) and x <= max(startX, endX):
                    if y >= min(startY, endY) and y <= max(startY, endY):
                        return True 
        # Checks if collision is within the range of the edge
        elif m1 != m2:
            x = (c2 - c1)/(m1 - m2)
            y = m1*x + c1
            if (x >= min(x1, x2) - SMALLPAD and x <= max(x1, x2) + SMALLPAD and y >= min(y1, y2) - SMALLPAD and y <= max(y1, y2) + SMALLPAD):
                if x >= min(startX, endX) - SMALLPAD and x <= max(startX, endX) + SMALLPAD:
                    if y >= min(startY, endY) - SMALLPAD and y <= max(startY, endY) + SMALLPAD:
                        return True
        # Checks if parralel that edges are not too close
        elif m1 == m2 and m2 != 0:
            shortestDist = abs(c2-c1)/((1 + m1*m1)**0.5)

            # Gets perpendicular line using one set of edges to find the intersection on other edge,
            #c3 ==> c for start coordinate of edge, c4 ==> c for end coordinate of edge
            m3 = -1/m2
            c3, c4 = y1 - m3*x1, y2 - m3*x2

            # Coordinates to compare 
            x1, x2 = (c3 - c1)/(m1 - m3), (c4 - c1)/(m1 - m3)
            y1, y2 = m1*x1 + c1, m1*x2 + c1

            if shortestDist <= 2*LARGEPAD:
                if (x1 >= min(startX, endX) and x1 <= max(startX, endX)) or (x2 >= min(startX, endX) and x2 <= max(startX, endX)):
                    if (y1 >= min(startY, endY) and y1 <= max(startY, endY)) or (y2 >= min(startY, endY) and y2 <= max(startY, endY)):
                        return True

        return False

    def __validateNewEdgeWithNode(self, startX, startY, endX, endY, userInput, otherNodes = [], nodeCapID = False):
        # Gets list of all nodes
        if otherNodes == []:
            allNodes = self.__nodes
        else:
            allNodes = otherNodes + self.__nodes

        if self.__addedNodes[2] != []:
            for setOfNodes in self.__addedNodes[2]:
                allNodes = allNodes + setOfNodes
            
        collisions = False
        idx = 0
        
        edge = Edge("*", "*", 0, 2, startX, startY, endX, endY)

        while idx < len(allNodes) and not collisions:
            # Accounts for associated nodes to be drawn at different times but collide
            if allNodes[idx].getNodeID() != nodeCapID:
                X, Y = allNodes[idx].getCoords()

                # Checks collision with main arrow
                if self.__collisionDetectionEdgewithNode(startX, startY, endX, endY, X, Y):
                    collisions = True

                # Checks collision with fw arrow
                detectionBoxCoordsX, detectionBoxCoordsY = edge.getSmallFwArrowCoords()
                vertices = []
                for coordX in detectionBoxCoordsX:
                    for coordY in detectionBoxCoordsY:
                        vertices.append([coordX, coordY])

                for j, vertex1 in enumerate(vertices):
                    for k in range(j + 1, len(vertices)):
                        vertex2 = vertices[k]
                        if (vertex1[0] in vertex2 and not vertex1[1] in vertex2) or (
                            not vertex1[0] in vertex2 and vertex1[1] in vertex2):
                            
                            x1, y1 = vertex1
                            x2, y2 = vertex2
                            if self.__collisionDetectionEdgewithNode(x1, y1, x2, y2, X, Y):
                                collisions = True

                # Checks collision with bw arrow
                detectionBoxCoordsX, detectionBoxCoordsY = edge.getSmallBwArrowCoords()
                vertices = []
                for coordX in detectionBoxCoordsX:
                    for coordY in detectionBoxCoordsY:
                        vertices.append([coordX, coordY])

                for j, vertex1 in enumerate(vertices):
                    for k in range(j + 1, len(vertices)):
                        vertex2 = vertices[k]
                        if (vertex1[0] in vertex2 and not vertex1[1] in vertex2) or (
                            not vertex1[0] in vertex2 and vertex1[1] in vertex2):
                            
                            x1, y1 = vertex1
                            x2, y2 = vertex2
                            if self.__collisionDetectionEdgewithNode(x1, y1, x2, y2, X, Y):
                                collisions = True
                            
            idx += 1

        if collisions and userInput:
            self.__addErrorMsg("Edge collides with other nodes")
        
        return collisions

    def __collisionDetectionEdgewithNode(self, startX, startY, endX, endY, X, Y):
        collisions = False

        if startX != endX:
            m1 = (endY - startY)/(endX - startX)#ckeck for y axis lines
            c1 = -m1*startX + startY
        else:
            m1 = "Inf"
            c1 = startX
            
        if m1 != "Inf":
            # Checks if collision between an edge that is not vertical and a node
            dist = abs(-m1*X + Y - c1)//((1 + (m1)**2)**0.5)
            if dist - RADIUS - SMALLPAD <= 0:
                if X >= min(startX, endX) - SMALLPAD and X <= max(startX, endX) + SMALLPAD:
                    if Y >= min(startY, endY) - SMALLPAD and Y <= max(startY, endY) + SMALLPAD:
                        collisions = True
        else:
            # Checks if collision between a vertical edge and a node
            if c1 <= X + RADIUS + SMALLPAD and c1 >= X - RADIUS - SMALLPAD and endY >= Y - RADIUS and endY <= Y + RADIUS:
                collisions = True

        return collisions
              
    def __checkMinCap(self):
        self.__ifMinCap = False
        
        for edge in self.__edges:
            if edge.hasMinCap():
                self.__ifMinCap = True
            
    def __updateFlow(self):
        self.__invalidInput = False
        flowInfo = []

        nodeCapDict = {}
        for node in self.__nodes:
            if node.getNodeCap() != 0:
                nodeCapDict[node.getNodeID()] = node.getNodeCap()

        # Gets text in relation to augmented flow 
        for inputBox in self.__flowInpBoxes:
            if inputBox.getTxt() != "":
                flowInfo.append(inputBox.getTxt())
            else:
                self.__addErrorMsg("Not all required inputs were completed")
                return

        flowInfo[0] = flowInfo[0].split(",")
        flowInfo[1] = int(flowInfo[1])
        
        # Checks if existing edges along paths
        edgeIdxs = []
        idx, match = 0, False
        while idx < len(flowInfo[0]) - 1:
            match = False
            
            for i in range(len(self.__edges)):
                currentEdge = self.__edges[i]
                if currentEdge.getFromNode() == flowInfo[0][idx] and currentEdge.getToNode() == flowInfo[0][idx + 1]:
                    if currentEdge.getBwFlow() >= flowInfo[1]:
                        currentEdge.addFlow(flowInfo[1])
                        edgeIdxs.append(i)
                    else:
                        self.__addErrorMsg("Additional flow entered is too great")

                    if nodeCapDict != {}:
                        if nodeCapDict.get(currentEdge.getFromNode(), False) != False:
                            # Accounts for existing flow
                            total = nodeCapDict.get(currentEdge.getFromNode(), False)
                            for path, flow in self.__addedFlows:
                                if currentEdge.getFromNode() in path:
                                    total -= int(flow)

                        if idx == len(flowInfo[0]) - 2:
                            if nodeCapDict.get(currentEdge.getToNode(), False) != False:
                                for path, flow in self.__addedFlows:
                                    if currentEdge.getToNode() in path:
                                        total -= int(flow)

                        if flowInfo[1] > total:
                            self.__addErrorMsg("Additional flow entered is too great")

                    match = True                  
            if not match:
                self.__addErrorMsg("Atleast one edge does not exist")

            idx += 1

        if self.__invalidInput:
            for each in edgeIdxs:
                self.__edges[each].addFlow(-flowInfo[1])
        else:
            found, idx = False, 0

            # Combines flows if path already exists
            while idx < len(self.__addedFlows) and not found:
                if self.__addedFlows[idx][0] == flowInfo[0]:
                    self.__addedFlows[idx][1] += flowInfo[1]

                    recordIdx = self.__maxFlowScrollbar.findElement(",".join(flowInfo[0]))
                    existingPath, existingFlow = self.__maxFlowScrollbar.getElement(recordIdx)
                    self.__maxFlowScrollbar.delRecord(recordIdx)
                    self.__maxFlowScrollbar.insertRecords(recordIdx, [existingPath, str(int(existingFlow) + flowInfo[1])])
                    
                    found = True

                idx += 1

            if not found:
                self.__addedFlows.append(flowInfo)

                if self.__maxFlowScrollbar.getLenDispData() == 0:
                    self.__maxFlowScrollbar.insertRecords(0, ["Path", "Flow"])
                self.__maxFlowScrollbar.insertRecords(-1, [",".join(flowInfo[0]), str(flowInfo[1])])

            self.__additionalTotal += int(flowInfo[1])
            self.__maxFlowScrollbar.updateHeader(f"Max Flow - Total = {self.__additionalTotal}")

    def __createNodeCap(self, node):
        ingoingX, ingoingY, flowThroughNode = self.__getIngoingCoordsOfNodeCap(node)
        outgoingX, outgoingY = self.__getOutgoingCoordsOfNodeCap(node)

        ingoingNode = Node(f"{node.getNodeID()}-1", 0, ingoingX, ingoingY)
        ingoingNode.updateType("NodeCap")
        outgoingNode = Node(f"{node.getNodeID()}-2", 0, outgoingX, outgoingY)
        outgoingNode.updateType("NodeCap")
        
        ingoingPos = self.__findPossiblePos(ingoingNode, nodeCapID = node.getNodeID())
        outgoingPos = self.__findPossiblePos(outgoingNode, nodeCapID = node.getNodeID())
        ingoingNode.replaceCoords(ingoingPos[0][0], ingoingPos[0][1])
        outgoingNode.replaceCoords(outgoingPos[0][0], outgoingPos[0][1])

        if len(ingoingPos) > 50:
            ingoingPos = ingoingPos[:50]
        if len(outgoingPos) > 50:
            outgoingPos = outgoingPos[:50]
        
        self.__addedEdges[2].append([])

        self.__nodeCapButton.setHideButton()

        ingoingIdx, collisions = 0, True
        while ingoingIdx < len(ingoingPos) and collisions:
            outgoingIdx = 0
            ingoingX, ingoingY = ingoingNode.getCoords()
            while outgoingIdx < len(outgoingPos) and collisions:
                collisions, edgeIDToAdd = False, []
                outgoingX, outgoingY = outgoingNode.getCoords()

                # Checks proximity between nodes
                if ((ingoingX - outgoingX)**2 + (ingoingY - outgoingY)**2)**0.5 > 35 + 2*RADIUS:
                    ingoingNode, outgoingNode, edgeIDToAdd, collisions = self.__createIngoingEdgeToNodeCap(
                        node, ingoingNode, outgoingNode, edgeIDToAdd, collisions)
                    ingoingNode, outgoingNode, edgeIDToAdd, collisions = self.__createOutgoingEdgeToNodeCap(
                        node, ingoingNode, outgoingNode, edgeIDToAdd, collisions)
                    ingoingNode, outgoingNode, collisions = self.__createEdgeBetweenNodeCap(
                        node, ingoingNode, outgoingNode, collisions, flowThroughNode)
                else:
                    collisions = True
   
                if collisions:
                    outgoingNode.replaceCoords(outgoingPos[outgoingIdx][0], outgoingPos[outgoingIdx][1])
                    self.__addedEdges[2][-1] = []
                
                outgoingIdx += 1

            if collisions:
                ingoingNode.replaceCoords(ingoingPos[ingoingIdx][0], ingoingPos[ingoingIdx][1])
            ingoingIdx += 1

        if not collisions:
            self.__ifNodeCap = True
            self.__nodeCapButton.setShowButton()

            self.__addedNodes[2].append([ingoingNode, outgoingNode])
            node.updateNodeCapRef(len(self.__addedNodes[2]) - 1)

            self.__nodeRelDict[ingoingNode.getNodeID()] = len(self.__nodeRelDict)
            self.__nodeRelDict[outgoingNode.getNodeID()] = len(self.__nodeRelDict)
            
            if self.__nodeCapButton.getCurrentPhase() == "Show Node Cap":
                self.__nodeCapButton.changePhase()                 

            # Adds edge IDs once all are valid
            for each, edgeID, inOrOut in edgeIDToAdd:
                if inOrOut == "in":
                    each.addIncomingEdge(edgeID)
                else:
                    each.addOutgoingEdge(edgeID)
        else:
            self.__addErrorMsg("No valid node capacity position")

            # Resets edge to not being part of node cap
            for edgeID in node.getIncomingEdges():
                edgeIdx = self.__edgeRelDict[edgeID]
                edge = self.__getEdge(edgeIdx)
                edge.updatePartOfNodeCap(False)

            for edgeID in node.getOutgoingEdges():
                edgeIdx = self.__edgeRelDict[edgeID]
                edge = self.__getEdge(edgeIdx)
                edge.updatePartOfNodeCap(False)

    def __getIngoingCoordsOfNodeCap(self, node):
        X, Y = node.getCoords()

        ingoingX, ingoingY = 0, 0
        count, flowThroughNode = 0, 0
        for edgeID in node.getIncomingEdges():
            edgeIdx = self.__edgeRelDict[edgeID]
            edge = self.__getEdge(edgeIdx)
            edge.updatePartOfNodeCap(True)
            flowThroughNode += edge.getFwFlow()
            fromNodeID = edge.getFromNode()
            nodeIdx = self.__nodeRelDict[fromNodeID]
            fromNode = self.__getNode(nodeIdx)
            x, y = fromNode.getCoords()
            ingoingX += x
            ingoingY += y
            count += 1

        if count != 0:
            ingoingX /= count
            ingoingY /= count

            # Finds average pos between incoming node and original position
            ingoingX, ingoingY = (ingoingX + X)/2, (ingoingY + Y)/2
        else:
            ingoingX, ingoingY = X, Y

        return [ingoingX, ingoingY, flowThroughNode]

    def __getOutgoingCoordsOfNodeCap(self, node):
        X, Y = node.getCoords()
          
        outgoingX, outgoingY = 0, 0
        count = 0
        for edgeID in node.getOutgoingEdges():
            edgeIdx = self.__edgeRelDict[edgeID]
            edge = self.__getEdge(edgeIdx)
            edge.updatePartOfNodeCap(True)
            toNodeID = edge.getToNode()
            nodeIdx = self.__nodeRelDict[toNodeID]
            toNode = self.__getNode(nodeIdx)
            x, y = toNode.getCoords()
            outgoingX += x
            outgoingY += y
            count += 1

        if count != 0:
            outgoingX /= count
            outgoingY /= count

            # Finds average pos between outgoing nodes and original position
            outgoingX, outgoingY = (outgoingY + X)/2, (outgoingY + Y)/2
        else:
            outgoingX, outgoingY = X, Y

        return [outgoingX, outgoingY]

    def __createIngoingEdgeToNodeCap(self, node, ingoingNode, outgoingNode, edgeIDToAdd, collisions):
        for i, edgeID in enumerate(node.getIncomingEdges()):
            hasNodeCap = False
            
            edgeIdx = self.__edgeRelDict[edgeID]
            edge = self.__getEdge(edgeIdx)
            fromNodeID = edge.getFromNode()
            nodeIdx = self.__nodeRelDict[fromNodeID]
            fromNode = self.__getNode(nodeIdx)

            # Bases off node cap if one has been found
            if fromNode.getNodeCap() > 0 and fromNode.getNodeCapRef() != "":
                hasNodeCap = True
                fromNode = self.__addedNodes[2][fromNode.getNodeCapRef()][1]
                startX, startY = fromNode.getCoords()
            else:
                startX, startY = fromNode.getCoords()
            endX, endY = ingoingNode.getCoords()

            startX, startY, endX, endY = self.__shiftStartEndCoordsOfEdge(startX, startY, endX, endY)

            if self.__validateNewEdgeWithOtherEdges(startX, startY, endX, endY, False, nodeCapID = node.getNodeID()):
                collisions = True
            if self.__validateNewEdgeWithNode(startX, startY, endX, endY, False, [ingoingNode, outgoingNode], nodeCapID = node.getNodeID()):
                collisions = True

            if not collisions:
                # Adds initial flow if any from augmented paths
                newEdge = Edge(fromNode.getNodeID(), f"{ingoingNode.getNodeID()}", edge.getMinCap(), edge.getMaxCap(), startX, startY, endX, endY)
                newEdge.addFlow(edge.getFwFlow())

                self.__addedEdges[2][-1].append(newEdge)
                ingoingNode.addIncomingEdge(newEdge.getEdgeID())
                if hasNodeCap:
                    edgeIDToAdd.append([fromNode, newEdge.getEdgeID(), "out"])
            else:
                # Resets ingoingNode incoming edges
                incomingEdges = node.getIncomingEdges()
                for j in range(i):
                    ingoingNode.delIncomingEdge(incomingEdges[j])
                    
        return [ingoingNode, outgoingNode, edgeIDToAdd, collisions]

    def __createOutgoingEdgeToNodeCap(self, node, ingoingNode, outgoingNode, edgeIDToAdd, collisions):
        for i, edgeID in enumerate(node.getOutgoingEdges()):
            hasNodeCap = False
            
            edgeIdx = self.__edgeRelDict[edgeID]
            edge = self.__getEdge(edgeIdx)
            toNodeID = edge.getToNode()
            nodeIdx = self.__nodeRelDict[toNodeID]
            toNode = self.__getNode(nodeIdx)

            # Bases off node cap if one has been found
            startX, startY = outgoingNode.getCoords()
            if toNode.getNodeCap() > 0 and toNode.getNodeCapRef() != "":
                hasNodeCap = True
                toNode = self.__addedNodes[2][toNode.getNodeCapRef()][0]
                endX, endY = toNode.getCoords()
            else:
                endX, endY = toNode.getCoords()

            startX, startY, endX, endY = self.__shiftStartEndCoordsOfEdge(startX, startY, endX, endY)

            if self.__validateNewEdgeWithOtherEdges(startX, startY, endX, endY, False, nodeCapID = node.getNodeID()):
                collisions = True
            if self.__validateNewEdgeWithNode(startX, startY, endX, endY, False, [ingoingNode, outgoingNode], nodeCapID = node.getNodeID()):
                collisions = True

            if not collisions:
                # Adds initial flow if any from augmented paths
                newEdge = Edge(outgoingNode.getNodeID(), toNode.getNodeID(), edge.getMinCap(), edge.getMaxCap(), startX, startY, endX, endY)
                newEdge.addFlow(edge.getFwFlow())
                
                self.__addedEdges[2][-1].append(newEdge)
                
                outgoingNode.addOutgoingEdge(newEdge.getEdgeID())
                if hasNodeCap:
                    edgeIDToAdd.append([toNode, newEdge.getEdgeID(), "in"])
            else:
                # Resets outgoingNode outgoing edges
                outgoingEdges = node.getOutgoingEdges()
                for j in range(i):
                    outgoingNode.delOutgoingEdge(outgoingEdges[j])

        return [ingoingNode, outgoingNode, edgeIDToAdd, collisions]

    def __createEdgeBetweenNodeCap(self, node, ingoingNode, outgoingNode, collisions, flowThroughNode):
        startX, startY = ingoingNode.getCoords()
        endX, endY = outgoingNode.getCoords()
        
        startX, startY, endX, endY = self.__shiftStartEndCoordsOfEdge(startX, startY, endX, endY)

        if self.__validateNewEdgeWithNode(startX, startY, endX, endY, False, [ingoingNode, outgoingNode], nodeCapID = node.getNodeID()):
            collisions = True
        if self.__validateNewEdgeWithOtherEdges(startX, startY, endX, endY, False, nodeCapID = node.getNodeID()):
            collisions = True

        if not collisions:
            # Adds initial flow if any from augmented paths
            edgeBetween = Edge(ingoingNode.getNodeID(), outgoingNode.getNodeID(), 0, node.getNodeCap(), startX, startY, endX, endY)
            edgeBetween.addFlow(flowThroughNode)

            self.__addedEdges[2][-1].append(edgeBetween)
            ingoingNode.addOutgoingEdge(edgeBetween.getEdgeID())
            outgoingNode.addIncomingEdge(edgeBetween.getEdgeID())

        return [ingoingNode, outgoingNode, collisions]
                
    def __createSupersink(self):  
        X, Y = 0, 0

        # Average pos of sinks
        coords = [sink.getCoords() for sink in self.__sinks]
        for each in coords:
            X += each[0]
            Y += each[1]
        X /= len(coords)
        Y /= len(coords)
        
        supersink = SourcesOrSinks("T", 0, X, Y)
        supersink.updateType("Supersink")
        
        if self.__isSupersource:
            positions = self.__findPossiblePos(supersink, [self.__addedNodes[0]])
        else:
            positions = self.__findPossiblePos(supersink)

        if len(positions) > 0:
            supersink.replaceCoords(positions[0][0], positions[0][1])
            self.__addedNodes[1] = supersink

            collisions = True
            while collisions:
                collisions, nodeCapEdges = False, []
                self.__supersinkButton.setHideButton()
                for sinkIdx, sink in enumerate(self.__sinks):
                    ifNodeCapIsSink = False
                    
                    startX, startY = sink.getCoords()
                    endX, endY = supersink.getCoords()

                    startX, startY, endX, endY = self.__shiftStartEndCoordsOfEdge(startX, startY, endX, endY)

                    if self.__isSupersource:
                        if self.__validateNewEdgeWithNode(startX, startY, endX, endY, False, [self.__addedNodes[0]]):
                            collisions = True
                    else:
                        if self.__validateNewEdgeWithNode(startX, startY, endX, endY, False):
                            collisions = True
                    if self.__validateNewEdgeWithOtherEdges(startX, startY, endX, endY, False):
                            collisions = True

                    if sink.getNodeCapRef() != "":
                        ifNodeCapIsSink = True

                        # Accounts for edges going from a node cap
                        nodeCapStartX, nodeCapStartY = self.__addedNodes[2][sink.getNodeCapRef()][1].getCoords()
                        nodeCapEndX, nodeCapEndY = supersink.getCoords()

                        nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY = self.__shiftStartEndCoordsOfEdge(
                            nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY)

                        if self.__validateNewEdgeWithNode(nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY, False, nodeCapID = sink.getNodeID()):
                            collisions = True
                        if self.__validateNewEdgeWithOtherEdges(nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY, False, nodeCapID = sink.getNodeID()):
                            collisions = True
                            
                    if not collisions:
                        # Creates an edge if no collisions, based on known connected edges
                        edgeIDs = [edgeID for edgeID in sink.getIncomingEdges()]

                        maxCap, fwFlow = 0, 0
                        for edge in self.__edges:
                            for edgeID in edgeIDs:
                                if edge == edgeID:
                                    maxCap += edge.getMaxCap()
                                    fwFlow += edge.getFwFlow()
                            
                        edge = Edge(sink.getNodeID(), "T", 0, maxCap, startX, startY, endX, endY)
                        edge.addFlow(fwFlow)
                        self.__addedEdges[1].append(edge)

                        if ifNodeCapIsSink:
                            edgeWithNodeCap = Edge(f"{sink.getNodeID()}-2", "T", 0, maxCap, nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY)
                            nodeCapEdges.append([edgeWithNodeCap, sink.getNodeCapRef(), fwFlow, len(self.__addedEdges[1]) - 1])
                    else:
                        # Resets as no valid positions
                        try:
                            positions.pop(0)
                            supersink.replaceCoords(positions[0][0], positions[0][1])          
                        except IndexError:
                            collisions = False
                            self.__addedNodes[1] = []
                            
                        finally:
                            self.__addedEdges[1] = []
                            nodeCapEdges = []
                            for i in range(sinkIdx):
                                supersink.delIncomingEdge(edge.getEdgeID())
                                self.__sinks[i].delOutgoingEdge(edge.getEdgeID())
                                
                        break

        if self.__addedNodes[1] != []:
            self.__isSupersink = True
            self.__supersinkButton.setShowButton()

            for edge in self.__addedEdges[1]:
                supersink.addIncomingEdge(edge.getEdgeID())
                for sink in self.__sinks:
                    if sink.getNodeID() == edge.getFromNode():
                        sink.addOutgoingEdge(edge.getEdgeID())

            for edge, nodeCapRef, fwFlow, associatedEdgeIdx in nodeCapEdges:
                edge.addFlow(fwFlow)
                self.__addedEdges[2][nodeCapRef].append(edge)
                self.__addedNodes[2][nodeCapRef][1].addOutgoingEdge(edge.getEdgeID())
                self.__addedEdges[1][associatedEdgeIdx].updatePartOfNodeCap(True)

            self.__nodeRelDict["T"] = len(self.__nodeRelDict)
            if self.__supersinkButton.getCurrentPhase() == "Show Supersink":
                self.__supersinkButton.changePhase()
        else:
            self.__addErrorMsg("No valid supersink position found")

    def __createSupersource(self):        
        X, Y = 0, 0

        # Average pos of sources
        coords = [source.getCoords() for source in self.__sources]
        for each in coords:
            X += each[0]
            Y += each[1]
        X /= len(coords)
        Y /= len(coords)
        
        supersource = SourcesOrSinks("S", 0, X, Y)
        supersource.updateType("Supersource")
        positions = self.__findPossiblePos(supersource)

        if len(positions) > 0:
            supersource.replaceCoords(positions[0][0], positions[0][1])
            self.__addedNodes[0] = supersource

            collisions = True 
            while collisions:
                collisions = False
                nodeCapEdges = []
                self.__supersinkButton.setHideButton()
                for sourceID, source in enumerate(self.__sources):
                    ifNodeCapIsSource = False
                    
                    startX, startY = supersource.getCoords()
                    endX, endY = source.getCoords()

                    startX, startY, endX, endY = self.__shiftStartEndCoordsOfEdge(startX, startY, endX, endY)

                    if self.__validateNewEdgeWithOtherEdges(startX, startY, endX, endY, False): 
                        collisions = True
                    if self.__validateNewEdgeWithNode(startX, startY, endX, endY, False):
                        collisions = True

                    if source.getNodeCapRef() != "":
                        ifNodeCapIsSource = True

                        # Accounts for edges going from a node cap
                        nodeCapStartX, nodeCapStartY = supersource.getCoords()
                        nodeCapEndX, nodeCapEndY = self.__addedNodes[2][source.getNodeCapRef()][0].getCoords()

                        nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY = self.__shiftStartEndCoordsOfEdge(
                            nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY)
                        if self.__validateNewEdgeWithNode(nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY, False, nodeCapID = source.getNodeID()):
                            collisions = True
                        if self.__validateNewEdgeWithOtherEdges(nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY, False, nodeCapID = source.getNodeID()):
                            collisions = True

                    if not collisions:
                        # Creates an edge if no collisions, based on known connected edges
                        edgeIDs = [edgeID for edgeID in source.getOutgoingEdges()]
                        maxCap, fwFlow = 0, 0
                        for edge in self.__edges:
                            for each in edgeIDs:
                                if edge == each:
                                    maxCap += edge.getMaxCap()
                                    fwFlow += edge.getFwFlow()
                            
                        edge = Edge("S", source.getNodeID(), 0, maxCap, startX, startY, endX, endY)
                        edge.addFlow(fwFlow)

                        if ifNodeCapIsSource:
                            edgeWithNodeCap = Edge("S", f"{source.getNodeID()}-1", 0, maxCap, nodeCapStartX, nodeCapStartY, nodeCapEndX, nodeCapEndY)
                            nodeCapEdges.append([edgeWithNodeCap, source.getNodeCapRef(), fwFlow, len(self.__addedEdges[0])])
                        
                        self.__addedEdges[0].append(edge)
                    else:
                        # Resets as no valid positions
                        try:
                            positions.pop(0)
                            supersource.replaceCoords(positions[0][0], positions[0][1])    
                        except IndexError:
                            collisions = False
                            self.__addedNodes[0] = []
                        finally:
                            self.__addedEdges[0] = []
                            nodeCapEdges = []
                            for i in range(sourceID):
                                self.__sources[i].delIncomingEdge(edge.getEdgeID())
                                supersource.delOutgoingEdge(edge.getEdgeID())
                        break
                        
        if self.__addedNodes[0] != []:
            self.__isSupersource = True
            self.__supersourceButton.setShowButton()

            for edge in self.__addedEdges[0]:                        
                supersource.addOutgoingEdge(edge.getEdgeID())
                for source in self.__sources:
                    if source.getNodeID() == edge.getToNode():
                        source.addIncomingEdge(edge.getEdgeID())

            for edge, nodeCapRef, fwFlow, associatedEdgeIdx in nodeCapEdges:
                edge.addFlow(fwFlow)
                self.__addedEdges[2][nodeCapRef].append(edge)
                self.__addedNodes[2][nodeCapRef][0].addIncomingEdge(edge.getEdgeID())
                self.__addedEdges[0][associatedEdgeIdx].updatePartOfNodeCap(True)

            self.__nodeRelDict[edge.getFromNode()] = len(self.__nodeRelDict)
            
            if self.__supersourceButton.getCurrentPhase() == "Show Supersource":
                self.__supersourceButton.changePhase()
        else:
            self.__addErrorMsg("No valid supersource position found")

    def __findPossiblePos(self, node, otherNodesToCheck = [], nodeCapID = False):
        possCoords = []
        change = [[10,0], [0,-10], [-10, 0], [0, 10]]
        count = 2

        while count < 50:
            mult = count//2

            # increments so checks possible positions in spiral from center point
            if count % 2 == 1:
                temp = change.pop(0)
                change.append(temp)

            changeX, changeY = change[0][0], change[0][1]

            # Mult is variable to allow number of shifts per change to grdually increase
            for i in range(mult):
                collision = False
                
                X, Y = node.getCoords()
                node.replaceCoords(X + changeX, Y + changeY)

                newNodeX, newNodeY = node.getCoords()
                if all([newNodeX > self.__graphDispBorder.getX() + RADIUS,
                            newNodeY > self.__graphDispBorder.getY() + RADIUS,
                            newNodeX < self.__graphDispBorder.getX() + self.__graphDispBorder.getW() - RADIUS,
                            newNodeY < self.__graphDispBorder.getH() + self.__graphDispBorder.getY() - RADIUS]):
                    
                    if self.__validateNewNodeWithOtherNodes(newNodeX, newNodeY, False, 35, otherNodesToCheck, nodeCapID):
                        collision = True
                    if self.__validateNewNodeWithEdge(newNodeX, newNodeY, False, nodeCapID = nodeCapID):
                        collision = True
                else:
                    collision = True
                    
                if not collision:
                    possCoords.append(node.getCoords())

            count += 1
            
        return possCoords

    def __analyseCut(self):
        invalid = False
        
        sourceSide, sinkSide = [], []
        source2Sink, sink2Source = [], []

        visited, onSourceSide, invalid, collidedEdges, nodeCapsSliced = self.__BFS(invalid)

        for nodeID, ifOnSourceSide in zip(visited, onSourceSide):
            if ifOnSourceSide:
                sourceSide.append(nodeID)
            else:
                sinkSide.append(nodeID)

        # Checks sources and sinks are on there respected sides of the cut
        idx = 0
        while idx < len(self.__sources) and not invalid:
            match = False

            source = self.__sources[idx]
            if source.getNodeCapRef() != "":
                source = self.__addedNodes[2][source.getNodeCapRef()][0]
                
            for nodeID in sourceSide:
                if source.getNodeID() == nodeID:
                    match = True
            if not match:
                invalid = True
                
            idx += 1

        idx = 0
        while idx < len(self.__sinks) and not invalid:
            match = False
            
            sink = self.__sinks[idx]
            if sink.getNodeCapRef() != "":
                sink = self.__addedNodes[2][sink.getNodeCapRef()][1]
                
            for nodeID in sinkSide: 
                if sink.getNodeID() == nodeID:
                    match = True

            if sink.getNodeCapRef() == "" and sink.getNodeCap() > 0 and not match:
                match = True
                
            if not match:
                invalid = True
            idx += 1
            
        for collidedEdge in collidedEdges:
            fromNode, toNode = collidedEdge.getFromNode(), collidedEdge.getToNode()
            if fromNode in sourceSide and toNode in sinkSide:
                source2Sink.append(collidedEdge.getMaxCap())
            elif toNode in sourceSide and fromNode in sinkSide:
                sink2Source.append(collidedEdge.getOriginalMinCap())

        # Splits any nodes into node IDs it would have been if valid pos for node cap
        for nodeCap, nodeCapValue in nodeCapsSliced:
            if nodeCap in sourceSide:
                idx = sourceSide.index(nodeCap)
                sourceSide[idx] = f"{nodeCap}-1"
                sinkSide.append(f"{nodeCap}-2")
                source2Sink.append(nodeCapValue)
            elif nodeCap in sinkSide:
                idx = sinkSide.index(nodeCap)
                sinkSide[idx] = f"{nodeCap}-1"
                sourceSide.append(f"{nodeCap}-2")
                sink2Source.append(nodeCapValue)
                
        if invalid:
            self.__cuts.pop(-1)
            Cut.decreaseID()
            self.__addErrorMsg("Cut drawn is invalid")
        else:
            source2SinkTotal = reduce(lambda x, y: x + y, source2Sink)
            if len(sink2Source) != 0:
                sink2SourceTotal = reduce(lambda x, y: x + y, sink2Source)
                sink2Source = list(map(lambda x: str(x), sink2Source))
                sink2Source = " + ".join(sink2Source)
            else:
                sink2SourceTotal = 0
                sink2Source = 0

            source2Sink = list(map(lambda x: str(x), source2Sink))
            source2Sink = " + ".join(source2Sink)

            sourceSide = ",".join(sourceSide)
            sinkSide = ",".join(sinkSide)
           
            self.__cuts[-1].setCutNotation(sourceSide, sinkSide)
            self.__cuts[-1].setCutValues(source2Sink, sink2Source, source2SinkTotal, sink2SourceTotal)
            
            if self.__dispCutInfoScrollbar.getLenDispData() == 0:
                headers = ["Cut ID + notation", "Source to sink values", "Sink to source values", "Total cutValue"]
                self.__dispCutInfoScrollbar.insertRecords(-1, headers)
                
            self.__dispCutInfoScrollbar.insertRecords(-1, [self.__cuts[-1].getCutID() + " " + self.__cuts[-1].getCutNotation(),
                                                           source2Sink, str(sink2Source), f"{source2SinkTotal} - {sink2SourceTotal}"])
            self.__dispCutInfoScrollbar.insertRecords(-1, [" ", f"= {source2SinkTotal}", f"= {sink2SourceTotal}", f"= {source2SinkTotal-sink2SourceTotal}"], True)

            self.__showCutIDButtons.append(Button(self.__cutIDScrollbar.getX() + self.__cutIDScrollbar.getW(),
                                                self.__cutIDScrollbar.getY() + len(self.__showCutIDButtons)*20, INTBUTTONWIDTH, BUTTONHEIGHT,
                                                ["Hide", "Show"], BLACK, 2))
                                                    
            self.__cutIDScrollbar.insertRecords(-1, self.__cuts[-1].getCutID())

        return invalid

    def __BFS(self, invalid):
        Queue = CircularQueue()
        collidedEdges, visited = [], []

        noOfNodes = self.__getNoOfExisingNodes()

        # For each index, if on the source side ==> True, if on the sink side ==> False
        onSourceSide, nodeCapsSliced = [""]*noOfNodes, []
        onSourceSide[0] = True

        if self.__isSupersource:
            Queue.push(self.__addedNodes[0])
            visited.append(self.__addedNodes[0].getNodeID())
            onSourceSide[0] = True
        else:
            for i, source in enumerate(self.__sources):
                if source.getNodeCapRef() != "":
                    source = self.__addedNodes[2][source.getNodeCapRef()][0]
                Queue.push(source)
                visited.append(source.getNodeID())
                onSourceSide[i] = True

        # Uses a BFS for all node within graph to determine collisions with each cut drawn
        while not Queue.isEmpty():
            collision = False
            
            currentNode = Queue.remove()
            outgoingEdges = currentNode.getOutgoingEdges()

            if len(outgoingEdges) != 0:
                for edgeID in outgoingEdges:
                    currentEdgeIdx = self.__edgeRelDict[edgeID]
                    currentEdge = self.__getEdge(currentEdgeIdx)
                    node = self.__getNode(self.__nodeRelDict[currentEdge.getToNode()])
                    nodeCapRef = node.getNodeCapRef()
                    # Accounts for node cap being the next edge
                    if nodeCapRef != "":
                        node = self.__addedNodes[2][node.getNodeCapRef()][0]
                        for addedEdge in self.__addedEdges[2][nodeCapRef]:
                            if addedEdge.getFromNode() == currentEdge.getFromNode() and addedEdge.getToNode() == node.getNodeID():
                                currentEdge = addedEdge

                    ifOnSourceSide = onSourceSide[visited.index(currentEdge.getFromNode())]

                    startX, startY = currentEdge.getStartCoords()
                    endX, endY = currentEdge.getEndCoords()

                    # Collision ==> swap side the cut
                    if self.__cuts[-1].validateLineCollisionWithEdge(startX, startY, endX, endY):
                        ifOnSourceSide = not ifOnSourceSide
                        collision = True

                    X, Y = currentNode.getCoords()
                    if self.__cuts[-1].validateLineCollisionWithNode(X, Y):
                        # If node cap can't be made, allows collision through node
                        if currentNode.getNodeCap() > 0 and currentNode.getNodeCapRef() == "":
                            nodeCapsSliced.append([currentNode.getNodeID(), currentNode.getNodeCap()])
                            ifOnSourceSide = not ifOnSourceSide
                        else:
                            invalid = True
                            
                    try:
                        ifOtherNodeIsOnSourceSide = onSourceSide[visited.index(currentEdge.getToNode())]
                        if ifOtherNodeIsOnSourceSide != ifOnSourceSide:
                            invalid = True     
                    except ValueError:
                        if currentEdge.getToNode() == "T" and currentEdge.getToNode() not in visited:
                            Queue.push(self.__addedNodes[1])
                            node = self.__addedNodes[1]
                        elif currentEdge.getToNode() not in visited:
                            node = self.__getNode(self.__nodeRelDict[currentEdge.getToNode()])
                                                                      
                            Queue.push(node)
                        visited.append(node.getNodeID())
                        onSourceSide[visited.index(node.getNodeID())] = ifOnSourceSide
                    finally:
                        if collision:
                            collidedEdges.append(currentEdge)
            else:
                X, Y = currentNode.getCoords()
                if self.__cuts[-1].validateLineCollisionWithNode(X, Y):
                    # If node cap can't be made, allows collision through node
                    if currentNode.getNodeCap() > 0 and currentNode.getNodeCapRef() == "":
                        nodeCapsSliced.append([currentNode.getNodeID(), currentNode.getNodeCap()])
                    else:
                        invalid = True

        return [visited, onSourceSide, invalid, collidedEdges, nodeCapsSliced]

    def __getNoOfExisingNodes(self):
        noOfNodes = len(self.__nodes)
        if self.__isSupersource:
            noOfNodes += 1
        if self.__isSupersink:
            noOfNodes += 1
        if self.__addedNodes[2] != []:
            nodeCapNodesNo = reduce(lambda y, z: y + z, list(map(lambda x: len(x), self.__addedNodes[2])))
            noOfNodes += nodeCapNodesNo

        return noOfNodes
     
def main():
    networkFlows = NetworkFlows()

    running = True
    while running:
        eventList = pg.event.get()

        for event in eventList:
            if event.type == pg.QUIT:
              running = False

        networkFlows.main(eventList)
        
        pg.display.flip()
        pg.time.delay(10)

        SCREEN.fill(BLACK)

if __name__ == "__main__":
    main()
