import glfw
from OpenGL.GL import *
import numpy as np
import math
import ctypes
from Shader import Shader
from Model import Model
from Camera import Camera
from pyglm import glm

class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.shader = Shader(
            "shaders/vShader.glsl",
            "shaders/fShader.glsl"
        )

        self.camera = Camera(glm.vec3(1, 0, 1), glm.vec3(0, 0, 0),0.1, 100)
        self.model = Model(self.camera)
        self.model.translate(glm.vec3(0,0,0))

        self.vertices = np.array([    
             0.5,  0.5, 0.0,   1.0, 0.0, 0.0,  # top right (red)
             0.5, -0.5, 0.0,   0.0, 1.0, 0.0,  # bottom right (green)
            -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,  # bottom left (blue)
            -0.5,  0.5, 0.0,   1.0, 1.0, 0.0   # top left (yellow)
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 3,
            1, 2, 3
        ], dtype=np.uint32)

        self._setup_buffers()

    def _setup_buffers(self):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        stride = 6 * 4  # 6 флоатов на 4 байта

        # позиции
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        #  (не перепутай пж_)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def fill(self, color):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        self.shader.use()

        time = glfw.get_time()
        angle = time  # скорость вращения
        # cos_a = math.cos(angle)
        # sin_a = math.sin(angle)

        # # model матрица (+вращение как пример для работы юниформ)
        # model = np.array(
        #     [[cos_a, -sin_a, 0.0, 0.0],
        #      [sin_a, cos_a, 0.0, 0.0],
        #      [0.0, 0.0, 1.0, 0.0],
        #      [0.0, 0.0, 0.0, 1.0]],
        #     dtype=np.float32)

        self.shader.set_mat4("model", glm.value_ptr(self.model.getMVP()))

        # # cдвиг право+низ
        # model[3][0] = 0.5
        # model[3][1] = -0.5
        #
        # # масштаб
        # model[0][0] = 0.5
        # model[1][1] = 0.5

        # model_loc = glGetUniformLocation(self.shader.program, "model")
        # glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)


class Display:
    def __init__(self):
        self.window = None
        self.surface = None

    def set_mode(self, width, height):
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

        self.surface = Surface(width, height)
        return self.surface


class Engine:
    def __init__(self):
        self.display = Display()
        self.running = True

    def process_input(self):
        if glfw.get_key(self.display.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            self.running = False

    def update(self):
        glfw.swap_buffers(self.display.window)
        glfw.poll_events()

        if glfw.window_should_close(self.display.window):
            self.running = False

    def quit(self):
        glfw.terminate()


if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1600, 900)

    while engine.running:
        engine.process_input()

        screen.fill((1.0, 0.8, 0.2, 1.0))

        engine.update()

    engine.quit()