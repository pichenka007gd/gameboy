class Cartridge:
    def __init__(self):
        self.rom_data = None
        self.rom_size = 0
        self.ram_size = 0
        self.title = ""
        
    def load(self, rom_path: str) -> bool:
        try:
            with open(rom_path, 'rb') as f:
                self.rom_data = f.read()
                return True
        except:
            return False
