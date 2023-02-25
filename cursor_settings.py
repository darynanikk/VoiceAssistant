class Settings:
    def __init__(self):
        pass


class CursorSettings(Settings):
    def __init__(self, step, lookup_radius):
        self.step = step
        self.lookup_radius = lookup_radius
