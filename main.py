from Dvishok.Engine import Engine
from Dvishok.Sprite.Font.Font import Font
from Dvishok.Sprite.Sprite.Image import Image
from Dvishok.Sprite.Sprite.SpriteSurface import SpriteSurface
from Dvishok.Sprite.Texture import Texture


if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1600, 900)

    font1 = Font("Dvishok/Assets/fonts/PublicPixel-rv0pA.ttf", 48)
    font2 = Font("Dvishok/Assets/fonts/PublicPixel-rv0pA.ttf", 30)

    text1 = font1.render(
    "Фуораов крутой текст урааа",
    (0.7, 1.0, 0.7),
    )

    text2 = font2.render(
        "абвгдежзийклмнопрстуфхцчыьъщшэюя",
        (0.1, 0.5, 0.8)
    )

    img = Image(600, 600, engine.get_display().camera, texture=Texture("Dvishok/Assets/images/MainIcon.jpg"))



    while engine.running:
        engine.process_input()

        screen.draw()


        screen.blit(img, 0, 0)
        screen.blit(text1, 200, 300)
        screen.blit(text2, 400, 500)



        engine.update()

    engine.quit()