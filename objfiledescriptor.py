from calculation.shapes.line import Line
from calculation.shapes.point import Point
from calculation.shapes.wireframe import Wireframe
from calculation.shapes.worldItem import GraphicObject


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
        print("Object was saved")
        return True

    def getObjFileFromPoint(self, point: Point) -> str:
        return f"p {point.x} {point.y}"

    def getObjFileFromLine(self, line: Line) -> str:
        fileContent = f'''v {line.start.x} {line.start.x}\n
                          v {line.end.x} {line.end.y}\n
                          l 1 2'''
        return fileContent

    def getObjFileFromWireframe(self, wireframe: Wireframe) -> str:
        fileContent = str()
        polygonalFaceLine = "f"
        for vertixIndex, vertix in enumerate(wireframe.points):
            fileContent += f"v {vertix.x} {vertix.y}\n"
            polygonalFaceLine += f" {vertixIndex + 1}"
        fileContent += polygonalFaceLine
        return fileContent

    def load(self, filepath: str):
        pass
