import glfw
from OpenGL.GL import *
import numpy as np

class Shader:
    def __init__(self, vertex_src, fragment_src):
        self.program = self._create_program(vertex_src, fragment_src)

    def _compile_shader(self, src, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, src)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            raise Exception(glGetShaderInfoLog(shader).decode())

        return shader

    def _create_program(self, v_src, f_src):
        v = self._compile_shader(v_src, GL_VERTEX_SHADER)
        f = self._compile_shader(f_src, GL_FRAGMENT_SHADER)

        program = glCreateProgram()
        glAttachShader(program, v)
        glAttachShader(program, f)
        glLinkProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            raise Exception(glGetProgramInfoLog(program))

        glDeleteShader(v)
        glDeleteShader(f)

        return program

    def use(self):
        glUseProgram(self.program)


class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.shader = Shader(
            """
            #version 330 core
            layout (location = 0) in vec3 aPos;
            void main()
            {
                gl_Position = vec4(aPos, 1.0);
            }
            """,
            """
            #version 330 core
            out vec4 FragColor;
            uniform vec4 color;
            void main()
            {
                FragColor = color;
            }
            """
        )

        self.vertices = np.array([
             0.5,  0.5, 0.0,
             0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0,
            -0.5,  0.5, 0.0
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

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, None)
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def fill(self, color):

        # фон (glClearColor)
        glClearColor(0.3, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # wireframe режим
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # рисуем прямоугольник
        self.shader.use()

        color_loc = glGetUniformLocation(self.shader.program, "color")
        glUniform4f(color_loc, *color)

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
    screen = engine.display.set_mode(800, 600)

    while engine.running:
        engine.process_input()

        screen.fill((1.0, 0.8, 0.2, 1.0))

        engine.update()

    engine.quit()