import numpy as np

class GPU:
    def __init__(self):
        self.screen_buffer = np.zeros((144, 160), dtype=np.uint8)  # 160x144 pixels
        self.line = 0
        self.mode = 0
        self.cycles = 0
        self.memory = None
        
        # GPU регистры
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
        """Подключение памяти к GPU"""
        self.memory = memory
        
    def step(self, cycles: int):
        """Обновление GPU на указанное количество циклов"""
        self.cycles += cycles
        
        # Режимы GPU:
        # Mode 0: H-Blank (период после отрисовки линии)
        # Mode 1: V-Blank (период после отрисовки всего экрана)
        # Mode 2: Scanning OAM
        # Mode 3: Transferring Data to LCD Driver
        
        if self.cycles >= 456:  # Количество циклов на линию
            self.cycles -= 456
            self.line += 1
            self.ly = self.line
            
            if self.line == 144:  # Начало V-Blank
                self.mode = 1
            elif self.line >= 154:  # Конец V-Blank
                self.line = 0
                self.ly = 0
                self.mode = 2
            else:
                self.render_line()
                
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
                
                # Применяем палитру
                final_color = (self.bgp >> (color * 2)) & 3
                self.screen_buffer[self.line][x] = final_color
                
    def get_screen(self) -> np.ndarray:
        """Получить текущий буфер экрана"""
        return self.screen_buffer.copy()
