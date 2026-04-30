from Dvishok.Sprite.Surface import Surface
from OpenGL.GL import *

class BackgroundSurface(Surface):
    def __init__(self, camera, width, height, color=(0.2, 0.3, 0.4, 1.0)):
        super().__init__(camera, width, height)
        self.color = color

    def draw(self):
        glClearColor(*self.color)
        glClear(GL_COLOR_BUFFER_BIT)

    def set_color(self, color):
        self.color = color