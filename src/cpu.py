from memory import Memory
from logger import Logger
import ctypes


log = Logger()


class CPU:
    def __init__(self) -> None:
        self.a = 0 # акум
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0
        self.f = 0x00000000 # флаги первые 4 бита
        self.pc = 0x100 # счетчик
        self.sp = 0x0000 # стэк
        self.cycles = 0
        try: self.memory
        except: self.memory = None
        self.interrupts_enabled = False
        self.halted = False
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

        self.temp = 0x00 
        self.opcode = 0x00
        
    def get_reg_pair(self, pair: str) -> int:
        high, low = self.get_reg(pair[0]), self.get_reg(pair[1])
        return (high << 8) | low
        
    def set_reg_pair(self, pair: str, value: int) -> int:
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
        
    def connect_memory(self, memory: Memory) -> None:
        self.memory = memory
        
    def reset(self) -> None:
        self.__init__()
        
    def get_flag(self, flag: int) -> bool:
        return (self.f & flag) != 0
        
    def set_flag(self, flag: int, value: bool) -> None:
        if value:
            self.f |= flag
        else:
            self.f &= ~flag
            
    def read_byte(self) -> int:
        value = self.memory.read_byte(self.pc)
        self.pc += 1
        return value
        
    def read_word(self) -> int:
        value = self.memory.read_byte(self.pc) | (self.memory.read_byte(self.pc + 1) << 8)
        self.pc += 2
        return value
        
    def push(self, value: int) -> None:
        self.sp -= 2
        self.memory.write_byte(self.sp, value & 0xFF)
        self.memory.write_byte(self.sp + 1, (value >> 8) & 0xFF)
        
    def pop(self) -> int:
        value = self.memory.read_byte(self.sp) | (self.memory.read_byte(self.sp + 1) << 8)
        #print(f"{self.pc:02X}")
        #print(f"{value:02X}")
        self.sp += 2
        return value
    
    #@log.step_log()
    def step(self) -> int:
        opcode = self.read_byte()
        self.execute_instruction(opcode)
        return self.cycles
        
    def add_reg(self, reg: str, value: int) -> None:
        temp = self.get_reg(reg) + value
        self.set_flag(self.FLAG_H, (self.a & 0x0F) + (value & 0x0F) > 0x0F)
        self.set_flag(self.FLAG_C, temp > 0xFF)
        self.set_reg(reg, temp & 0xFF)
        self.set_flag(self.FLAG_Z, self.get_reg(reg) == 0)
        self.set_flag(self.FLAG_N, False)

    def add_reg_pair(self, regpair: str, value: int) -> None:
        reg = self.get_reg_pair(regpair)
        result = (reg + value)

        self.set_reg_pair(regpair, result & 0xFFFF)

        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, result > 0x0FFF)
        self.set_flag(self.FLAG_C, result > 0xFFFF)
        
    def sub_reg(self, reg: str, value: int) -> None:
        temp = self.get_reg(reg) - value
        self.set_flag(self.FLAG_H, (self.get_reg(reg) & 0x0F) < (value & 0x0F))
        self.set_flag(self.FLAG_C, temp < 0)
        self.set_reg(reg, temp & 0xFF)
        self.set_flag(self.FLAG_Z, self.get_reg(reg) == 0)
        self.set_flag(self.FLAG_N, True)

    def sub_reg_pair(self, regpair: str, value: int) -> None:
        temp = self.get_register_pair(regpair) - value
        self.set_flag(self.FLAG_H, (self.get_register_pair(regpair) & 0xFFF) < (value & 0xFFF))
        self.set_flag(self.FLAG_C, temp < 0)
        self.set_reg_pair(regpair, temp & 0xFFFF)
        self.set_flag(self.FLAG_N, True)

    def adc_reg(self, reg: str, value: int) -> None:
        carry = 1 if self.get_flag(self.FLAG_C) else 0
        temp = self.get_reg(reg) + value + carry
        self.set_flag(self.FLAG_H, (self.get_reg(reg) & 0x0F) + (value & 0x0F) + carry > 0x0F)
        self.set_flag(self.FLAG_C, temp > 0xFF)
        self.set_reg(reg, temp & 0xFF)
        self.set_flag(self.FLAG_Z, self.get_reg(reg) == 0)
        self.set_flag(self.FLAG_N, False)
        
    def sbc_reg(self, reg: str, value: int) -> None:
        carry = 1 if self.get_flag(self.FLAG_C) else 0
        temp = self.get_reg(reg) - value - carry
        self.set_flag(self.FLAG_H, (self.get_reg(reg) & 0x0F) < ((value & 0x0F) + carry))
        self.set_flag(self.FLAG_C, temp < 0)
        self.set_reg(reg, temp & 0xFF)
        self.set_flag(self.FLAG_Z, self.a == 0)
        self.set_flag(self.FLAG_N, True)
        
    def and_reg(self, reg: str, value: int) -> None:
        self.set_reg(reg, self.get_reg(reg) & value)
        self.set_flag(self.FLAG_Z, self.get_reg(reg) == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, True)
        self.set_flag(self.FLAG_C, False)
        
    def or_reg(self, reg: str, value: int) -> None:
        self.set_reg(reg, self.get_reg(reg) | value)
        self.set_flag(self.FLAG_Z, self.get_reg(reg) == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, False)
        
    def xor_reg(self, reg: str, value: int) -> None:
        self.set_reg(reg, self.get_reg(reg) ^ value)
        self.set_flag(self.FLAG_Z, self.get_reg(reg) == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, False)
        
    def cp_reg(self, reg: str, value: int) -> None:
        temp = self.get_reg(reg) - value
        self.set_flag(self.FLAG_Z, temp & 0xFF == 0)
        self.set_flag(self.FLAG_N, True)
        self.set_flag(self.FLAG_H, (self.get_reg(reg) & 0x0F) < (value & 0x0F))
        self.set_flag(self.FLAG_C, temp < 0)

    def get_reg(self, reg: str) -> int:
        return getattr(self, reg.lower())

    def set_reg(self, reg: str, value: int) -> None:
        if reg.lower() in ["a", "b", "c", "d", "e", "h", "l", "f"]:
            setattr(self, reg.lower(), value)
        elif reg.lower() in ["(hl)"]:
            self.memory.write_byte(self.get_reg_pair("HL"), value)
        else:
            IndexError(f"register name error: {reg}")

    def inc_reg(self, reg: str) -> None:
        temp = self.get_reg(reg)
        result = (temp + 1) & 0xFF
        self.set_reg(reg, result)
        self.set_flag(self.FLAG_Z, result == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, (temp & 0x0F) + 1 > 0x0F)

    def inc_reg_pair(self, regpair: str) -> None:
        temp = self.get_reg_pair(regpair)
        result = (temp + 1) & 0xFFFF
        self.set_reg_pair(regpair, result)

    def dec_reg(self, reg: str) -> None:
        temp = self.get_reg(reg)
        result = (temp - 1) & 0xFF
        self.set_reg(reg, result)
        self.set_flag(self.FLAG_Z, result == 0)
        self.set_flag(self.FLAG_N, True)
        self.set_flag(self.FLAG_H, (temp & 0x0F) == 0)

    def dec_reg_pair(self, regpair: str) -> None:
        temp = self.get_reg_pair(regpair)
        result = (temp - 1) & 0xFFFF
        self.set_reg_pair(regpair, result)

    def rlc_reg(self, reg):
        self.set_reg(reg, self.get_reg(reg) << 1) | (self.get_reg(reg) >> 7)
        self.set_flag(self.FLAG_Z, temp == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, self.get_reg(reg) & 0x80)

    def rrc_reg(self, reg):
        temp = (self.get_reg(reg) >> 1) | ((self.get_reg(reg) & 0x01) << 7)
        self.set_flag(self.FLAG_Z, temp == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, self.get_reg(reg) & 0x01)
        self.set_reg(reg, temp)

    def srl_reg(self, reg):
        temp = self.get_reg(reg) >> 1
        self.set_flag(self.FLAG_Z, temp == 0)
        self.set_flag(self.FLAG_N, False)
        self.set_flag(self.FLAG_H, False)
        self.set_flag(self.FLAG_C, self.get_reg(reg) & 0x01)
        self.set_reg(reg, temp)

    def execute_instruction(self, opcode: int) -> int:
        self.opcode = opcode

        def cycles(cycles: int) -> None:
            self.cycles += cycles
            return cycles

        # mnemonic # flags # bytes cycles

        if opcode == 0x00:   # NOP         | ---- | 1 4
            pass
            cycles(4)
        elif opcode == 0x01: # LD BC,d16   | ---- | 3 12
            self.set_reg_pair("BC", self.read_word())
            cycles(12)
        elif opcode == 0x02: # LD (BC),A   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair('BC'), self.a)
            cycles(8)
        elif opcode == 0x03: # INC BC      | ---- | 1 8
            self.inc_reg_pair("BC")
            cycles(8)
        elif opcode == 0x04: # INC B       | Z0H- | 1 4
            self.inc_reg("B")
            cycles(4)
        elif opcode == 0x05: # DEC B       | Z1H- | 1 4
            self.dec_reg("B")
            cycles(4)
        elif opcode == 0x06: # LD B,d8     | ---- | 2 8
            self.b = self.read_byte()
            cycles(8)
        elif opcode == 0x07: # RLCA        | 000C | 1 4
            carry = (self.a & 0x80) >> 7
            self.a = ((self.a << 1) | carry) & 0xFF
            self.set_flag(self.FLAG_C, carry == 1)
            self.set_flag(self.FLAG_Z, False)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, False)
            cycles(4)
        elif opcode == 0x08: # LD (a16),SP | ---- | 3 20
            addr = self.read_word()
            self.memory.write_byte(addr, self.sp & 0xFF)
            self.memory.write_byte(addr + 1, (self.sp >> 8) & 0xFF)
            cycles(20)
        elif opcode == 0x09: # ADD HL,BC   | -0HC | 1 8
            self.add_reg_pair("HL", self.get_reg_pair("BC"))
            cycles(8)
        elif opcode == 0x0A: # LD A,(BC)   | ---- | 1 8
            self.a = self.memory.read_byte(self.get_reg_pair("BC"))
            cycles(8)
        elif opcode == 0x0B: # DEC BC      | ---- | 1 8
            self.dec_reg_pair("BC")
            cycles(8)
        elif opcode == 0x0C: # INC C       | Z0H- | 1 4
            self.inc_reg("C")
            cycles(4)
        elif opcode == 0x0D: # DEC C       | Z1H- | 1 4
            self.dec_reg("C")
            cycles(4)
        elif opcode == 0x0E: # LD C,d8     | ---- | 2 8
            self.c = self.read_byte()
            cycles(8)
        elif opcode == 0x0F: # RRCA        | 000C | 1 4
            carry = self.a & 0x01
            self.a = ((self.a >> 1) | (carry << 7)) & 0xFF
            self.set_flag(self.FLAG_C, carry)
            self.set_flag(self.FLAG_H, False)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_Z, False)
            cycles(4)
        elif opcode == 0x10: # STOP 0      | ---- | 2 4
            self.read_byte()
            self.stopped = True
            cycles(4)
        elif opcode == 0x11: # LD DE,d16   | ---- | 3 12
            self.set_reg_pair("DE", self.read_word())
            cycles(12)
        elif opcode == 0x12: # LD (DE),A   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("DE"), self.a)
            cycles(8)
        elif opcode == 0x13: # INC DE      | ---- | 1 8
            self.set_reg_pair("DE", (self.get_reg_pair("DE") + 1) & 0xFFFF)
            cycles(8)
        elif opcode == 0x14: # INC D       | Z0H- | 1 4
            self.inc_reg("D")
            cycles(4)
        elif opcode == 0x15: # DEC D       | Z1H- | 1 4
            self.dec_reg("D")
            cycles(4)
        elif opcode == 0x16: # LD D,d8     | ---- | 2 8
            self.d = self.read_byte()
            cycles(8)
        elif opcode == 0x17: # RLA         | 000C | 1 4
            old_carry = 1 if self.get_flag(self.FLAG_C) else 0
            new_carry = (self.a & 0x80) >> 7
            self.a = ((self.a << 1) & 0xFF) | old_carry
            self.set_flag(self.FLAG_C, new_carry)
            self.set_flag(self.FLAG_Z, False)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, False)
            cycles(4)
        elif opcode == 0x18: # JR r8       | ---- | 2 12
            offset = ctypes.c_int8(self.read_byte()).value
            self.pc = (self.pc + offset) & 0xFFFF
            cycles(12)
        elif opcode == 0x19: # ADD HL,DE   | -0HC | 1 8
            self.add_reg_pair("HL", self.get_reg_pair("DE"))
            cycles(8)
        elif opcode == 0x1A: # LD A,(DE)   | ---- | 1 8
            self.a = self.memory.read_byte(self.get_reg_pair("DE"))
            cycles(8)
        elif opcode == 0x1B: # DEC DE      | ---- | 1 8
            self.dec_reg_pair("DE")
            cycles(8)
        elif opcode == 0x1C: # INC E       | Z0H- | 1 4
            self.inc_reg("E")
            cycles(4)
        elif opcode == 0x1D: # DEC E       | Z1H- | 1 4
            self.dec_reg("E")
            cycles(4)
        elif opcode == 0x1E: # LD E,d8     | ---- | 2 8
            self.e = self.read_byte()
            cycles(8)
        elif opcode == 0x1F: # RRA         | 000C | 1 4
            old_carry = 1 if self.get_flag(self.FLAG_C) else 0
            new_carry = self.a & 0x01
            self.a = ((self.a >> 1) | (old_carry << 7)) & 0xFF
            self.set_flag(self.FLAG_C, new_carry)
            self.set_flag(self.FLAG_Z, False)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, False)
            cycles(4)
        elif opcode == 0x20: # JR NZ,r8    | ---- | 2 12/8
            offset = ctypes.c_int8(self.read_byte()).value
            self.pc = (self.pc + offset) & 0xFFFF if not self.get_flag(self.FLAG_Z) else self.pc
            cycles(12 if not self.get_flag(self.FLAG_Z) else 8)
        elif opcode == 0x21: # LD HL,d16   | ---- | 3 12
            self.set_reg_pair("HL", self.read_word())
            cycles(12)
        elif opcode == 0x22: # LD (HL+),A  | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.a)
            self.inc_reg_pair("HL")
            cycles(8)
        elif opcode == 0x23: # INC HL      | ---- | 1 8
            self.inc_reg_pair("HL")
            cycles(8)
        elif opcode == 0x24: # INC H       | Z0H- | 1 4
            self.inc_reg("H")
            cycles(4)
        elif opcode == 0x25: # DEC H       | Z1H- | 1 4
            self.dec_reg("H")
            cycles(4)
        elif opcode == 0x26: # LD H,d8     | ---- | 2 8
            self.h = self.read_byte()
            cycles(8)
        elif opcode == 0x27: # DAA         | Z-0C | 1 4
            a, n, h, c = self.a, self.get_flag(self.FLAG_N), self.get_flag(self.FLAG_H), self.get_flag(self.FLAG_C)
            fix, nc = 0, c
            if not n:
                if h or (a & 0xF) > 9: fix += 0x06
                if c or a > 0x99: fix += 0x60; nc = 1
                a = (a + fix) & 0xFF
            else:
                if h: fix += 0x06
                if c: fix += 0x60
                a = (a - fix) & 0xFF
            self.a = a
            self.set_flag(self.FLAG_Z, a == 0)
            self.set_flag(self.FLAG_H, False)
            self.set_flag(self.FLAG_C, nc)
            cycles(4)
        elif opcode == 0x28: # JR Z,r8     | ---- | 2 12/8
            offset = ctypes.c_int8(self.read_byte()).value
            self.pc = (self.pc + offset) & 0xFFFF if self.get_flag(self.FLAG_Z) else self.pc
            cycles(12 if self.get_flag(self.FLAG_Z) else 8)
        elif opcode == 0x29: # ADD HL,HL   | -0HC | 1 8
            self.add_reg_pair("HL", self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x2A: # LD A,(HL+)  | ---- | 1 8
            self.a = self.memory.read_byte(self.get_reg_pair("HL"))
            self.inc_reg_pair("HL")
            cycles(8)
        elif opcode == 0x2B: # DEC HL      | ---- | 1 8
            self.dec_reg_pair("HL")
            cycles(8)
        elif opcode == 0x2C: # INC L       | Z0H- | 1 4
            self.inc_reg("L")
            cycles(4)
        elif opcode == 0x2D: # DEC L       | Z1H- | 1 4
            self.dec_reg("L")
            cycles(4)
        elif opcode == 0x2E: # LD L,d8     | ---- | 2 8
            self.l = self.read_byte()
            cycles(8)
        elif opcode == 0x2F: # CPL         | -11- | 1 4
            self.a ^= 0xFF
            self.set_flag(self.FLAG_N, True)
            self.set_flag(self.FLAG_H, True)
            cycles(4)
        elif opcode == 0x30: # JR NC,r8    | ---- | 2 12/8
            offset = ctypes.c_int8(self.read_byte()).value
            if not self.get_flag(self.FLAG_C):
                self.pc = (self.pc + offset) & 0xFFFF
                cycles(12)
            else:
                cycles(8)
        elif opcode == 0x31: # LD SP,d16   | ---- | 3 12
            self.sp = self.read_word()
            cycles(12)
        elif opcode == 0x32: # LD (HL-),A  | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.a)
            self.dec_reg_pair("HL")
            cycles(8)
        elif opcode == 0x33: # INC SP      | ---- | 1 8
            self.sp = (self.sp + 1) & 0xFFFF
            cycles(8)
        elif opcode == 0x34: # INC (HL)    | Z0H- | 1 12
            value = (self.memory.read_byte(self.get_reg_pair('HL')) + 1) & 0xFF
            self.memory.write_byte(self.get_reg_pair('HL'), value)
            self.set_flag(self.FLAG_Z, value == 0)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, (value & 0x0F) == 0x00)
            cycles(12)
        elif opcode == 0x35: # DEC (HL)    | Z1H- | 1 12
            value = (self.memory.read_byte(self.get_reg_pair('HL')) - 1) & 0xFF
            self.memory.write_byte(self.get_reg_pair('HL'), value)
            self.set_flag(self.FLAG_Z, value == 0)
            self.set_flag(self.FLAG_N, True)
            self.set_flag(self.FLAG_H, (value & 0x0F) == 0x00)
            cycles(12)
        elif opcode == 0x36: # LD (HL),d8  | ---- | 2 12
            self.memory.write_byte(self.get_reg_pair("HL"), self.read_byte())
            cycles(12)
        elif opcode == 0x37: # SCF         | -001 | 1 4
            self.set_flag(self.FLAG_C, True)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, False)
            cycles(4)
        elif opcode == 0x38: # JR C,r8     | ---- | 2 12/8
            offset = ctypes.c_int8(self.read_byte()).value
            self.pc = (self.pc + offset) & 0xFFFF if self.get_flag(self.FLAG_C) else self.pc
            cycles(12 if self.get_flag(self.FLAG_C) else 8)
        elif opcode == 0x39: # ADD HL,SP   | -0HC | 1 8
            result = (self.get_reg_pair('HL') + self.sp) & 0xFFFF
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, ((self.get_reg_pair('HL') & 0xFFF) + (self.sp & 0xFFF)) > 0xFFF)
            self.set_flag(self.FLAG_C, self.get_reg_pair('HL') + self.sp > 0xFFFF)
            self.set_reg_pair('HL', result)
            cycles(8)
        elif opcode == 0x3A: # LD A,(HL-)  | ---- | 1 8
            self.a = self.memory.read_byte(self.get_reg_pair("HL"))
            self.dec_reg_pair("HL")
            cycles(8)
        elif opcode == 0x3B: # DEC SP      | ---- | 1 8
            self.sp = (self.sp - 1) & 0xFFFF
            cycles(8)
        elif opcode == 0x3C: # INC A       | Z0H- | 1 4
            self.inc_reg("A")
            cycles(4)
        elif opcode == 0x3D: # DEC A       | Z1H- | 1 4
            self.dec_reg("A")
            cycles(4)
        elif opcode == 0x3E: # LD A,d8     | ---- | 2 8
            self.a = self.read_byte()
            cycles(8)
        elif opcode == 0x3F: # CCF         | -00C | 1 4
            self.set_flag(self.FLAG_C, not self.get_flag(self.FLAG_C))
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, False)
            cycles(4)
        elif opcode == 0x40: # LD B,B      | ---- | 1 4
            self.b = b
            cycles(4)
        elif opcode == 0x41: # LD B,C      | ---- | 1 4
            self.b = self.c
            cycles(4)
        elif opcode == 0x42: # LD B,D      | ---- | 1 4
            self.b = self.d
            cycles(4)
        elif opcode == 0x43: # LD B,E      | ---- | 1 4
            self.b = self.e
            cycles(4)
        elif opcode == 0x44: # LD B,H      | ---- | 1 4
            self.b = self.h
            cycles(4)
        elif opcode == 0x45: # LD B,L      | ---- | 1 4
            self.b = self.l
            cycles(4)
        elif opcode == 0x46: # LD B,(HL)   | ---- | 1 8
            self.b = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x47: # LD B,A      | ---- | 1 4
            self.b = self.a
            cycles(4)
        elif opcode == 0x48: # LD C,B      | ---- | 1 4
            self.c = self.b
            cycles(4)
        elif opcode == 0x49: # LD C,C      | ---- | 1 4
            self.c = self.c
            cycles(4)
        elif opcode == 0x4A: # LD C,D      | ---- | 1 4
            self.c = self.d
            cycles(4)
        elif opcode == 0x4B: # LD C,E      | ---- | 1 4
            self.c = self.e
            cycles(4)
        elif opcode == 0x4C: # LD C,H      | ---- | 1 4
            self.c = self.h
            cycles(4)
        elif opcode == 0x4D: # LD C,L      | ---- | 1 4
            self.c = self.l
            cycles(4)
        elif opcode == 0x4E: # LD C,(HL)   | ---- | 1 8
            self.c = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x4F: # LD C,A      | ---- | 1 4
            self.c = self.a
            cycles(4)
        elif opcode == 0x50: # LD D,B      | ---- | 1 4
            self.d = self.b
            cycles(4)
        elif opcode == 0x51: # LD D,C      | ---- | 1 4
            self.d = self.c
            cycles(4)
        elif opcode == 0x52: # LD D,D      | ---- | 1 4
            self.d = self.d
            cycles(4)
        elif opcode == 0x53: # LD D,E      | ---- | 1 4
            self.d = self.e
            cycles(4)
        elif opcode == 0x54: # LD D,H      | ---- | 1 4
            self.d = self.h
            cycles(4)
        elif opcode == 0x55: # LD D,L      | ---- | 1 4
            self.d = self.h
            cycles(4)
        elif opcode == 0x56: # LD D,(HL)   | ---- | 1 8
            self.d = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x57: # LD D,A      | ---- | 1 4
            self.d = self.a
            cycles(4)
        elif opcode == 0x58: # LD E,B      | ---- | 1 4
            self.e = self.b
            cycles(4)
        elif opcode == 0x59: # LD E,C      | ---- | 1 4
            self.e = self.c
            cycles(4)
        elif opcode == 0x5A: # LD E,D      | ---- | 1 4
            self.e = self.d
            cycles(4)
        elif opcode == 0x5B: # LD E,E      | ---- | 1 4
            self.e = self.e
            cycles(4)
        elif opcode == 0x5C: # LD E,H      | ---- | 1 4
            self.e = self.h
            cycles(4)
        elif opcode == 0x5D: # LD E,L      | ---- | 1 4
            self.e = self.l
            cycles(4)
        elif opcode == 0x5E: # LD E,(HL)   | ---- | 1 8
            self.e = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x5F: # LD E,A      | ---- | 1 4
            self.e = self.a
            cycles(4)
        elif opcode == 0x60: # LD H,B      | ---- | 1 4
            self.h = self.b
            cycles(4)
        elif opcode == 0x61: # LD H,C      | ---- | 1 4
            self.h = self.c
            cycles(4)
        elif opcode == 0x62: # LD H,D      | ---- | 1 4
            self.h = self.d
            cycles(4)
        elif opcode == 0x63: # LD H,E      | ---- | 1 4
            self.h = self.e
            cycles(4)
        elif opcode == 0x64: # LD H,H      | ---- | 1 4
            self.h = self.h
            cycles(4)
        elif opcode == 0x65: # LD H,L      | ---- | 1 4
            self.h = self.l
            cycles(4)
        elif opcode == 0x66: # LD H,(HL)   | ---- | 1 8
            self.h = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x67: # LD H,A      | ---- | 1 4
            self.h = self.a
            cycles(4)
        elif opcode == 0x68: # LD L,B      | ---- | 1 4
            self.l = self.b
            cycles(4)
        elif opcode == 0x69: # LD L,C      | ---- | 1 4
            self.l = self.c
            cycles(4)
        elif opcode == 0x6A: # LD L,D      | ---- | 1 4
            self.l = self.d
            cycles(4)
        elif opcode == 0x6B: # LD L,E      | ---- | 1 4
            self.l = self.e
            cycles(4)
        elif opcode == 0x6C: # LD L,H      | ---- | 1 4
            self.l = self.h
            cycles(4)
        elif opcode == 0x6D: # LD L,L      | ---- | 1 4
            self.l = self.l
            cycles(4)
        elif opcode == 0x6E: # LD L,(HL)   | ---- | 1 8
            self.l = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x6F: # LD L,A      | ---- | 1 4
            self.l = self.a
            cycles(4)
        elif opcode == 0x70: # LD (HL),B   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.b)
            cycles(8)
        elif opcode == 0x71: # LD (HL),C   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.c)
            cycles(8)
        elif opcode == 0x72: # LD (HL),D   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.d)
            cycles(8)
        elif opcode == 0x73: # LD (HL),E   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.e)
            cycles(8)
        elif opcode == 0x74: # LD (HL),H   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.h)
            cycles(8)
        elif opcode == 0x75: # LD (HL),L   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.l)
            cycles(8)
        elif opcode == 0x76: # HALT        | ---- | 1 4
            self.halted = True
            cycles(4)
        elif opcode == 0x77: # LD (HL),A   | ---- | 1 8
            self.memory.write_byte(self.get_reg_pair("HL"), self.a)
            cycles(8)
        elif opcode == 0x78: # LD A,B      | ---- | 1 4
            self.a = self.b
            cycles(4)
        elif opcode == 0x79: # LD A,C      | ---- | 1 4
            self.a = self.c
            cycles(4)
        elif opcode == 0x7A: # LD A,D      | ---- | 1 4
            self.a = self.d
            cycles(4)
        elif opcode == 0x7B: # LD A,E      | ---- | 1 4
            self.a = self.e
            cycles(4)
        elif opcode == 0x7C: # LD A,H      | ---- | 1 4
            self.a = self.h
            cycles(4)
        elif opcode == 0x7D: # LD A,L      | ---- | 1 4
            self.a = self.l
            cycles(4)
        elif opcode == 0x7E: # LD A,(HL)   | ---- | 1 8
            self.a = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(8)
        elif opcode == 0x7F: # LD A,A      | ---- | 1 4
            self.a = self.a
            cycles(4)
        elif opcode == 0x80: # ADD A,B     | Z0HC | 1 4
            self.add_reg("A", self.b)
            cycles(4)
        elif opcode == 0x81: # ADD A,C     | Z0HC | 1 4
            self.add_reg("A", self.c)
            cycles(4)
        elif opcode == 0x82: # ADD A,D     | Z0HC | 1 4
            self.add_reg("A", self.d)
            cycles(4)
        elif opcode == 0x83: # ADD A,E     | Z0HC | 1 4
            self.add_reg("A", self.e)
            cycles(4)
        elif opcode == 0x84: # ADD A,H     | Z0HC | 1 4
            self.add_reg("A", self.h)
            cycles(4)
        elif opcode == 0x85: # ADD A,L     | Z0HC | 1 4
            self.add_reg("A", self.l)
            cycles(4)
        elif opcode == 0x86: # ADD A,(HL)  | Z0HC | 1 8
            self.add_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0x87: # ADD A,A     | Z0HC | 1 4
            self.add_reg("A", self.a)
            cycles(4)
        elif opcode == 0x88: # ADC A,B     | Z0HC | 1 4
            self.adc_reg("A", self.b)
            cycles(4)
        elif opcode == 0x89: # ADC A,C     | Z0HC | 1 4
            self.adc_reg("A", self.c)
            cycles(4)
        elif opcode == 0x8A: # ADC A,D     | Z0HC | 1 4
            self.adc_reg("A", self.d)
            cycles(4)
        elif opcode == 0x8B: # ADC A,E     | Z0HC | 1 4
            self.adc_reg("A", self.e)
            cycles(4)
        elif opcode == 0x8C: # ADC A,H     | Z0HC | 1 4
            self.adc_reg("A", self.h)
            cycles(4)
        elif opcode == 0x8D: # ADC A,L     | Z0HC | 1 4
            self.adc_reg("A", self.l)
            cycles(4)
        elif opcode == 0x8E: # ADC A,(HL)  | Z0HC | 1 8
            self.adc_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0x8F: # ADC A,A     | Z0HC | 1 4
            self.adc_reg("A", self.a)
            cycles(4)
        elif opcode == 0x90: # SUB B       | Z1HC | 1 4
            self.sub_reg("A", self.b)
            cycles(4)
        elif opcode == 0x91: # SUB C       | Z1HC | 1 4
            self.sub_reg("A", self.c)
            cycles(4)
        elif opcode == 0x92: # SUB D       | Z1HC | 1 4
            self.sub_reg("A", self.d)
            cycles(4)
        elif opcode == 0x93: # SUB E       | Z1HC | 1 4
            self.sub_reg("A", self.e)
            cycles(4)
        elif opcode == 0x94: # SUB H       | Z1HC | 1 4
            self.sub_reg("A", self.h)
            cycles(4)
        elif opcode == 0x95: # SUB L       | Z1HC | 1 4
            self.sub_reg("A", self.l)
            cycles(4)
        elif opcode == 0x96: # SUB (HL)    | Z1HC | 1 8
            self.sub_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0x97: # SUB A       | Z1HC | 1 4
            self.sub_reg("A", self.a)
            cycles(4)
        elif opcode == 0x98: # SBC A,B     | Z1HC | 1 4
            self.sbc_reg("A", self.b)
            cycles(4)
        elif opcode == 0x99: # SBC A,C     | Z1HC | 1 4
            self.sbc_reg("A", self.c)
            cycles(4)
        elif opcode == 0x9A: # SBC A,D     | Z1HC | 1 4
            self.sbc_reg("A", self.d)
            cycles(4)
        elif opcode == 0x9B: # SBC A,E     | Z1HC | 1 4
            self.sbc_reg("A", self.e)
            cycles(4)
        elif opcode == 0x9C: # SBC A,H     | Z1HC | 1 4
            self.sbc_reg("A", self.h)
            cycles(4)
        elif opcode == 0x9D: # SBC A,L     | Z1HC | 1 4
            self.sbc_reg("A", self.l)
            cycles(4)
        elif opcode == 0x9E: # SBC A,(HL)  | Z1HC | 1 8
            self.sbc_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0x9F: # SBC A,A     | Z1HC | 1 4
            self.sbc_reg("A", self.a)
            cycles(4)
        elif opcode == 0xA0: # AND B       | Z010 | 1 4
            self.and_reg("A", self.b)
            cycles(4)
        elif opcode == 0xA1: # AND C       | Z010 | 1 4
            self.and_reg("A", self.c)
            cycles(4)
        elif opcode == 0xA2: # AND D       | Z010 | 1 4
            self.and_reg("A", self.d)
            cycles(4)
        elif opcode == 0xA3: # AND E       | Z010 | 1 4
            self.and_reg("A", self.e)
            cycles(4)
        elif opcode == 0xA4: # AND H       | Z010 | 1 4
            self.and_reg("A", self.h)
            cycles(4)
        elif opcode == 0xA5: # AND L       | Z010 | 1 4
            self.and_reg("A", self.l)
            cycles(4)
        elif opcode == 0xA6: # AND (HL)    | Z010 | 1 8
            self.and_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0xA7: # AND A       | Z010 | 1 4
            self.and_reg("A", self.a)
            cycles(4)
        elif opcode == 0xA8: # XOR B       | Z000 | 1 4
            self.xor_reg("A", self.b)
            cycles(4)
        elif opcode == 0xA9: # XOR C       | Z000 | 1 4
            self.xor_reg("A", self.c)
            cycles(4)
        elif opcode == 0xAA: # XOR D       | Z000 | 1 4
            self.xor_reg("A", self.d)
            cycles(4)
        elif opcode == 0xAB: # XOR E       | Z000 | 1 4
            self.xor_reg("A", self.e)
            cycles(4)
        elif opcode == 0xAC: # XOR H       | Z000 | 1 4
            self.xor_reg("A", self.h)
            cycles(4)
        elif opcode == 0xAD: # XOR L       | Z000 | 1 4
            self.xor_reg("A", self.l)
            cycles(4)
        elif opcode == 0xAE: # XOR (HL)    | Z000 | 1 8
            self.xor_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0xAF: # XOR A       | Z000 | 1 4
            self.xor_reg("A", self.a)
            cycles(4)
        elif opcode == 0xB0: # OR B        | Z000 | 1 4
            self.or_reg("A", self.b)
            cycles(4)
        elif opcode == 0xB1: # OR C        | Z000 | 1 4
            self.or_reg("A", self.c)
            cycles(4)
        elif opcode == 0xB2: # OR D        | Z000 | 1 4
            self.or_reg("A", self.d)
            cycles(4)
        elif opcode == 0xB3: # OR E        | Z000 | 1 4
            self.or_reg("A", self.e)
            cycles(4)
        elif opcode == 0xB4: # OR H        | Z000 | 1 4
            self.or_reg("A", self.h)
            cycles(4)
        elif opcode == 0xB5: # OR L        | Z000 | 1 4
            self.or_reg("A", self.l)
            cycles(4)
        elif opcode == 0xB6: # OR (HL)     | Z000 | 1 8
            self.or_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0xB7: # OR A        | Z000 | 1 4
            self.or_reg("A", self.a)
            cycles(4)
        elif opcode == 0xB8: # CP B        | Z1HC | 1 4
            self.cp_reg("A", self.b)
            cycles(4)
        elif opcode == 0xB9: # CP C        | Z1HC | 1 4
            self.cp_reg("A", self.c)
            cycles(4)
        elif opcode == 0xBA: # CP D        | Z1HC | 1 4
            self.cp_reg("A", self.d)
            cycles(4)
        elif opcode == 0xBB: # CP E        | Z1HC | 1 4
            self.cp_reg("A", self.e)
            cycles(4)
        elif opcode == 0xBC: # CP H        | Z1HC | 1 4
            self.cp_reg("A", self.h)
            cycles(4)
        elif opcode == 0xBD: # CP L        | Z1HC | 1 4
            self.cp_reg("A", self.l)
            cycles(4)
        elif opcode == 0xBE: # CP (HL)     | Z1HC | 1 8
            self.cp_reg("A", self.memory.read_byte(self.get_reg_pair("HL")))
            cycles(8)
        elif opcode == 0xBF: # CP A        | Z1HC | 1 4
            self.cp_reg("A", self.a)
            cycles(4)
        elif opcode == 0xC0: # RET NZ      | ---- | 1 20/8
            if not self.get_flag(self.FLAG_Z):
                self.pc = self.pop()
                cycles(20)
            else:
                cycles(8)
        elif opcode == 0xC1: # POP BC      | ---- | 1 12
            self.set_reg_pair("BC", self.pop())
            cycles(12)
        elif opcode == 0xC2: # JP NZ,a16   | ---- | 3 16/12
            address = self.read_word()
            if not self.get_flag(self.FLAG_Z):
                self.pc = address
                cycles(16)
            else:
                cycles(12)
        elif opcode == 0xC3: # JP a16      | ---- | 3 16
            self.pc = self.read_word()
            cycles(16)
        elif opcode == 0xC4: # CALL NZ,a16 | ---- | 3 24/12
            address = self.read_word()
            if not self.get_flag(self.FLAG_Z):
                self.push(self.pc)
                self.pc = address
                cycles(24)
            else:
                cycles(12)
        elif opcode == 0xC5: # PUSH BC     | ---- | 1 16
            self.push(self.get_reg_pair("BC"))
            cycles(16)
        elif opcode == 0xC6: # ADD A,d8    | Z0HC | 2 8
            self.add_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xC7: # RST 00H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x00
            cycles(16)
        elif opcode == 0xC8: # RET Z       | ---- | 1 20/8
            if self.get_flag(self.FLAG_Z):
                self.pc = self.pop()
                cycles(20)
            else:
                cycles(8)
        elif opcode == 0xC9: # RET         | ---- | 1 16
            self.pc = self.pop()
            cycles(16)
        elif opcode == 0xCA: # JP Z,a16    | ---- | 3 16/12
            address = self.read_word()     # Читает всегда!
            if self.get_flag(self.FLAG_Z):
                self.pc = address
                cycles(16)
            else:
                cycles(12)
        elif opcode == 0xCB: # PREFIX CB   | ---- | 1 4
            prefix = self.read_byte()
            print(f"prefix cb: {prefix:02X}")
            cycles(self.execute_prefix(prefix) + 4)
        elif opcode == 0xCC: # CALL Z,a16  | ---- | 3 24/12
            address = self.read_word()
            if self.get_flag(self.FLAG_Z):
                self.push(self.pc)
                self.pc = address
                cycles(24)
            else:
                cycles(12)
        elif opcode == 0xCD: # CALL a16    | ---- | 3 24
            self.push(self.pc + 2) # +++++++ 3333333 !!!1! +++ 222222 +++++ pc+1 ==== ++++++3 3333
            self.pc = self.read_word()
            cycles(24)
        elif opcode == 0xCE: # ADC A,d8    | Z0HC | 2 8
            self.adc_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xCF: # RST 08H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x08
            cycles(16)
        elif opcode == 0xD0: # RET NC      | ---- | 1 20/8
            if not self.get_flag(self.FLAG_C):
                self.pc = self.pop()
                cycles(20)
            else:
                cycles(8)
        elif opcode == 0xD1: # POP DE      | ---- | 1 12
            self.set_reg_pair("DE", self.pop())
            cycles(12)
        elif opcode == 0xD2: # JP NC,a16   | ---- | 3 16/12
            address = self.read_word()
            if not self.get_flag(self.FLAG_C):
                self.pc = address
                cycles(16)
            else:
                cycles(12)
        elif opcode == 0xD4: # CALL NC,a16 | ---- | 3 24/12
            address = self.read_word()
            if not self.get_flag(self.FLAG_C):
                self.push(self.pc)
                self.pc = address
                cycles(24)
            else:
                cycles(12)
        elif opcode == 0xD5: # PUSH DE     | ---- | 1 16
            self.push(self.get_reg_pair("DE"))
            cycles(16)
        elif opcode == 0xD6: # SUB d8      | Z1HC | 2 8
            self.sub_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xD7: # RST 10H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x10
            cycles(16)
        elif opcode == 0xD8: # RET C       | ---- | 1 20/8
            if self.get_flag(self.FLAG_C):
                self.pc = self.pop()
                cycles(20)
            else:
                cycles(8)
        elif opcode == 0xD9: # RETI        | ---- | 1 16
            self.pc = self.pop()
            self.interrupts_enabled = True
            cycles(16)
        elif opcode == 0xDA: # JP C,a16    | ---- | 3 16/12
            if self.get_flag(self.FLAG_C):
                self.pc = self.read_word()
                cycles(16)
            else:
                cycles(12)
        elif opcode == 0xDC: # CALL C,a16  | ---- | 3 24/12
            if self.get_flag(self.FLAG_C):
                self.push(self.pc)
                self.pc = self.read_word()
                cycles(24)
            else:
                cycles(12)
        elif opcode == 0xDE: # SBC A,d8    | Z1HC | 2 8
            self.sbc_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xDF: # RST 18H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x18
            cycles(16)
        elif opcode == 0xE0: # LDH (a8),A  | ---- | 2 12
            a8 = self.read_byte()
            address = 0xFF00 + a8
            self.memory.write_byte(address, self.a)
            cycles(12)
        elif opcode == 0xE1: # POP HL      | ---- | 1 12
            self.set_reg_pair("HL", self.pop())
            cycles(12)
        elif opcode == 0xE2: # LD (C),A    | ---- | 2 8
            self.memory.write_byte(0xFF00 + self.c, self.a)
            cycles(8)
        elif opcode == 0xE5: # PUSH HL     | ---- | 1 16
            self.push(self.get_reg_pair("HL"))
            cycles(16)
        elif opcode == 0xE6: # AND d8      | Z010 | 2 8
            self.and_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xE7: # RST 20H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x20
            cycles(16)
        elif opcode == 0xE8: # ADD SP,r8   | 00HC | 2 16
            temp = ctypes.c_int8(self.read_byte()).value
            result = (self.sp + temp) & 0xFFFF
            self.set_flag(self.FLAG_Z, False)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, ((self.sp & 0xF) + (temp & 0xF)) > 0xF)
            self.set_flag(self.FLAG_C, ((self.sp & 0xFF) + (temp & 0xFF)) > 0xFF)
            self.sp = result
            cycles(16)
        elif opcode == 0xE9: # JP (HL)     | ---- | 1 4
            self.pc = self.memory.read_byte(self.get_reg_pair("HL"))
            cycles(4)
        elif opcode == 0xEA: # LD (a16),A  | ---- | 3 16
            self.memory.write_byte(self.read_word(), self.a)
            cycles(16)
        elif opcode == 0xEE: # XOR d8      | Z000 | 2 8
            self.xor_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xEF: # RST 28H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x28
            cycles(16)
        elif opcode == 0xF0: # LDH A,(a8)  | ---- | 2 12
            self.a = self.memory.read_byte(0xFF00 + self.read_byte())
            cycles(12)
        elif opcode == 0xF1: # POP AF      | ZNHC | 1 12
            self.set_reg_pair("AF", self.pop())
            cycles(12)
        elif opcode == 0xF2: # LD A,(C)    | ---- | 2 8
            self.a = self.memory.read_byte(0xFF00 + self.c)
            cycles(8)
        elif opcode == 0xF3: # DI          | ---- | 1 4
            self.interrupts_enabled = False
            cycles(4)
        elif opcode == 0xF5: # PUSH AF     | ---- | 1 16
            self.push(self.get_reg_pair("AF"))
            cycles(16)
        elif opcode == 0xF6: # OR d8       | Z000 | 2 8
            self.or_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xF7: # RST 30H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x30
            cycles(16)
        elif opcode == 0xF8: # LD HL,SP+r8 | 00HC | 2 12
            offset = ctypes.c_int8(self.read_byte()).value
            result = (self.sp + offset) & 0xFFFF
            self.set_reg_pair("HL", result)
            self.set_flag(self.FLAG_Z, False)
            self.set_flag(self.FLAG_N, False)
            self.set_flag(self.FLAG_H, ((self.sp & 0xF) + (offset & 0xF)) > 0xF)
            self.set_flag(self.FLAG_C, ((self.sp & 0xFF) + (offset & 0xFF)) > 0xFF)
            cycles(12)
        elif opcode == 0xF9: # LD SP,HL    | ---- | 1 8
            self.sp = self.get_reg_pair("HL")
            cycles(8)
        elif opcode == 0xFA: # LD A,(a16)  | ---- | 3 16
            self.a = self.memory.read_byte(self.read_word())
            cycles(16)
        elif opcode == 0xFB: # EI          | ---- | 1 4
            self.interrupts_enabled = True
            cycles(4)
        elif opcode == 0xFE: # CP d8       | Z1HC | 2 8
            self.cp_reg("A", self.read_byte())
            cycles(8)
        elif opcode == 0xFF: # RST 38H     | ---- | 1 16
            self.push(self.pc)
            self.pc = 0x38
            cycles(16)
        else:
            IndexError(f"Unknown opcode: 0x{opcode:02X}")

    def execute_prefix(self, prefix) -> int:
        self.prefix = prefix

        def cycles(cycles: int) -> None:
            return cycles

        # mnemonic # flags # bytes cycles

        if prefix == 0x00: # RLC B       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x01: # RLC C       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x02: # RLC D       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x03: # RLC E       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x04: # RLC H       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x05: # RLC L       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x06: # RLC (HL)    | Z00C | 2 16
            cycles(16)
        elif prefix == 0x07: # RLC A       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x08: # RRC B       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x09: # RRC C       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x0A: # RRC D       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x0B: # RRC E       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x0C: # RRC H       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x0D: # RRC L       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x0E: # RRC (HL)    | Z00C | 2 16
            cycles(16)
        elif prefix == 0x0F: # RRC A       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x10: # RL B        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x11: # RL C        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x12: # RL D        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x13: # RL E        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x14: # RL H        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x15: # RL L        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x16: # RL (HL)     | Z00C | 2 16
            cycles(16)
        elif prefix == 0x17: # RL A        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x18: # RR B        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x19: # RR C        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x1A: # RR D        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x1B: # RR E        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x1C: # RR H        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x1D: # RR L        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x1E: # RR (HL)     | Z00C | 2 16
            cycles(16)
        elif prefix == 0x1F: # RR A        | Z00C | 2 8
            cycles(8)
        elif prefix == 0x20: # SLA B       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x21: # SLA C       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x22: # SLA D       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x23: # SLA E       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x24: # SLA H       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x25: # SLA L       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x26: # SLA (HL)    | Z00C | 2 16
            cycles(16)
        elif prefix == 0x27: # SLA A       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x28: # SRA B       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x29: # SRA C       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x2A: # SRA D       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x2B: # SRA E       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x2C: # SRA H       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x2D: # SRA L       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x2E: # SRA (HL)    | Z000 | 2 16
            cycles(16)
        elif prefix == 0x2F: # SRA A       | Z000 | 2 8
            cycles(8)
        elif prefix == 0x30: # SWAP B      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x31: # SWAP C      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x32: # SWAP D      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x33: # SWAP E      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x34: # SWAP H      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x35: # SWAP L      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x36: # SWAP (HL)   | Z000 | 2 16
            cycles(16)
        elif prefix == 0x37: # SWAP A      | Z000 | 2 8
            cycles(8)
        elif prefix == 0x38: # SRL B       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x39: # SRL C       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x3A: # SRL D       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x3B: # SRL E       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x3C: # SRL H       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x3D: # SRL L       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x3E: # SRL (HL)    | Z00C | 2 16
            cycles(16)
        elif prefix == 0x3F: # SRL A       | Z00C | 2 8
            cycles(8)
        elif prefix == 0x40: # BIT 0,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x41: # BIT 0,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x42: # BIT 0,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x43: # BIT 0,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x44: # BIT 0,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x45: # BIT 0,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x46: # BIT 0,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x47: # BIT 0,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x48: # BIT 1,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x49: # BIT 1,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x4A: # BIT 1,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x4B: # BIT 1,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x4C: # BIT 1,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x4D: # BIT 1,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x4E: # BIT 1,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x4F: # BIT 1,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x50: # BIT 2,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x51: # BIT 2,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x52: # BIT 2,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x53: # BIT 2,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x54: # BIT 2,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x55: # BIT 2,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x56: # BIT 2,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x57: # BIT 2,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x58: # BIT 3,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x59: # BIT 3,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x5A: # BIT 3,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x5B: # BIT 3,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x5C: # BIT 3,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x5D: # BIT 3,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x5E: # BIT 3,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x5F: # BIT 3,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x60: # BIT 4,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x61: # BIT 4,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x62: # BIT 4,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x63: # BIT 4,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x64: # BIT 4,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x65: # BIT 4,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x66: # BIT 4,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x67: # BIT 4,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x68: # BIT 5,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x69: # BIT 5,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x6A: # BIT 5,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x6B: # BIT 5,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x6C: # BIT 5,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x6D: # BIT 5,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x6E: # BIT 5,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x6F: # BIT 5,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x70: # BIT 6,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x71: # BIT 6,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x72: # BIT 6,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x73: # BIT 6,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x74: # BIT 6,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x75: # BIT 6,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x76: # BIT 6,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x77: # BIT 6,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x78: # BIT 7,B     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x79: # BIT 7,C     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x7A: # BIT 7,D     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x7B: # BIT 7,E     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x7C: # BIT 7,H     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x7D: # BIT 7,L     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x7E: # BIT 7,(HL)  | Z01- | 2 16
            cycles(16)
        elif prefix == 0x7F: # BIT 7,A     | Z01- | 2 8
            cycles(8)
        elif prefix == 0x80: # RES 0,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0x81: # RES 0,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0x82: # RES 0,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0x83: # RES 0,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0x84: # RES 0,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0x85: # RES 0,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0x86: # RES 0,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0x87: # RES 0,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0x88: # RES 1,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0x89: # RES 1,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0x8A: # RES 1,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0x8B: # RES 1,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0x8C: # RES 1,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0x8D: # RES 1,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0x8E: # RES 1,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0x8F: # RES 1,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0x90: # RES 2,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0x91: # RES 2,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0x92: # RES 2,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0x93: # RES 2,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0x94: # RES 2,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0x95: # RES 2,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0x96: # RES 2,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0x97: # RES 2,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0x98: # RES 3,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0x99: # RES 3,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0x9A: # RES 3,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0x9B: # RES 3,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0x9C: # RES 3,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0x9D: # RES 3,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0x9E: # RES 3,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0x9F: # RES 3,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA0: # RES 4,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA1: # RES 4,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA2: # RES 4,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA3: # RES 4,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA4: # RES 4,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA5: # RES 4,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA6: # RES 4,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xA7: # RES 4,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA8: # RES 5,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xA9: # RES 5,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xAA: # RES 5,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xAB: # RES 5,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xAC: # RES 5,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xAD: # RES 5,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xAE: # RES 5,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xAF: # RES 5,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB0: # RES 6,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB1: # RES 6,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB2: # RES 6,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB3: # RES 6,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB4: # RES 6,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB5: # RES 6,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB6: # RES 6,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xB7: # RES 6,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB8: # RES 7,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xB9: # RES 7,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xBA: # RES 7,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xBB: # RES 7,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xBC: # RES 7,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xBD: # RES 7,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xBE: # RES 7,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xBF: # RES 7,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC0: # SET 0,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC1: # SET 0,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC2: # SET 0,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC3: # SET 0,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC4: # SET 0,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC5: # SET 0,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC6: # SET 0,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xC7: # SET 0,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC8: # SET 1,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xC9: # SET 1,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xCA: # SET 1,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xCB: # SET 1,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xCC: # SET 1,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xCD: # SET 1,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xCE: # SET 1,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xCF: # SET 1,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD0: # SET 2,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD1: # SET 2,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD2: # SET 2,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD4: # SET 2,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD5: # SET 2,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD6: # SET 2,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD7: # SET 2,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xD8: # SET 2,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xD9: # SET 3,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xDA: # SET 3,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xDC: # SET 3,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xDE: # SET 3,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xDF: # SET 3,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE0: # SET 3,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE1: # SET 3,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xE2: # SET 3,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE5: # SET 4,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE6: # SET 4,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE7: # SET 4,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE8: # SET 4,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xE9: # SET 4,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xEA: # SET 4,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xEE: # SET 4,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xEF: # SET 4,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF0: # SET 5,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF1: # SET 5,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF2: # SET 5,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF3: # SET 5,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF5: # SET 5,H     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF6: # SET 5,L     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF7: # SET 5,(HL)  | ---- | 2 16
            cycles(16)
        elif prefix == 0xF8: # SET 5,A     | ---- | 2 8
            cycles(8)
        elif prefix == 0xF9: # SET 6,B     | ---- | 2 8
            cycles(8)
        elif prefix == 0xFA: # SET 6,C     | ---- | 2 8
            cycles(8)
        elif prefix == 0xFB: # SET 6,D     | ---- | 2 8
            cycles(8)
        elif prefix == 0xFE: # SET 6,E     | ---- | 2 8
            cycles(8)
        elif prefix == 0xFF: # SET 6,H     | ---- | 2 8
            cycles(8)
        else:
            IndexError(f"Unknown prefix: 1x{prefix:02X}")

