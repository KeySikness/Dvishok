import glfw
from OpenGL.GL import *
from Dvishok.Sprite.SpriteSurface import SpriteSurface
from Dvishok.Camera import Camera
from Dvishok.Sprite.Surface import Surface
from Dvishok.Sprite.Group import Group
from pyglm import glm

class Display:
    def __init__(self):
        self.camera = None
        self.window = None
        self.surface = None

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

        self.window = glfw.create_window(width, height, "Engine", None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")

        glfw.make_context_current(self.window)

        glViewport(0, 0, width, height)

        def resize(window, w, h):
            glViewport(0, 0, w, h)

        glfw.set_framebuffer_size_callback(self.window, resize)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.camera = Camera(width, height)

        self.surface = SpriteSurface(width, height, self.camera)
        return self.surface

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def running(self):
        return not glfw.window_should_close(self.window)

    def quit(self):
        glfw.terminate()