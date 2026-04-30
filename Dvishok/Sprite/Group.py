from Dvishok.Sprite.Surface import Surface


class Group:
    def __init__(self, *obj):
        self.sprites = [o for o in obj]

    def update(self, *args):
        if not args:
            for sprite in self.sprites:
                sprite.update()
        else:
            pass

    def blit(self):
        for sprite in self.sprites:
            sprite.blit()

    def get_by_id(self, obj_id):
        return self.sprites[obj_id]

    def get(self):
        return self.sprites

    def add(self, *obj):
        for sprite in obj:
            self.sprites.append(sprite)

    def pop(self, element):
        if type(element) == int:
            self.sprites.pop(element)
            return True
        if type(element) == Surface:
            self.sprites.remove(element)
            return True
        else:
            return False