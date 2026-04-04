from Engine import Engine
from pyglm import glm

from SpriteSurface import SpriteSurface

if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1920, 1080)
    sprite1 = SpriteSurface(engine.display.camera, 200, 200, x=100, y=100)
    sprite2 = SpriteSurface(engine.display.camera, 200, 200, x=500, y=100)

    while engine.running:
        engine.process_input()

        screen.draw()
        engine.display.blit(sprite1)
        engine.display.blit(sprite2)

        engine.update()

    engine.quit()