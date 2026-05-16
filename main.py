from Dvishok.Engine import Engine
from Dvishok.Sprite.Font.Font import Font
from Dvishok.Sprite.Sprite.Image import Image
from Dvishok.Sprite.Texture import Texture
from Dvishok.Sprite.Group import Group


if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1600, 900)

    font1 = Font("Dvishok/Assets/fonts/PublicPixel-rv0pA.ttf", 48)
    font2 = Font("Dvishok/Assets/fonts/PublicPixel-rv0pA.ttf", 30)

    text1 = font1.render(
    "Фуораов крутой текст урааа",
    (0.7, 1.0, 0.7),
        x = 200,
        y = 300
    )

    text2 = font2.render(
        "абвгдеёжзийклмнопрстуфхцчыьъщшэюя",
        (0.1, 0.5, 0.8),
        x = 400,
        y = 500
    )

    img = Image(600, 600, engine.get_display().camera, texture=Texture("Dvishok/Assets/images/MainIcon.jpg"), x = 0, y = 0)

    group = Group(img, text1, text2)

    while engine.running:
        engine.process_input()

        screen.draw()

        group.draw(screen)

        engine.update()

    engine.quit()