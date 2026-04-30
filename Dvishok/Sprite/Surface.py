from OpenGL.GL import *

class Surface:
    def __init__(self, camera, width, height):
        self.camera = camera
        self.width = width
        self.height = height

    def draw(self):
        pass

    def update(self):
        pass

    def set_size(self, width, height):
        self.width = width
        self.height = height

