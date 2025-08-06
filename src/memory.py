class Memory:
    def __init__(self):
        self.rom = bytearray(0x8000)    # 32KB ROM
        self.vram = bytearray(0x2000)   # 8KB Video RAM
        self.ram = bytearray(0x2000)    # 8KB Internal RAM
        self.oam = bytearray(0x100)     # Sprite Attribute Memory
        self.io = bytearray(0x80)       # I/O Registers
        self.hram = bytearray(0x7F)     # High RAM
        
    def read_byte(self, address: int) -> int:
        """Чтение байта из памяти"""
        if address < 0x8000:  # ROM
            return self.rom[address]
        elif address < 0xA000:  # VRAM
            return self.vram[address - 0x8000]
        elif address < 0xC000:  # External RAM
            return 0  # TODO: Implement cartridge RAM
        elif address < 0xE000:  # Internal RAM
            return self.ram[address - 0xC000]
        elif address < 0xFE00:  # Echo RAM
            return self.ram[address - 0xE000]
        elif address < 0xFEA0:  # OAM
            return self.oam[address - 0xFE00]
        elif address < 0xFF00:  # Unusable
            return 0
        elif address < 0xFF80:  # I/O
            return self.io[address - 0xFF00]
        elif address < 0xFFFF:  # HRAM
            return self.hram[address - 0xFF80]
        else:  # Interrupt Enable Register
            IndexError("address error")

    def write_byte(self, address: int, value: int):
        """Запись байта в память"""
        if address < 0x8000:  # ROM
            pass  # ROM is read-only
        elif address < 0xA000:  # VRAM
            self.vram[address - 0x8000] = value
        elif address < 0xC000:  # External RAM
            pass  # TODO: Implement cartridge RAM
        elif address < 0xE000:  # Internal RAM
            self.ram[address - 0xC000] = value
        elif address < 0xFE00:  # Echo RAM
            self.ram[address - 0xE000] = value
        elif address < 0xFEA0:  # OAM
            self.oam[address - 0xFE00] = value
        elif address < 0xFF00:  # Unusable
            pass
        elif address < 0xFF80:  # I/O
            self.io[address - 0xFF00] = value
        elif address < 0xFFFF:  # HRAM
            self.hram[address - 0xFF80] = value
        else:  # Interrupt Enable Register
            IndexError("address error")
