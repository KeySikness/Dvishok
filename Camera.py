from pyglm import glm

class Camera:
    def __init__(self, cameraPosition: glm.vec3, cameraTarget: glm.vec3, minDrawRange: float, maxDrawRange:float, FOV: float = glm.radians(45)):
        self.ProjectionMatrix = None
        self.ViewMatrix = None
        self.position = cameraPosition
        self.target = cameraTarget
        self.fov = FOV
        self.minDrawRange = minDrawRange
        self.maxDrawRange = maxDrawRange

        self.rebuildViewMatrix()
        self.rebuildProjectionMatrix()

    def getViewMatrix(self):
        return self.ViewMatrix

    def getProjectionMatrix(self):
        return self.ProjectionMatrix

    def rebuildViewMatrix(self):
        self.ViewMatrix = glm.lookAt(self.position, self.target, glm.vec3(0, 1, 0))

    def rebuildProjectionMatrix(self):
        self.ProjectionMatrix = glm.perspective(self.fov, 16.0/9.0 , self.minDrawRange, self.maxDrawRange)

    def changePosition(self, newPos: glm.vec3):
        self.position = newPos
        self.rebuildViewMatrix()

    def changeFOV(self, newFOV: float):
        self.fov = newFOV
        self.rebuildProjectionMatrix()

    def changeTarget(self, newTarget: glm.vec3):
        self.target = newTarget
        self.rebuildViewMatrix()

    def changeMinDrawRange(self, newMinDrawRange: float):
        self.minDrawRange = newMinDrawRange
        self.rebuildProjectionMatrix()

    def changeMaxDrawRange(self, newMaxDrawRange: float):
        self.maxDrawRange = newMaxDrawRange
        self.rebuildProjectionMatrix()