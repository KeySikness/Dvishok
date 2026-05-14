from OpenGL.GL import *
import numpy as np
import ctypes
from Dvishok.Shaders.Shader import Shader
from Dvishok.Camera import Camera
from pyglm import glm
from Dvishok.Sprite.Texture import Texture
from Dvishok.Sprite.Sprite.Surface import Surface
from Dvishok.Sprite.Rect import Rect


class SpriteSurface(Surface):
    def __init__(self, width: int, height: int, camera: Camera, color = None, x=0, y=0, texture = None):
        super().__init__(camera, width, height, x, y)
        self.width = width
        self.height = height
        self.camera = camera
        if color is None:
            self.color = [1, 0, 0]
        else:
            self.color = [c / 255.0 for c in color]
        self.texture = texture

        self.shader = Shader(
            "Dvishok/Shaders/surface/vShader.glsl",
            "Dvishok/Shaders/surface/fShader.glsl"
        )

        self.rect = Rect(self.camera)
        self.rect.scale(glm.vec3(self.width, self.height, 0))
        self.rect.x += x
        self.rect.y += y

        self.vertices = np.array([
             1, 1, 0.0,     self.color[0], self.color[1], self.color[2],    1.0,1.0,
             1, 0.0, 0.0,     self.color[0], self.color[1], self.color[2],    1.0,0.0,
             0.0, 0.0, 0.0,     self.color[0], self.color[1], self.color[2],    0.0,0.0,
             0.0, 1, 0.0,     self.color[0], self.color[1], self.color[2],    0.0,1.0
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 3,
            1, 2, 3
        ], dtype=np.uint32)

        self._setup_buffers()

    def _setup_buffers(self):
        if self.texture:
            pass
        else:
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


    def draw(self):
        if self.texture:
            pass
        else:
            self.shader.use()
            self.shader.set_mat4("model", glm.value_ptr(self.rect.getMVP()))
            glBindVertexArray(self.VAO)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)

    def collide(self, obj):
        points = [obj.rect.top_left, obj.rect.top_right, obj.rect.bottom_left, obj.rect.bottom_right]

        if any(self.collide_point(p) for p in points):
            return True
        return False

    def collide_point(self, obj):
        return (self.rect.x <= obj[0] <= self.rect.x + self.rect.width) and (
                    self.rect.y <= obj[1] <= self.rect.y + self.rect.height)

    def set_color(self, color):
        self.color = [c / 255.0 for c in color]

        self.vertices = np.array([
            1, 1, 0.0, self.color[0], self.color[1], self.color[2],
            1, 0.0, 0.0, self.color[0], self.color[1], self.color[2],
            0.0, 0.0, 0.0, self.color[0], self.color[1], self.color[2],
            0.0, 1, 0.0, self.color[0], self.color[1], self.color[2]
        ], dtype=np.float32)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBindBuffer(GL_ARRAY_BUFFER, 0)