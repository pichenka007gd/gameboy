class Base():
    def __init__(self, gb):
        self.cpu = gb.cpu
        self.memory = gb.memory

class Timer(Base):
    def __init__(self, gb):
        super().__init__(gb)
        self.counter = 0
        self.delta = 0

    def update(self):
        self.counter += self.cpu.cycles - self.delta
        self.delta = self.cpu.cycles
        if self.counter >= 256:
            self.counter -= 256
            self.memory.io[0x04] = (self.memory.io[0x04] + 1) & 0xFF


class Common(Base):
    def __init__(self, gb):
        super().__init__(gb)
        self.timer = Timer(gb)

    def step(self):
        self.timer.update()
