from OpenGL.GL import *
import numpy as np
import ctypes
from Shader import Shader
from Model import Model
from Camera import Camera
from pyglm import glm
from Texture import Texture
from Font import Font


class Surface:
    def __init__(self, width: int, height: int, camera: Camera):
        self.width = width
        self.height = height
        self.camera = camera
        self.texture = Texture("assets/images/MainIcon.jpg")

        self.shader = Shader(
            "shaders/surface/vShader.glsl",
            "shaders/surface/fShader.glsl"
        )

        self.font = Font(
            "assets/fonts/PublicPixel-rv0pA.ttf",
            32
        )

        self.text_surface = self.font.render(
            "Hello world я фиг знает",
            (1.0, 1.0, 1.0)
        )

        self.model = Model(self.camera)

        self.vertices = np.array([
             800, 450, 0.0,     1.0, 0.0, 0.0,    1.0,1.0,
             800, 0,   0.0,     0.0, 1.0, 0.0,    1.0,0.0,
             0,   0,   0.0,     0.0, 0.0, 1.0,    0.0,0.0,
             0,   450, 0.0,     1.0, 1.0, 0.0,    0.0,1.0
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

        stride = 8 * 4  # 8 флоатов на 4 байта

        # позиции
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        #  (не перепутай пж_)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        # UV
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)

    def fill(self, color):
        glClearColor(*color)
        glClear(GL_COLOR_BUFFER_BIT)

    def blit(self, text_surface, x, y):
        text_surface.font.draw(
            text_surface,
            x,
            y,
            self.width,
            self.height
        )

    def draw(self):
        self.shader.use()

        glActiveTexture(GL_TEXTURE0)

        self.texture.bind()

        glUniform1i(
            glGetUniformLocation(self.shader.program, "texture1"),
            0
        )

        self.shader.set_mat4(
            "model",
            glm.value_ptr(self.model.getMVP())
        )

        glBindVertexArray(self.VAO)

        glDrawElements(
            GL_TRIANGLES,
            6,
            GL_UNSIGNED_INT,
            None
        )

        glBindVertexArray(0)

        self.blit(self.text_surface, 100, 100)