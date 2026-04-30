from Engine import Engine

if __name__ == "__main__":
    engine = Engine()
    screen = engine.display.set_mode(1600, 800)

    while engine.running:
        engine.process_input()

        screen.fill((0.3, 0.2, 0.2, 1.0))
        screen.draw()

        engine.update()

    engine.quit()