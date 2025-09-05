class Memory:
    def __init__(self):
        self.rom = bytearray(0x8000*2)
        self.rom_bank = 1
        self.vram = bytearray(0x2000)     # 8 KB VRAM
        self.ram = bytearray(0x2000)      # 8 KB Internal RAM
        self.cart_ram = bytearray(0x2000) # Cartridge RAM (размер варьируется)
        self.oam = bytearray(0xA0)        # Sprite Attribute Table (160 bytes)
        self.io = bytearray(0x80)         # I/O Registers (128 bytes)
        self.hram = bytearray(0x7F)       # High RAM (127 bytes)s
        self.interrupt_enable = 0x00      # 0xFFFF
        self.last = 0x100
        
    def read_byte(self, address: int) -> int:
        if 0x0000 <= address < 0x4000:
            return self.rom[address]
        elif 0x4000 <= address < 0x8000:
            bank_offset = self.rom_bank * 0x4000
            rom_addr = bank_offset + (address - 0x4000)
            if rom_addr < len(self.rom):
                return self.rom[rom_addr]
            else:
                return 0xFF
        elif 0x8000 <= address < 0xA000:
            return self.vram[address - 0x8000]
        elif 0xA000 <= address < 0xC000:
            # External cartridge RAM (если подключена)
            return self.cart_ram[(address - 0xA000) % len(self.cart_ram)]
        elif 0xC000 <= address < 0xE000:
            return self.ram[address - 0xC000]
        elif 0xE000 <= address < 0xFE00:
            # Echo RAM (зеркало 0xC000-0xDE00)
            return self.ram[address - 0xE000]
        elif 0xFE00 <= address < 0xFEA0:
            return self.oam[address - 0xFE00]
        elif 0xFEA0 <= address < 0xFF00:
            # Неиспользуемая область (не разрешено обращаться)
            return 0x00 #0xFF # in gbi is 0x00
        elif 0xFF00 <= address < 0xFF80:
            return self.io[address - 0xFF00]
        elif 0xFF80 <= address < 0xFFFF:
            return self.hram[address - 0xFF80]
        elif address == 0xFFFF:
            return self.interrupt_enable
        else:
            raise IndexError(f"Address out of range: {address:#04x}")

    def write_byte(self, address: int, value: int):
        self.last = address
        value = value & 0xFF  # только байт
        if 0x0000 <= address < 0x8000:
            # Здесь обычно реализуется переключение банков ROM и RAM — это MBC, никуда не пишем
            self._mbc_write(address, value)
        elif 0x8000 <= address < 0xA000:
            self.vram[address - 0x8000] = value
        elif 0xA000 <= address < 0xC000:
            self.cart_ram[(address - 0xA000) % len(self.cart_ram)] = value
        elif 0xC000 <= address < 0xE000:
            self.ram[address - 0xC000] = value
        elif 0xE000 <= address < 0xFE00:
            self.ram[address - 0xE000] = value
        elif 0xFE00 <= address < 0xFEA0:
            self.oam[address - 0xFE00] = value
        elif 0xFEA0 <= address < 0xFF00:
            # Неиспользуемый диапазон
            pass
        elif 0xFF00 <= address < 0xFF80:
            if address == 0xFF04:
                self.io[address - 0xFF00] = 0
                return
            self.io[address - 0xFF00] = value
        elif 0xFF80 <= address < 0xFFFF:
            self.hram[address - 0xFF80] = value
        elif address == 0xFFFF:
            self.interrupt_enable = value
        else:
            raise IndexError(f"Address out of range: {address:#04x}")

    def _mbc_write(self, address: int, value: int):
        if 0x2000 <= address < 0x4000:
            bank = value & 0x1F
            print("bank: {bank:X02}")
            if bank == 0:
                bank = 1
            self.rom_bank = bank