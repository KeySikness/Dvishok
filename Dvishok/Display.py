import glfw
from OpenGL.GL import *

from Dvishok.Sprite.BackgroundSurface import BackgroundSurface
from Dvishok.Sprite.SpriteSurface import SpriteSurface
from Dvishok.Sprite.Surface import Surface
from Dvishok.Camera import Camera
from Dvishok.Sprite.Group import Group
from pyglm import glm

class Display:
    def __init__(self):
        self.camera = None
        self.window = None
        self.surface = None
        self.title = "Engine team is GOAT"
        self.sprites = []

    def set_caption(self, title: str):
        self.title = title

    def blit(self, sprite):
        if type(sprite) == Surface:
            self.sprites.append(sprite)
            return True

        if type(sprite) == Group:
            for s in sprite.get():
                self.sprites.append(s)
            return True
        return False

    def update(self):
        for sprite in self.sprites:
            sprite.update()
            sprite.draw()

        self.sprites = []

    def set_mode(self, width: int, height: int):
        if not glfw.init():
            raise Exception("GLFW init failed")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

        self.window = glfw.create_window(width, height, self.title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")

        glfw.make_context_current(self.window)

        glViewport(0, 0, width, height)

        def resize(window, w, h):
            glViewport(0, 0, w, h)

        glfw.set_framebuffer_size_callback(self.window, resize)

        self.camera = Camera(width, height)
        background = BackgroundSurface(self.camera, width, height, color=(1.0, 0.8, 0.2, 1.0))
        self.sprites.append(background)
        return background