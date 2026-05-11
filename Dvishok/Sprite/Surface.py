from OpenGL.GL import *
import numpy as np
import ctypes
from Dvishok.Shaders.Shader import Shader
from Dvishok.Sprite.Model import Model
from Dvishok.Camera import Camera
from pyglm import glm
from Dvishok.Sprite.Texture import Texture
from Dvishok.Sprite.Font import Font
from Dvishok.Sprite.Font.TextSurface import TextSurface
from Dvishok.Sprite.Image.ImageSurface import ImageSurface


class Surface:
    def __init__(self, camera, width, height, x = 0, y = 0):
        self.camera = camera
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def draw(self):
        pass

    def blit(self, obj, x, y):
        """Отображает переданный объект по определенным для него правилам """
        from Dvishok.Sprite.SpriteSurface import SpriteSurface
        if isinstance(obj, TextSurface):
            obj.font.draw(
                obj,
                x,
                y,
                self.width,
                self.height
            )
        if isinstance(obj, ImageSurface):
            obj.image.draw(obj, x, y, self.width, self.height)
        if isinstance(obj, SpriteSurface):
            pass
        pass

    def update(self):
        pass

    def set_size(self, width, height):
        self.width = width
        self.height = height