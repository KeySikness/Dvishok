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

    def getViewMatrix(self) -> glm.mat4:
        return self.ViewMatrix

    def getProjectionMatrix(self) -> glm.mat4:
        return self.ProjectionMatrix

    def getPos(self) -> glm.vec3:
        return self.position

    def rebuildViewMatrix(self):
        self.ViewMatrix = glm.lookAt(self.position, self.target, glm.vec3(0, 1, 0))

    def rebuildProjectionMatrix(self):
        self.ProjectionMatrix = glm.perspective(self.fov, 16.0/9.0 , self.minDrawRange, self.maxDrawRange)

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

    def get_forward(self) -> glm.vec3:
        direction = glm.normalize(self.target - self.position)
        return direction

    def get_right(self) -> glm.vec3:
        forward = self.get_forward()
        world_up = glm.vec3(0, 1, 0)
        right = glm.normalize(glm.cross(forward, world_up))
        return right

    def get_up(self) -> glm.vec3:
        right = self.get_right()
        forward = self.get_forward()
        up = glm.cross(right, forward)
        return up

    def move_around_focus(self, delta: glm.vec3):
        right = self.get_right()
        up = self.get_up()
        forward = self.get_forward()
        self.position += right * delta.x + up * delta.y + forward * delta.z
        self.rebuildViewMatrix()

    def move(self, delta: glm.vec3):
        self.position.x += delta.x
        self.position.z += delta.z
        self.position.y += delta.y
        self.target.x += delta.x
        self.target.y += delta.y
        self.rebuildViewMatrix()