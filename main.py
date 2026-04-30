import glfw

from Dvishok.Engine import Engine
from Dvishok.Sprite.Color import COLORS
from Dvishok.Sprite.Group import Group

from Dvishok.Sprite.SpriteSurface import SpriteSurface

if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1920, 1080)
    sprite1 = SpriteSurface(engine.display.camera, 200, 200, x=0, y=100, color=COLORS["black"])
    sprite2 = SpriteSurface(engine.display.camera, 200, 200, x=500, y=100)
    print(sprite1.collide(sprite2))
    group = Group(sprite1, sprite2)


    while engine.running:
        if engine.get_key(glfw.KEY_ESCAPE):
            engine.quit()

        screen.draw()
        engine.display.blit(group)

        engine.update()

