from pyglm import glm

import Camera


class Model:
    def __init__(self, camera: Camera.Camera, transform: glm.mat4 = None, rotation: glm.mat4 = None, scale: glm.mat4 = None):
        self.MVP = None
        self.transform = transform if transform is not None else glm.mat4(1.0)
        self.rotation = rotation if rotation is not None else glm.mat4(1.0)
        self.scaling = scale if scale is not None else glm.mat4(1.0)
        self.camera = camera
        self.buildMVP()

    def translate(self, vector:glm.vec3):
        translation = glm.translate(glm.vec3(vector.x, vector.y, vector.z))
        self.transform = translation * self.transform

        self.buildMVP()

    def rotate(self, origin:glm.vec3, angle_rad: float):
        rot = glm.rotate(angle_rad, glm.vec3(0, 0, 1))
        transform_to_origin = glm.translate(glm.vec3(-origin.x, -origin.y, 0))
        transform_back = glm.translate(glm.vec3(origin.x, origin.y, 0))

        self.transform = transform_back * rot * transform_to_origin * self.transform

        self.rotation = rot * self.rotation

        self.buildMVP()

    def scale(self, vector:glm.vec3):
        scale = glm.scale(glm.vec3(vector.x, vector.y, 1))
        self.scaling = scale * self.scaling

        self.buildMVP()

    def getModel(self):
        return self.transform * self.rotation * self.scaling

    def decompose(self):
        scale = glm.vec3()
        orientation = glm.quat()
        translation = glm.vec3()
        skew = glm.vec3()
        perspective = glm.vec4()
        glm.decompose(self.getModel(), scale, orientation, translation, skew, perspective)
        return scale, orientation, translation, skew, perspective
    
    def buildMVP(self):
        self.MVP = self.camera.getProjectionMatrix() * self.camera.getViewMatrix() * self.getModel()
    
    def getMVP(self):
        return self.MVP