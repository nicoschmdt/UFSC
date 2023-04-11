
from window import GraphicObject, Point, Line, Wireframe

class OBJFileDescriptor:

    def save(self, graphicObject: GraphicObject, filepath: str):
        if graphicObject == None:
            print("No object to be saved was provided")
            return
        if isinstance(graphicObject, Point):
            self.savePoint(graphicObject)
        elif isinstance(graphicObject, Line):
            self.saveLine(graphicObject)
        elif isinstance(graphicObject, Wireframe):
            self.saveWireframe(graphicObject)
 
    def getObjFileContentFromPoint(self, point: Point):
        pass

    def saveLine(self, line: Line):
        pass

    def saveWireframe(self, wireframe: Wireframe):
        pass

    def load(self, filepath: str):
        pass
