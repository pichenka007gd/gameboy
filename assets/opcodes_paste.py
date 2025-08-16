if opcode == 0x00: # NOP         | ---- | 1 4
    cycles(4)
if opcode == 0x01: # LD BC,d16   | ---- | 3 12
    cycles(12)
if opcode == 0x02: # LD (BC),A   | ---- | 1 8
    cycles(8)
if opcode == 0x03: # INC BC      | ---- | 1 8
    cycles(8)
if opcode == 0x04: # INC B       | Z0H- | 1 4
    cycles(4)
if opcode == 0x05: # DEC B       | Z1H- | 1 4
    cycles(4)
if opcode == 0x06: # LD B,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x07: # RLCA        | 000C | 1 4
    cycles(4)
if opcode == 0x08: # LD (a16),SP | ---- | 3 20
    cycles(20)
if opcode == 0x09: # ADD HL,BC   | -0HC | 1 8
    cycles(8)
if opcode == 0x0A: # LD A,(BC)   | ---- | 1 8
    cycles(8)
if opcode == 0x0B: # DEC BC      | ---- | 1 8
    cycles(8)
if opcode == 0x0C: # INC C       | Z0H- | 1 4
    cycles(4)
if opcode == 0x0D: # DEC C       | Z1H- | 1 4
    cycles(4)
if opcode == 0x0E: # LD C,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x0F: # RRCA        | 000C | 1 4
    cycles(4)
if opcode == 0x10: # STOP 0      | ---- | 2 4
    cycles(4)
if opcode == 0x11: # LD DE,d16   | ---- | 3 12
    cycles(12)
if opcode == 0x12: # LD (DE),A   | ---- | 1 8
    cycles(8)
if opcode == 0x13: # INC DE      | ---- | 1 8
    cycles(8)
if opcode == 0x14: # INC D       | Z0H- | 1 4
    cycles(4)
if opcode == 0x15: # DEC D       | Z1H- | 1 4
    cycles(4)
if opcode == 0x16: # LD D,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x17: # RLA         | 000C | 1 4
    cycles(4)
if opcode == 0x18: # JR r8       | ---- | 2 12
    cycles(12)
if opcode == 0x19: # ADD HL,DE   | -0HC | 1 8
    cycles(8)
if opcode == 0x1A: # LD A,(DE)   | ---- | 1 8
    cycles(8)
if opcode == 0x1B: # DEC DE      | ---- | 1 8
    cycles(8)
if opcode == 0x1C: # INC E       | Z0H- | 1 4
    cycles(4)
if opcode == 0x1D: # DEC E       | Z1H- | 1 4
    cycles(4)
if opcode == 0x1E: # LD E,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x1F: # RRA         | 000C | 1 4
    cycles(4)
if opcode == 0x20: # JR NZ,r8    | ---- | 2 12/8
    cycles(8)
if opcode == 0x21: # LD HL,d16   | ---- | 3 12
    cycles(12)
if opcode == 0x22: # LD (HL+),A  | ---- | 1 8
    cycles(8)
if opcode == 0x23: # INC HL      | ---- | 1 8
    cycles(8)
if opcode == 0x24: # INC H       | Z0H- | 1 4
    cycles(4)
if opcode == 0x25: # DEC H       | Z1H- | 1 4
    cycles(4)
if opcode == 0x26: # LD H,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x27: # DAA         | Z-0C | 1 4
    cycles(4)
if opcode == 0x28: # JR Z,r8     | ---- | 2 12/8
    cycles(8)
if opcode == 0x29: # ADD HL,HL   | -0HC | 1 8
    cycles(8)
if opcode == 0x2A: # LD A,(HL+)  | ---- | 1 8
    cycles(8)
if opcode == 0x2B: # DEC HL      | ---- | 1 8
    cycles(8)
if opcode == 0x2C: # INC L       | Z0H- | 1 4
    cycles(4)
if opcode == 0x2D: # DEC L       | Z1H- | 1 4
    cycles(4)
if opcode == 0x2E: # LD L,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x2F: # CPL         | -11- | 1 4
    cycles(4)
if opcode == 0x30: # JR NC,r8    | ---- | 2 12/8
    cycles(8)
if opcode == 0x31: # LD SP,d16   | ---- | 3 12
    cycles(12)
if opcode == 0x32: # LD (HL-),A  | ---- | 1 8
    cycles(8)
if opcode == 0x33: # INC SP      | ---- | 1 8
    cycles(8)
if opcode == 0x34: # INC (HL)    | Z0H- | 1 12
    cycles(12)
if opcode == 0x35: # DEC (HL)    | Z1H- | 1 12
    cycles(12)
if opcode == 0x36: # LD (HL),d8  | ---- | 2 12
    cycles(12)
if opcode == 0x37: # SCF         | -001 | 1 4
    cycles(4)
if opcode == 0x38: # JR C,r8     | ---- | 2 12/8
    cycles(8)
if opcode == 0x39: # ADD HL,SP   | -0HC | 1 8
    cycles(8)
if opcode == 0x3A: # LD A,(HL-)  | ---- | 1 8
    cycles(8)
if opcode == 0x3B: # DEC SP      | ---- | 1 8
    cycles(8)
if opcode == 0x3C: # INC A       | Z0H- | 1 4
    cycles(4)
if opcode == 0x3D: # DEC A       | Z1H- | 1 4
    cycles(4)
if opcode == 0x3E: # LD A,d8     | ---- | 2 8
    cycles(8)
if opcode == 0x3F: # CCF         | -00C | 1 4
    cycles(4)
if opcode == 0x40: # LD B,B      | ---- | 1 4
    cycles(4)
if opcode == 0x41: # LD B,C      | ---- | 1 4
    cycles(4)
if opcode == 0x42: # LD B,D      | ---- | 1 4
    cycles(4)
if opcode == 0x43: # LD B,E      | ---- | 1 4
    cycles(4)
if opcode == 0x44: # LD B,H      | ---- | 1 4
    cycles(4)
if opcode == 0x45: # LD B,L      | ---- | 1 4
    cycles(4)
if opcode == 0x46: # LD B,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x47: # LD B,A      | ---- | 1 4
    cycles(4)
if opcode == 0x48: # LD C,B      | ---- | 1 4
    cycles(4)
if opcode == 0x49: # LD C,C      | ---- | 1 4
    cycles(4)
if opcode == 0x4A: # LD C,D      | ---- | 1 4
    cycles(4)
if opcode == 0x4B: # LD C,E      | ---- | 1 4
    cycles(4)
if opcode == 0x4C: # LD C,H      | ---- | 1 4
    cycles(4)
if opcode == 0x4D: # LD C,L      | ---- | 1 4
    cycles(4)
if opcode == 0x4E: # LD C,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x4F: # LD C,A      | ---- | 1 4
    cycles(4)
if opcode == 0x50: # LD D,B      | ---- | 1 4
    cycles(4)
if opcode == 0x51: # LD D,C      | ---- | 1 4
    cycles(4)
if opcode == 0x52: # LD D,D      | ---- | 1 4
    cycles(4)
if opcode == 0x53: # LD D,E      | ---- | 1 4
    cycles(4)
if opcode == 0x54: # LD D,H      | ---- | 1 4
    cycles(4)
if opcode == 0x55: # LD D,L      | ---- | 1 4
    cycles(4)
if opcode == 0x56: # LD D,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x57: # LD D,A      | ---- | 1 4
    cycles(4)
if opcode == 0x58: # LD E,B      | ---- | 1 4
    cycles(4)
if opcode == 0x59: # LD E,C      | ---- | 1 4
    cycles(4)
if opcode == 0x5A: # LD E,D      | ---- | 1 4
    cycles(4)
if opcode == 0x5B: # LD E,E      | ---- | 1 4
    cycles(4)
if opcode == 0x5C: # LD E,H      | ---- | 1 4
    cycles(4)
if opcode == 0x5D: # LD E,L      | ---- | 1 4
    cycles(4)
if opcode == 0x5E: # LD E,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x5F: # LD E,A      | ---- | 1 4
    cycles(4)
if opcode == 0x60: # LD H,B      | ---- | 1 4
    cycles(4)
if opcode == 0x61: # LD H,C      | ---- | 1 4
    cycles(4)
if opcode == 0x62: # LD H,D      | ---- | 1 4
    cycles(4)
if opcode == 0x63: # LD H,E      | ---- | 1 4
    cycles(4)
if opcode == 0x64: # LD H,H      | ---- | 1 4
    cycles(4)
if opcode == 0x65: # LD H,L      | ---- | 1 4
    cycles(4)
if opcode == 0x66: # LD H,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x67: # LD H,A      | ---- | 1 4
    cycles(4)
if opcode == 0x68: # LD L,B      | ---- | 1 4
    cycles(4)
if opcode == 0x69: # LD L,C      | ---- | 1 4
    cycles(4)
if opcode == 0x6A: # LD L,D      | ---- | 1 4
    cycles(4)
if opcode == 0x6B: # LD L,E      | ---- | 1 4
    cycles(4)
if opcode == 0x6C: # LD L,H      | ---- | 1 4
    cycles(4)
if opcode == 0x6D: # LD L,L      | ---- | 1 4
    cycles(4)
if opcode == 0x6E: # LD L,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x6F: # LD L,A      | ---- | 1 4
    cycles(4)
if opcode == 0x70: # LD (HL),B   | ---- | 1 8
    cycles(8)
if opcode == 0x71: # LD (HL),C   | ---- | 1 8
    cycles(8)
if opcode == 0x72: # LD (HL),D   | ---- | 1 8
    cycles(8)
if opcode == 0x73: # LD (HL),E   | ---- | 1 8
    cycles(8)
if opcode == 0x74: # LD (HL),H   | ---- | 1 8
    cycles(8)
if opcode == 0x75: # LD (HL),L   | ---- | 1 8
    cycles(8)
if opcode == 0x76: # HALT        | ---- | 1 4
    cycles(4)
if opcode == 0x77: # LD (HL),A   | ---- | 1 8
    cycles(8)
if opcode == 0x78: # LD A,B      | ---- | 1 4
    cycles(4)
if opcode == 0x79: # LD A,C      | ---- | 1 4
    cycles(4)
if opcode == 0x7A: # LD A,D      | ---- | 1 4
    cycles(4)
if opcode == 0x7B: # LD A,E      | ---- | 1 4
    cycles(4)
if opcode == 0x7C: # LD A,H      | ---- | 1 4
    cycles(4)
if opcode == 0x7D: # LD A,L      | ---- | 1 4
    cycles(4)
if opcode == 0x7E: # LD A,(HL)   | ---- | 1 8
    cycles(8)
if opcode == 0x7F: # LD A,A      | ---- | 1 4
    cycles(4)
if opcode == 0x80: # ADD A,B     | Z0HC | 1 4
    cycles(4)
if opcode == 0x81: # ADD A,C     | Z0HC | 1 4
    cycles(4)
if opcode == 0x82: # ADD A,D     | Z0HC | 1 4
    cycles(4)
if opcode == 0x83: # ADD A,E     | Z0HC | 1 4
    cycles(4)
if opcode == 0x84: # ADD A,H     | Z0HC | 1 4
    cycles(4)
if opcode == 0x85: # ADD A,L     | Z0HC | 1 4
    cycles(4)
if opcode == 0x86: # ADD A,(HL)  | Z0HC | 1 8
    cycles(8)
if opcode == 0x87: # ADD A,A     | Z0HC | 1 4
    cycles(4)
if opcode == 0x88: # ADC A,B     | Z0HC | 1 4
    cycles(4)
if opcode == 0x89: # ADC A,C     | Z0HC | 1 4
    cycles(4)
if opcode == 0x8A: # ADC A,D     | Z0HC | 1 4
    cycles(4)
if opcode == 0x8B: # ADC A,E     | Z0HC | 1 4
    cycles(4)
if opcode == 0x8C: # ADC A,H     | Z0HC | 1 4
    cycles(4)
if opcode == 0x8D: # ADC A,L     | Z0HC | 1 4
    cycles(4)
if opcode == 0x8E: # ADC A,(HL)  | Z0HC | 1 8
    cycles(8)
if opcode == 0x8F: # ADC A,A     | Z0HC | 1 4
    cycles(4)
if opcode == 0x90: # SUB B       | Z1HC | 1 4
    cycles(4)
if opcode == 0x91: # SUB C       | Z1HC | 1 4
    cycles(4)
if opcode == 0x92: # SUB D       | Z1HC | 1 4
    cycles(4)
if opcode == 0x93: # SUB E       | Z1HC | 1 4
    cycles(4)
if opcode == 0x94: # SUB H       | Z1HC | 1 4
    cycles(4)
if opcode == 0x95: # SUB L       | Z1HC | 1 4
    cycles(4)
if opcode == 0x96: # SUB (HL)    | Z1HC | 1 8
    cycles(8)
if opcode == 0x97: # SUB A       | Z1HC | 1 4
    cycles(4)
if opcode == 0x98: # SBC A,B     | Z1HC | 1 4
    cycles(4)
if opcode == 0x99: # SBC A,C     | Z1HC | 1 4
    cycles(4)
if opcode == 0x9A: # SBC A,D     | Z1HC | 1 4
    cycles(4)
if opcode == 0x9B: # SBC A,E     | Z1HC | 1 4
    cycles(4)
if opcode == 0x9C: # SBC A,H     | Z1HC | 1 4
    cycles(4)
if opcode == 0x9D: # SBC A,L     | Z1HC | 1 4
    cycles(4)
if opcode == 0x9E: # SBC A,(HL)  | Z1HC | 1 8
    cycles(8)
if opcode == 0x9F: # SBC A,A     | Z1HC | 1 4
    cycles(4)
if opcode == 0xA0: # AND B       | Z010 | 1 4
    cycles(4)
if opcode == 0xA1: # AND C       | Z010 | 1 4
    cycles(4)
if opcode == 0xA2: # AND D       | Z010 | 1 4
    cycles(4)
if opcode == 0xA3: # AND E       | Z010 | 1 4
    cycles(4)
if opcode == 0xA4: # AND H       | Z010 | 1 4
    cycles(4)
if opcode == 0xA5: # AND L       | Z010 | 1 4
    cycles(4)
if opcode == 0xA6: # AND (HL)    | Z010 | 1 8
    cycles(8)
if opcode == 0xA7: # AND A       | Z010 | 1 4
    cycles(4)
if opcode == 0xA8: # XOR B       | Z000 | 1 4
    cycles(4)
if opcode == 0xA9: # XOR C       | Z000 | 1 4
    cycles(4)
if opcode == 0xAA: # XOR D       | Z000 | 1 4
    cycles(4)
if opcode == 0xAB: # XOR E       | Z000 | 1 4
    cycles(4)
if opcode == 0xAC: # XOR H       | Z000 | 1 4
    cycles(4)
if opcode == 0xAD: # XOR L       | Z000 | 1 4
    cycles(4)
if opcode == 0xAE: # XOR (HL)    | Z000 | 1 8
    cycles(8)
if opcode == 0xAF: # XOR A       | Z000 | 1 4
    cycles(4)
if opcode == 0xB0: # OR B        | Z000 | 1 4
    cycles(4)
if opcode == 0xB1: # OR C        | Z000 | 1 4
    cycles(4)
if opcode == 0xB2: # OR D        | Z000 | 1 4
    cycles(4)
if opcode == 0xB3: # OR E        | Z000 | 1 4
    cycles(4)
if opcode == 0xB4: # OR H        | Z000 | 1 4
    cycles(4)
if opcode == 0xB5: # OR L        | Z000 | 1 4
    cycles(4)
if opcode == 0xB6: # OR (HL)     | Z000 | 1 8
    cycles(8)
if opcode == 0xB7: # OR A        | Z000 | 1 4
    cycles(4)
if opcode == 0xB8: # CP B        | Z1HC | 1 4
    cycles(4)
if opcode == 0xB9: # CP C        | Z1HC | 1 4
    cycles(4)
if opcode == 0xBA: # CP D        | Z1HC | 1 4
    cycles(4)
if opcode == 0xBB: # CP E        | Z1HC | 1 4
    cycles(4)
if opcode == 0xBC: # CP H        | Z1HC | 1 4
    cycles(4)
if opcode == 0xBD: # CP L        | Z1HC | 1 4
    cycles(4)
if opcode == 0xBE: # CP (HL)     | Z1HC | 1 8
    cycles(8)
if opcode == 0xBF: # CP A        | Z1HC | 1 4
    cycles(4)
if opcode == 0xC0: # RET NZ      | ---- | 1 20/8
    cycles(8)
if opcode == 0xC1: # POP BC      | ---- | 1 12
    cycles(12)
if opcode == 0xC2: # JP NZ,a16   | ---- | 3 16/12
    cycles(12)
if opcode == 0xC3: # JP a16      | ---- | 3 16
    cycles(16)
if opcode == 0xC4: # CALL NZ,a16 | ---- | 3 24/12
    cycles(12)
if opcode == 0xC5: # PUSH BC     | ---- | 1 16
    cycles(16)
if opcode == 0xC6: # ADD A,d8    | Z0HC | 2 8
    cycles(8)
if opcode == 0xC7: # RST 00H     | ---- | 1 16
    cycles(16)
if opcode == 0xC8: # RET Z       | ---- | 1 20/8
    cycles(8)
if opcode == 0xC9: # RET         | ---- | 1 16
    cycles(16)
if opcode == 0xCA: # JP Z,a16    | ---- | 3 16/12
    cycles(12)
if opcode == 0xCB: # PREFIX CB   | ---- | 1 4
    cycles(4)
if opcode == 0xCC: # CALL Z,a16  | ---- | 3 24/12
    cycles(12)
if opcode == 0xCD: # CALL a16    | ---- | 3 24
    cycles(24)
if opcode == 0xCE: # ADC A,d8    | Z0HC | 2 8
    cycles(8)
if opcode == 0xCF: # RST 08H     | ---- | 1 16
    cycles(16)
if opcode == 0xD0: # RET NC      | ---- | 1 20/8
    cycles(8)
if opcode == 0xD1: # POP DE      | ---- | 1 12
    cycles(12)
if opcode == 0xD2: # JP NC,a16   | ---- | 3 16/12
    cycles(12)
if opcode == 0xD4: #  CALL NC,a16 | ---- | 3 24/12
    cycles(12)
if opcode == 0xD5: # PUSH DE     | ---- | 1 16
    cycles(16)
if opcode == 0xD6: # SUB d8      | Z1HC | 2 8
    cycles(8)
if opcode == 0xD7: # RST 10H     | ---- | 1 16
    cycles(16)
if opcode == 0xD8: # RET C       | ---- | 1 20/8
    cycles(8)
if opcode == 0xD9: # RETI        | ---- | 1 16
    cycles(16)
if opcode == 0xDA: # JP C,a16    | ---- | 3 16/12
    cycles(12)
if opcode == 0xDC: #  CALL C,a16 | ---- | 3 24/12
    cycles(12)
if opcode == 0xDE: #  SBC A,d8   | Z1HC | 2 8
    cycles(8)
if opcode == 0xDF: # RST 18H     | ---- | 1 16
    cycles(16)
if opcode == 0xE0: # LDH (a8),A  | ---- | 2 12
    cycles(12)
if opcode == 0xE1: # POP HL      | ---- | 1 12
    cycles(12)
if opcode == 0xE2: # LD (C),A    | ---- | 2 8
    cycles(8)
if opcode == 0xE5: #   PUSH HL   | ---- | 1 16
    cycles(16)
if opcode == 0xE6: # AND d8      | Z010 | 2 8
    cycles(8)
if opcode == 0xE7: # RST 20H     | ---- | 1 16
    cycles(16)
if opcode == 0xE8: # ADD SP,r8   | 00HC | 2 16
    cycles(16)
if opcode == 0xE9: # JP (HL)     | ---- | 1 4
    cycles(4)
if opcode == 0xEA: # LD (a16),A  | ---- | 3 16
    cycles(16)
if opcode == 0xEE: #    XOR d8   | Z000 | 2 8
    cycles(8)
if opcode == 0xEF: # RST 28H     | ---- | 1 16
    cycles(16)
if opcode == 0xF0: # LDH A,(a8)  | ---- | 2 12
    cycles(12)
if opcode == 0xF1: # POP AF      | ZNHC | 1 12
    cycles(12)
if opcode == 0xF2: # LD A,(C)    | ---- | 2 8
    cycles(8)
if opcode == 0xF3: # DI          | ---- | 1 4
    cycles(4)
if opcode == 0xF5: #  PUSH AF    | ---- | 1 16
    cycles(16)
if opcode == 0xF6: # OR d8       | Z000 | 2 8
    cycles(8)
if opcode == 0xF7: # RST 30H     | ---- | 1 16
    cycles(16)
if opcode == 0xF8: # LD HL,SP+r8 | 00HC | 2 12
    cycles(12)
if opcode == 0xF9: # LD SP,HL    | ---- | 1 8
    cycles(8)
if opcode == 0xFA: # LD A,(a16)  | ---- | 3 16
    cycles(16)
if opcode == 0xFB: # EI          | ---- | 1 4
    cycles(4)
if opcode == 0xFE: #   CP d8     | Z1HC | 2 8
    cycles(8)
if opcode == 0xFF: # RST 38H     | --- | 1 16
    cycles(16)
