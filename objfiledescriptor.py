from geometry.shapes import Point, Line, Wireframe, GraphicObject, WorldItem
from geometry.transformations import determine_object_center

import os

from typing import List

class OBJFileDescriptor:

    def save(self, graphicObject: GraphicObject, filepath: str) -> bool:
        if graphicObject == None:
            print("No object to be saved was provided")
            return
        fileContent = str()
        if isinstance(graphicObject, Point):
            fileContent = self.getObjFileFromPoint(graphicObject)
        elif isinstance(graphicObject, Line):
            fileContent = self.getObjFileFromLine(graphicObject)
        elif isinstance(graphicObject, Wireframe):
            fileContent= self.getObjFileFromWireframe(graphicObject)
        else:
            return False
        with open(filepath, "w") as objFile:
            objFile.write(fileContent)
        return True

    def getObjFileFromPoint(self, point: Point) -> str:
        return f"p {point.x} {point.y}"

    def getObjFileFromLine(self, line: Line) -> str:
        fileContent = (
            f"v {line.start.x} {line.start.y}\n"
            f"v {line.end.x} {line.end.y}\n"
            "l 1 2"
        )
        return fileContent

    def getObjFileFromWireframe(self, wireframe: Wireframe) -> str:
        fileContent = str()
        polygonalFaceLine = "f"
        for vertixIndex, vertix in enumerate(wireframe.points):
            fileContent += f"v {vertix.x} {vertix.y}\n"
            polygonalFaceLine += f" {vertixIndex + 1}"
        fileContent += polygonalFaceLine
        return fileContent

    def load(self, folderPath: str) -> List[WorldItem]:
        if not os.path.isdir(folderPath):
            return list()
        loadedObjects = list()
        for filePath in os.listdir(folderPath):
            if filePath.endswith(".obj"):
                objectName = filePath.split(".")[0]
                with open(folderPath+"/"+filePath, "r") as objFile:
                    fileLines = objFile.readlines()
                    graphicObject = self.getObjectFromFile(fileLines)
                    worldItem = WorldItem(objectName, Point(0,0), graphicObject)
                    determine_object_center(worldItem)
                    loadedObjects.append(worldItem)
        return loadedObjects

    def getObjectFromFile(self, fileLines: List[str]) -> GraphicObject:
        if fileLines[0].startswith("p"):
            lineElements = fileLines[0].split(" ")
            x = int(lineElements[1])
            y = int(lineElements[2])
            return Point(x, y)
        elif fileLines[2].startswith("l"):
            startLineElements = fileLines[0].split(" ")
            endLineElements = fileLines[1].split(" ")
            startPoint = Point(int(startLineElements[1]), int(startLineElements[2]))
            endPoint = Point(int(endLineElements[1]), int(endLineElements[2]))
            return Line(startPoint, endPoint)
        else:
            vertexList = list()
            for vertexLine in fileLines[:-1]:
                lineElements = vertexLine.split(" ")
                vertexList.append(Point(int(lineElements[1]), int(lineElements[2][:-1])))
            return Wireframe(vertexList)
