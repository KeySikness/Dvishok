from OpenGL.GL import *
import numpy as np
import ctypes
from Dvishok.Shaders.Shader import Shader
from Dvishok.Sprite.Texture import Texture
from Dvishok.Sprite.Image.ImageSurface import ImageSurface
from pyglm import glm

class Image:
    def __init__(self, path: str):
        self.texture = Texture(path)
        self.width = self.texture.width
        self.height = self.texture.height

        # Используем тот же шейдер, что и SpriteSurface (работает с позицией, цветом и UV)
        self.shader = Shader(
            "Dvishok/Shaders/surface/vShader.glsl",
            "Dvishok/Shaders/surface/fShader.glsl"
        )

        self._setup_quad()

    def _setup_quad(self):
        """Создаёт VAO/VBO для центрированного квадрата размером 1x1.
           Вершины: позиция (x,y), цвет (r,g,b), UV (u,v). Цвет = белый."""
        vertices = np.array([
            # позиция    # цвет          # UV
             0, 0,  1.0, 1.0, 1.0,  0.0, 0.0,   # лево-низ
             1, 0,  1.0, 1.0, 1.0,  1.0, 0.0,   # право-низ
             1,  1,  1.0, 1.0, 1.0,  1.0, 1.0,   # право-верх
            0,  1,  1.0, 1.0, 1.0,  0.0, 1.0    # лево-верх
        ], dtype=np.float32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Индексы для двух треугольников
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Атрибут позиции (2 float)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 7 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Атрибут цвета (3 float)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 7 * 4, ctypes.c_void_p(2 * 4))
        glEnableVertexAttribArray(1)
        # Атрибут UV (2 float)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 7 * 4, ctypes.c_void_p(5 * 4))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)

    def render(self):
        """Возвращает ImageSurface для последующей отрисовки."""
        return ImageSurface(self)

    def draw(self, image_surface, x, y, surface_width, surface_height):
        self.shader.use()

        # Ортографическая проекция
        projection = glm.ortho(0, surface_width, surface_height, 0)
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader.program, "projection"),
            1, GL_FALSE, glm.value_ptr(projection)
        )

        # Модельная матрица: перенос в (x + w/2, y + h/2) и масштабирование
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(x + self.width/2, y + self.height/2, 0))
        model = glm.scale(model, glm.vec3(self.width, self.height, 1))
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader.program, "model"),
            1, GL_FALSE, glm.value_ptr(model)
        )

        # Привязка текстуры
        glActiveTexture(GL_TEXTURE0)
        self.texture.bind()
        glUniform1i(glGetUniformLocation(self.shader.program, "texture1"), 0)

        # Отрисовка
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)