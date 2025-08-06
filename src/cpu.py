class CPU:
    def __init__(self):
        self.a = 0 # акум
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0
        self.f = 0 # флаги
        self.pc = 0 # счетчик
        self.sp = 0xFFFE  # стэк
        self.cycles = 0
        self.memory = None
        self.interrupts_enabled = False
        self.halted = False #
        self.stopped = False
        
        self.FLAG_Z = 0x80 # устанавливается если результат равен 0
        self.FLAG_N = 0x40 # устанавливается после операции вычитания
        self.FLAG_H = 0x20 # если был перенос между младшими и старшими 4 битами
        self.FLAG_C = 0x10 # если был перенос из старшего бита или заимствование
        

        self._register_pairs = {
            'BC': (self.b, self.c),
            'DE': (self.d, self.e),
            'HL': (self.h, self.l),
            'AF': (self.a, self.f)
        }
        
    def get_register_pair(self, pair):
        high, low = self._register_pairs[pair]
        return (high << 8) | low
        
    def set_register_pair(self, pair, value):
        high = (value >> 8) & 0xFF
        low = value & 0xFF
        if pair == 'BC':
            self.b, self.c = high, low
        elif pair == 'DE':
            self.d, self.e = high, low
        elif pair == 'HL':
            self.h, self.l = high, low
        elif pair == 'AF':
            self.a, self.f = high, low
        
    def connect_memory(self, memory):
        self.memory = memory
        print(self.memory)
        
    def reset(self):
        #self.__init__()
        self.pc = 0x100  # Точка входа для картриджей
        
    def get_flag(self, flag):
        return (self.f & flag) != 0
        
    def set_flag(self, flag, value):
        if value:
            self.f |= flag
        else:
            self.f &= ~flag
            
    def read_byte(self):
        value = self.memory.read_byte(self.pc)
        self.pc += 1
        return value
        
    def read_word(self):
        value = self.memory.read_byte(self.pc) | (self.memory.read_byte(self.pc + 1) << 8)
        self.pc += 2
        return value
        
    def push(self, value):
        self.sp -= 2
        self.memory.write_byte(self.sp, value & 0xFF)
        self.memory.write_byte(self.sp + 1, (value >> 8) & 0xFF)
        
    def pop(self):
        value = self.memory.read_byte(self.sp) | (self.memory.read_byte(self.sp + 1) << 8)
        self.sp += 2
        return value
        
    def step(self):
        opcode = self.read_byte()
        self.execute_instruction(opcode)
        return self.cycles
        
    def add_a(self, value):
        temp = self.a + value
        self.set_flag(self.FLAG_H, (self.a & 0x0F) + (value & 0x0F) > 0x0F)
        self.set_flag(self.FLAG_C, temp > 0xFF)
        self.a = temp & 0xFF
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, False)
        
    def sub_a(self, value):
        temp = self.a - value
        self.set_flag(self.FLAG_H, (self.a & 0x0F) < (value & 0x0F))
        self.set_flag(self.FLAG_C, temp < 0)
        self.a = temp & 0xFF
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, True)
        
    def adc_a(self, value):
        carry = 1 if self.get_flag(self.FLAG_C) else 0
        temp = self.a + value + carry
        self.set_flag(self.FLAG_H, (self.a & 0x0F) + (value & 0x0F) + carry > 0x0F)
        self.set_flag(self.FLAG_C, temp > 0xFF)
        self.a = temp & 0xFF
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, False)
        
    def sbc_a(self, value):
        carry = 1 if self.get_flag(self.FLAG_C) else 0
        temp = self.a - value - carry
        self.set_flag(self.FLAG_H, (self.a & 0x0F) < ((value & 0x0F) + carry))
        self.set_flag(self.FLAG_C, temp < 0)
        self.a = temp & 0xFF
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, True)
        
    def and_a(self, value):
        self.a &= value
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, True)
        self.set_flag(self.FLAG_C, False)
        
    def or_a(self, value):
        self.a |= value
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, False)
        
    def xor_a(self, value):
        self.a ^= value
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, False)
        
    def cp_a(self, value):
        temp = self.a - value
        self.set_flag(self.FLAG_Z, temp & 0xFF == 0)
        self.set_flag(self.FLAG_N, True)
        self.set_flag(self.FLAG_H, (self.a & 0x0F) < (value & 0x0F))
        self.set_flag(self.FLAG_C, temp < 0)
        
    def execute_instruction(self, opcode):
        self.cycles = 4  # Базовое количество циклов
        
        if opcode == 0x00:  # NOP
            pass
            
        # 8-битные загрузки
        elif opcode == 0x3E:  # LD A,n
            self.a = self.read_byte()
            self.cycles = 8
        elif opcode == 0x06:  # LD B,n
            self.b = self.read_byte()
            self.cycles = 8
        elif opcode == 0x0E:  # LD C,n
            self.c = self.read_byte()
            self.cycles = 8
        elif opcode == 0x16:  # LD D,n
            self.d = self.read_byte()
            self.cycles = 8
        elif opcode == 0x1E:  # LD E,n
            self.e = self.read_byte()
            self.cycles = 8
        elif opcode == 0x26:  # LD H,n
            self.h = self.read_byte()
            self.cycles = 8
        elif opcode == 0x2E:  # LD L,n
            self.l = self.read_byte()
            self.cycles = 8
            
        # 16-битные загрузки
        elif opcode == 0x01:  # LD BC,nn
            self.set_register_pair('BC', self.read_word())
            self.cycles = 12
        elif opcode == 0x11:  # LD DE,nn
            self.set_register_pair('DE', self.read_word())
            self.cycles = 12
        elif opcode == 0x21:  # LD HL,nn
            self.set_register_pair('HL', self.read_word())
            self.cycles = 12
        elif opcode == 0x31:  # LD SP,nn
            self.sp = self.read_word()
            self.cycles = 12
            
        # Арифметические операции
        elif opcode == 0x80:  # ADD A,B
            self.add_a(self.b)
        elif opcode == 0x81:  # ADD A,C
            self.add_a(self.c)
        elif opcode == 0x82:  # ADD A,D
            self.add_a(self.d)
        elif opcode == 0x83:  # ADD A,E
            self.add_a(self.e)
        elif opcode == 0x84:  # ADD A,H
            self.add_a(self.h)
        elif opcode == 0x85:  # ADD A,L
            self.add_a(self.l)
        elif opcode == 0x86:  # ADD A,(HL)
            self.add_a(self.memory.read_byte(self.get_register_pair('HL')))
            self.cycles = 8
        elif opcode == 0x87:  # ADD A,A
            self.add_a(self.a)
            
        # Логические операции
        elif opcode == 0xA0:  # AND B
            self.and_a(self.b)
        elif opcode == 0xA1:  # AND C
            self.and_a(self.c)
        elif opcode == 0xB0:  # OR B
            self.or_a(self.b)
        elif opcode == 0xB1:  # OR C
            self.or_a(self.c)
        elif opcode == 0xA8:  # XOR B
            self.xor_a(self.b)
        elif opcode == 0xA9:  # XOR C
            self.xor_a(self.c)
        elif opcode == 0xAF:  # XOR A
            self.xor_a(self.a)
            
        # Переходы
        elif opcode == 0xC3:  # JP nn
            self.pc = self.read_word()
            self.cycles = 16
        elif opcode == 0xC2:  # JP NZ,nn
            address = self.read_word()
            if not self.get_flag(self.FLAG_Z):
                self.pc = address
                self.cycles = 16
            else:
                self.cycles = 12
                
        # Вызовы подпрограмм
        elif opcode == 0xCD:  # CALL nn
            address = self.read_word()
            self.push(self.pc)
            self.pc = address
            self.cycles = 24
            
        # Возвраты
        elif opcode == 0xC9:  # RET
            self.pc = self.pop()
            self.cycles = 16
            
        # Управление прерываниями
        elif opcode == 0xF3:  # DI
            self.interrupts_enabled = False
        elif opcode == 0xFB:  # EI
            self.interrupts_enabled = True
            
        # HALT и STOP
        elif opcode == 0x76:  # HALT
            self.halted = True
        elif opcode == 0x10:  # STOP
            self.stopped = True
            
        else:
            print(f"Unknown opcode: 0x{opcode:02X}")
            self.cycles = 4
