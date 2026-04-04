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

    def update(self):
        self.display.update()
        glfw.swap_buffers(self.display.window)
        glfw.poll_events()

        if glfw.window_should_close(self.display.window):
            self.running = False

    def get_display(self):
        return self.display

    def quit(self):
        glfw.terminate()
