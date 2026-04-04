from Engine import Engine
from pyglm import glm


if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1600, 900)

    while engine.running:
        engine.process_input()

        screen.fill((1.0, 0.8, 0.2, 1.0))

        engine.update()

    engine.quit()