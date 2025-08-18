import numpy as np
from PIL import Image




class GPU:
    def __init__(self):
        self.screen_buffer = np.zeros((144, 160), dtype=np.uint8)  # 160x144 pixels
        self.line = 0
        self.mode = 0
        self.cycles = 0
        self.memory = None
        
        self.lcdc = 0  # LCD Control
        self.stat = 0  # LCD Status
        self.scy = 0   # Scroll Y
        self.scx = 0   # Scroll X
        self.ly = 0    # LCD Y Coordinate
        self.lyc = 0   # LY Compare
        self.bgp = 0   # BG Palette Data
        self.obp0 = 0  # Object Palette 0 Data
        self.obp1 = 0  # Object Palette 1 Data
        self.wy = 0    # Window Y Position
        self.wx = 0    # Window X Position
        
    def connect_memory(self, memory):
        self.memory = memory
        
    def step(self, cycles: int):
        self.cycles += cycles

        # Read registers (keep this at the start)
        self.lcdc = self.memory.read_byte(0xFF40)
        self.stat = self.memory.read_byte(0xFF41)
        self.scy = self.memory.read_byte(0xFF42)
        self.scx = self.memory.read_byte(0xFF43)
        self.ly = self.memory.read_byte(0xFF44)
        self.lyc = self.memory.read_byte(0xFF45)
        self.bgp = self.memory.read_byte(0xFF47)
        self.obp0 = self.memory.read_byte(0xFF48)
        self.obp1 = self.memory.read_byte(0xFF49)
        self.wy = self.memory.read_byte(0xFF4A)
        self.wx = self.memory.read_byte(0xFF4B)

        if self.cycles >= 456:
            # FIX: Render CURRENT line (0-143) BEFORE advancing
            if self.line < 144:  # Only render visible lines
                self.render_line()
            
            self.cycles -= 456
            self.line += 1
            self.ly = self.line
            self.memory.write_byte(0xFF44, self.ly)

            # Handle line state transitions
            if self.line == 144:  # Enter V-Blank
                self.mode = 1
            elif self.line >= 154:  # Reset frame
                self.line = 0
                self.ly = 0
                self.mode = 2
                self.memory.write_byte(0xFF44, self.ly)
                
    def render_line(self):
        
        """Отрисовка одной линии экрана"""
        if not (self.lcdc & 0x80):  # LCD выключен
            return 
            
        # Отрисовка фона
        if self.lcdc & 0x01:
            
            tile_map = 0x9800 if not (self.lcdc & 0x08) else 0x9C00
            tile_data = 0x8800 if not (self.lcdc & 0x10) else 0x8000
            
            for x in range(160):
                scroll_x = (x + self.scx) & 0xFF
                scroll_y = (self.line + self.scy) & 0xFF
                
                tile_x = scroll_x >> 3
                tile_y = scroll_y >> 3
                
                pixel_x = scroll_x & 7
                pixel_y = scroll_y & 7
                
                tile_addr = tile_map + tile_y * 32 + tile_x
                tile_num = self.memory.read_byte(tile_addr)
                
                if tile_data == 0x8800:
                    tile_num = ((tile_num + 128) & 0xFF) - 128
                    
                tile_addr = tile_data + tile_num * 16 + pixel_y * 2
                tile_low = self.memory.read_byte(tile_addr)
                tile_high = self.memory.read_byte(tile_addr + 1)
                
                color_bit = 7 - pixel_x
                color = ((tile_high >> color_bit) & 1) << 1 | ((tile_low >> color_bit) & 1)
                
                final_color = (self.bgp >> (color * 2)) & 3
                self.screen_buffer[self.line][x] = final_color
                
                
                
    def get_screen(self) -> np.ndarray:
        return self.screen_buffer.copy()
