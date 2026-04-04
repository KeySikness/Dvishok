import glfw
from pyglm import glm
from Display import Display

class Engine:
    def __init__(self):
        self.display = Display()
        self.running = True

    def process_input(self):
        if glfw.get_key(self.display.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            self.running = False

        if glfw.get_key(self.display.window, glfw.KEY_UP) == glfw.PRESS:
            self.display.move_camera(glm.vec3(0, -0.01, 0))  # вверх
        if glfw.get_key(self.display.window, glfw.KEY_DOWN) == glfw.PRESS:
            self.display.move_camera(glm.vec3(0, 0.01, 0))  # вниз
        if glfw.get_key(self.display.window, glfw.KEY_LEFT) == glfw.PRESS:
            self.display.move_camera(glm.vec3(0.01, 0, 0))  # влево
        if glfw.get_key(self.display.window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.display.move_camera(glm.vec3(-0.01, 0, 0))  # вправо
        if glfw.get_key(self.display.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.display.move_camera(glm.vec3(0, 0, -0.01))  # приблизить
        if glfw.get_key(self.display.window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.display.move_camera(glm.vec3(0, 0, 0.01))  # отдалить

    def update(self):
        glfw.swap_buffers(self.display.window)
        glfw.poll_events()

        if glfw.window_should_close(self.display.window):
            self.running = False

    def get_display(self):
        return self.display

    def quit(self):
        glfw.terminate()
