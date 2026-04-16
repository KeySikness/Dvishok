# sprite_surface.py
import numpy as np
import ctypes
from OpenGL.GL import *

from Model import Model
from Surface import Surface
from Shader import Shader
from pyglm import glm

class SpriteSurface(Surface):
    def __init__(self, camera, width, height, x=0, y=0, color = None, shader=None):
        super().__init__(camera, width, height)
        if color is None:
            self.color = [1, 0, 0]
        self.width = width
        self.height = height
        self.camera = camera

        self.shader = Shader(
            "shaders/vShader.glsl",
            "shaders/fShader.glsl"
        )

        self.model = Model(self.camera)
        self.model.scale(glm.vec3(self.width, self.height, 0))
        self.model.translate(glm.vec3(x, y, 0))

        self.vertices = np.array([
            1, 1, 0.0, self.color[0], self.color[1], self.color[2],  # bottom right (red)
            1, 0.0, 0.0, self.color[0], self.color[1], self.color[2],  # top right (green)
            0.0, 0.0, 0.0, self.color[0], self.color[1], self.color[2],  # top left (blue)
            0.0, 1, 0.0, self.color[0], self.color[1], self.color[2] # bottom left (yellow)
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

    def update(self):
        self.model.translate(glm.vec3(.01, .01, 0))

    def draw(self):
        self.shader.use()
        self.shader.set_mat4("model", glm.value_ptr(self.model.getMVP()))
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)