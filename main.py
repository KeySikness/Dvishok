from Engine import Engine
from Font import Font

if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1600, 800)

    font1 = Font("assets/fonts/PublicPixel-rv0pA.ttf", 48)
    font2 = Font("assets/fonts/PublicPixel-rv0pA.ttf", 30)

    text1 = font1.render(
    "Фуораов крутой текст урааа",
    (0.7, 1.0, 0.7),
    )
    text2 = font2.render(
        "абвгдежзийклмнопрстуфхцчыьъщшэюя",
        (0.1, 0.5, 0.8)
    )

    while engine.running:
        engine.process_input()

        screen.fill((0.3, 0.2, 0.2, 1.0))

        screen.draw()

        screen.blit(text1, 200, 300)
        screen.blit(text2, 400, 500)

        engine.update()

    engine.quit()