if prefix == 0x00: # RLC B       | Z00C | 2 8
    self.rlc_prefix("B")
    cycles(8)
if prefix == 0x01: # RLC C       | Z00C | 2 8
    self.rlc_prefix("C")
    cycles(8)
if prefix == 0x02: # RLC D       | Z00C | 2 8
    self.rlc_prefix("D")
    cycles(8)
if prefix == 0x03: # RLC E       | Z00C | 2 8
    self.rlc_prefix("E")
    cycles(8)
if prefix == 0x04: # RLC H       | Z00C | 2 8
    self.rlc_prefix("H")
    cycles(8)
if prefix == 0x05: # RLC L       | Z00C | 2 8
    self.rlc_prefix("L")
    cycles(8)
if prefix == 0x06: # RLC (HL)    | Z00C | 2 16
    self.rlc_prefix("(HL)")
    cycles(16)
if prefix == 0x07: # RLC A       | Z00C | 2 8
    self.rlc_prefix("A")
    cycles(8)
if prefix == 0x08: # RRC B       | Z00C | 2 8
    self.rrc_prefix("B")
    cycles(8)
if prefix == 0x09: # RRC C       | Z00C | 2 8
    self.rrc_prefix("C")
    cycles(8)
if prefix == 0x0A: # RRC D       | Z00C | 2 8
    self.rrc_prefix("D")
    cycles(8)
if prefix == 0x0B: # RRC E       | Z00C | 2 8
    self.rrc_prefix("E")
    cycles(8)
if prefix == 0x0C: # RRC H       | Z00C | 2 8
    self.rrc_prefix("H")
    cycles(8)
if prefix == 0x0D: # RRC L       | Z00C | 2 8
    self.rrc_prefix("L")
    cycles(8)
if prefix == 0x0E: # RRC (HL)    | Z00C | 2 16
    self.rrc_prefix("(HL)")
    cycles(16)
if prefix == 0x0F: # RRC A       | Z00C | 2 8
    self.rrc_prefix("A")
    cycles(8)
if prefix == 0x10: # RL B        | Z00C | 2 8
    self.rl_prefix("B")
    cycles(8)
if prefix == 0x11: # RL C        | Z00C | 2 8
    self.rl_prefix("C")
    cycles(8)
if prefix == 0x12: # RL D        | Z00C | 2 8
    self.rl_prefix("D")
    cycles(8)
if prefix == 0x13: # RL E        | Z00C | 2 8
    self.rl_prefix("E")
    cycles(8)
if prefix == 0x14: # RL H        | Z00C | 2 8
    self.rl_prefix("H")
    cycles(8)
if prefix == 0x15: # RL L        | Z00C | 2 8
    self.rl_prefix("L")
    cycles(8)
if prefix == 0x16: # RL (HL)     | Z00C | 2 16
    self.rl_prefix("(HL)")
    cycles(16)
if prefix == 0x17: # RL A        | Z00C | 2 8
    self.rl_prefix("A")
    cycles(8)
if prefix == 0x18: # RR B        | Z00C | 2 8
    self.rr_prefix("B")
    cycles(8)
if prefix == 0x19: # RR C        | Z00C | 2 8
    self.rr_prefix("C")
    cycles(8)
if prefix == 0x1A: # RR D        | Z00C | 2 8
    self.rr_prefix("D")
    cycles(8)
if prefix == 0x1B: # RR E        | Z00C | 2 8
    self.rr_prefix("E")
    cycles(8)
if prefix == 0x1C: # RR H        | Z00C | 2 8
    self.rr_prefix("H")
    cycles(8)
if prefix == 0x1D: # RR L        | Z00C | 2 8
    self.rr_prefix("L")
    cycles(8)
if prefix == 0x1E: # RR (HL)     | Z00C | 2 16
    self.rr_prefix("(HL)")
    cycles(16)
if prefix == 0x1F: # RR A        | Z00C | 2 8
    self.rr_prefix("A")
    cycles(8)
if prefix == 0x20: # SLA B       | Z00C | 2 8
    self.sla_prefix("B")
    cycles(8)
if prefix == 0x21: # SLA C       | Z00C | 2 8
    self.sla_prefix("C")
    cycles(8)
if prefix == 0x22: # SLA D       | Z00C | 2 8
    self.sla_prefix("D")
    cycles(8)
if prefix == 0x23: # SLA E       | Z00C | 2 8
    self.sla_prefix("E")
    cycles(8)
if prefix == 0x24: # SLA H       | Z00C | 2 8
    self.sla_prefix("H")
    cycles(8)
if prefix == 0x25: # SLA L       | Z00C | 2 8
    self.sla_prefix("L")
    cycles(8)
if prefix == 0x26: # SLA (HL)    | Z00C | 2 16
    self.sla_prefix("(HL)")
    cycles(16)
if prefix == 0x27: # SLA A       | Z00C | 2 8
    self.sla_prefix("A")
    cycles(8)
if prefix == 0x28: # SRA B       | Z000 | 2 8
    self.sra_prefix("B")
    cycles(8)
if prefix == 0x29: # SRA C       | Z000 | 2 8
    self.sra_prefix("C")
    cycles(8)
if prefix == 0x2A: # SRA D       | Z000 | 2 8
    self.sra_prefix("D")
    cycles(8)
if prefix == 0x2B: # SRA E       | Z000 | 2 8
    self.sra_prefix("E")
    cycles(8)
if prefix == 0x2C: # SRA H       | Z000 | 2 8
    self.sra_prefix("H")
    cycles(8)
if prefix == 0x2D: # SRA L       | Z000 | 2 8
    self.sra_prefix("L")
    cycles(8)
if prefix == 0x2E: # SRA (HL)    | Z000 | 2 16
    self.sra_prefix("(HL)")
    cycles(16)
if prefix == 0x2F: # SRA A       | Z000 | 2 8
    self.sra_prefix("A")
    cycles(8)
if prefix == 0x30: # SWAP B      | Z000 | 2 8
    self.swap_prefix("B")
    cycles(8)
if prefix == 0x31: # SWAP C      | Z000 | 2 8
    self.swap_prefix("C")
    cycles(8)
if prefix == 0x32: # SWAP D      | Z000 | 2 8
    self.swap_prefix("D")
    cycles(8)
if prefix == 0x33: # SWAP E      | Z000 | 2 8
    self.swap_prefix("E")
    cycles(8)
if prefix == 0x34: # SWAP H      | Z000 | 2 8
    self.swap_prefix("H")
    cycles(8)
if prefix == 0x35: # SWAP L      | Z000 | 2 8
    self.swap_prefix("L")
    cycles(8)
if prefix == 0x36: # SWAP (HL)   | Z000 | 2 16
    self.swap_prefix("(HL)")
    cycles(16)
if prefix == 0x37: # SWAP A      | Z000 | 2 8
    self.swap_prefix("A")
    cycles(8)
if prefix == 0x38: # SRL B       | Z00C | 2 8
    self.srl_prefix("B")
    cycles(8)
if prefix == 0x39: # SRL C       | Z00C | 2 8
    self.srl_prefix("C")
    cycles(8)
if prefix == 0x3A: # SRL D       | Z00C | 2 8
    self.srl_prefix("D")
    cycles(8)
if prefix == 0x3B: # SRL E       | Z00C | 2 8
    self.srl_prefix("E")
    cycles(8)
if prefix == 0x3C: # SRL H       | Z00C | 2 8
    self.srl_prefix("H")
    cycles(8)
if prefix == 0x3D: # SRL L       | Z00C | 2 8
    self.srl_prefix("L")
    cycles(8)
if prefix == 0x3E: # SRL (HL)    | Z00C | 2 16
    self.srl_prefix("(HL)")
    cycles(16)
if prefix == 0x3F: # SRL A       | Z00C | 2 8
    self.srl_prefix("A")
    cycles(8)
if prefix == 0x40: # BIT 0,B     | Z01- | 2 8
    self.bit_prefix("B", 0)
    cycles(8)
if prefix == 0x41: # BIT 0,C     | Z01- | 2 8
    self.bit_prefix("C", 0)
    cycles(8)
if prefix == 0x42: # BIT 0,D     | Z01- | 2 8
    self.bit_prefix("D", 0)
    cycles(8)
if prefix == 0x43: # BIT 0,E     | Z01- | 2 8
    self.bit_prefix("E", 0)
    cycles(8)
if prefix == 0x44: # BIT 0,H     | Z01- | 2 8
    self.bit_prefix("H", 0)
    cycles(8)
if prefix == 0x45: # BIT 0,L     | Z01- | 2 8
    self.bit_prefix("L", 0)
    cycles(8)
if prefix == 0x46: # BIT 0,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 0)
    cycles(16)
if prefix == 0x47: # BIT 0,A     | Z01- | 2 8
    self.bit_prefix("A", 0)
    cycles(8)
if prefix == 0x48: # BIT 1,B     | Z01- | 2 8
    self.bit_prefix("B", 1)
    cycles(8)
if prefix == 0x49: # BIT 1,C     | Z01- | 2 8
    self.bit_prefix("C", 1)
    cycles(8)
if prefix == 0x4A: # BIT 1,D     | Z01- | 2 8
    self.bit_prefix("D", 1)
    cycles(8)
if prefix == 0x4B: # BIT 1,E     | Z01- | 2 8
    self.bit_prefix("E", 1)
    cycles(8)
if prefix == 0x4C: # BIT 1,H     | Z01- | 2 8
    self.bit_prefix("H", 1)
    cycles(8)
if prefix == 0x4D: # BIT 1,L     | Z01- | 2 8
    self.bit_prefix("L", 1)
    cycles(8)
if prefix == 0x4E: # BIT 1,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 1)
    cycles(16)
if prefix == 0x4F: # BIT 1,A     | Z01- | 2 8
    self.bit_prefix("A", 1)
    cycles(8)
if prefix == 0x50: # BIT 2,B     | Z01- | 2 8
    self.bit_prefix("B", 2)
    cycles(8)
if prefix == 0x51: # BIT 2,C     | Z01- | 2 8
    self.bit_prefix("C", 2)
    cycles(8)
if prefix == 0x52: # BIT 2,D     | Z01- | 2 8
    self.bit_prefix("D", 2)
    cycles(8)
if prefix == 0x53: # BIT 2,E     | Z01- | 2 8
    self.bit_prefix("E", 2)
    cycles(8)
if prefix == 0x54: # BIT 2,H     | Z01- | 2 8
    self.bit_prefix("H", 2)
    cycles(8)
if prefix == 0x55: # BIT 2,L     | Z01- | 2 8
    self.bit_prefix("L", 2)
    cycles(8)
if prefix == 0x56: # BIT 2,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 2)
    cycles(16)
if prefix == 0x57: # BIT 2,A     | Z01- | 2 8
    self.bit_prefix("A", 2)
    cycles(8)
if prefix == 0x58: # BIT 3,B     | Z01- | 2 8
    self.bit_prefix("B", 3)
    cycles(8)
if prefix == 0x59: # BIT 3,C     | Z01- | 2 8
    self.bit_prefix("C", 3)
    cycles(8)
if prefix == 0x5A: # BIT 3,D     | Z01- | 2 8
    self.bit_prefix("D", 3)
    cycles(8)
if prefix == 0x5B: # BIT 3,E     | Z01- | 2 8
    self.bit_prefix("E", 3)
    cycles(8)
if prefix == 0x5C: # BIT 3,H     | Z01- | 2 8
    self.bit_prefix("H", 3)
    cycles(8)
if prefix == 0x5D: # BIT 3,L     | Z01- | 2 8
    self.bit_prefix("L", 3)
    cycles(8)
if prefix == 0x5E: # BIT 3,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 3)
    cycles(16)
if prefix == 0x5F: # BIT 3,A     | Z01- | 2 8
    self.bit_prefix("A", 3)
    cycles(8)
if prefix == 0x60: # BIT 4,B     | Z01- | 2 8
    self.bit_prefix("B", 4)
    cycles(8)
if prefix == 0x61: # BIT 4,C     | Z01- | 2 8
    self.bit_prefix("C", 4)
    cycles(8)
if prefix == 0x62: # BIT 4,D     | Z01- | 2 8
    self.bit_prefix("D", 4)
    cycles(8)
if prefix == 0x63: # BIT 4,E     | Z01- | 2 8
    self.bit_prefix("E", 4)
    cycles(8)
if prefix == 0x64: # BIT 4,H     | Z01- | 2 8
    self.bit_prefix("H", 4)
    cycles(8)
if prefix == 0x65: # BIT 4,L     | Z01- | 2 8
    self.bit_prefix("L", 4)
    cycles(8)
if prefix == 0x66: # BIT 4,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 4)
    cycles(16)
if prefix == 0x67: # BIT 4,A     | Z01- | 2 8
    self.bit_prefix("A", 4)
    cycles(8)
if prefix == 0x68: # BIT 5,B     | Z01- | 2 8
    self.bit_prefix("B", 5)
    cycles(8)
if prefix == 0x69: # BIT 5,C     | Z01- | 2 8
    self.bit_prefix("C", 5)
    cycles(8)
if prefix == 0x6A: # BIT 5,D     | Z01- | 2 8
    self.bit_prefix("D", 5)
    cycles(8)
if prefix == 0x6B: # BIT 5,E     | Z01- | 2 8
    self.bit_prefix("E", 5)
    cycles(8)
if prefix == 0x6C: # BIT 5,H     | Z01- | 2 8
    self.bit_prefix("H", 5)
    cycles(8)
if prefix == 0x6D: # BIT 5,L     | Z01- | 2 8
    self.bit_prefix("L", 5)
    cycles(8)
if prefix == 0x6E: # BIT 5,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 5)
    cycles(16)
if prefix == 0x6F: # BIT 5,A     | Z01- | 2 8
    self.bit_prefix("A", 5)
    cycles(8)
if prefix == 0x70: # BIT 6,B     | Z01- | 2 8
    self.bit_prefix("B", 6)
    cycles(8)
if prefix == 0x71: # BIT 6,C     | Z01- | 2 8
    self.bit_prefix("C", 6)
    cycles(8)
if prefix == 0x72: # BIT 6,D     | Z01- | 2 8
    self.bit_prefix("D", 6)
    cycles(8)
if prefix == 0x73: # BIT 6,E     | Z01- | 2 8
    self.bit_prefix("E", 6)
    cycles(8)
if prefix == 0x74: # BIT 6,H     | Z01- | 2 8
    self.bit_prefix("H", 6)
    cycles(8)
if prefix == 0x75: # BIT 6,L     | Z01- | 2 8
    self.bit_prefix("L", 6)
    cycles(8)
if prefix == 0x76: # BIT 6,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 6)
    cycles(16)
if prefix == 0x77: # BIT 6,A     | Z01- | 2 8
    self.bit_prefix("A", 6)
    cycles(8)
if prefix == 0x78: # BIT 7,B     | Z01- | 2 8
    self.bit_prefix("B", 7)
    cycles(8)
if prefix == 0x79: # BIT 7,C     | Z01- | 2 8
    self.bit_prefix("C", 7)
    cycles(8)
if prefix == 0x7A: # BIT 7,D     | Z01- | 2 8
    self.bit_prefix("D", 7)
    cycles(8)
if prefix == 0x7B: # BIT 7,E     | Z01- | 2 8
    self.bit_prefix("E", 7)
    cycles(8)
if prefix == 0x7C: # BIT 7,H     | Z01- | 2 8
    self.bit_prefix("H", 7)
    cycles(8)
if prefix == 0x7D: # BIT 7,L     | Z01- | 2 8
    self.bit_prefix("L", 7)
    cycles(8)
if prefix == 0x7E: # BIT 7,(HL)  | Z01- | 2 16
    self.bit_prefix("(HL)", 7)
    cycles(16)
if prefix == 0x7F: # BIT 7,A     | Z01- | 2 8
    self.bit_prefix("A", 7)
    cycles(8)
if prefix == 0x80: # RES 0,B     | ---- | 2 8
    self.res_prefix("B", 0)
    cycles(8)
if prefix == 0x81: # RES 0,C     | ---- | 2 8
    self.res_prefix("C", 0)
    cycles(8)
if prefix == 0x82: # RES 0,D     | ---- | 2 8
    self.res_prefix("D", 0)
    cycles(8)
if prefix == 0x83: # RES 0,E     | ---- | 2 8
    self.res_prefix("E", 0)
    cycles(8)
if prefix == 0x84: # RES 0,H     | ---- | 2 8
    self.res_prefix("H", 0)
    cycles(8)
if prefix == 0x85: # RES 0,L     | ---- | 2 8
    self.res_prefix("L", 0)
    cycles(8)
if prefix == 0x86: # RES 0,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 0)
    cycles(16)
if prefix == 0x87: # RES 0,A     | ---- | 2 8
    self.res_prefix("A", 0)
    cycles(8)
if prefix == 0x88: # RES 1,B     | ---- | 2 8
    self.res_prefix("B", 1)
    cycles(8)
if prefix == 0x89: # RES 1,C     | ---- | 2 8
    self.res_prefix("C", 1)
    cycles(8)
if prefix == 0x8A: # RES 1,D     | ---- | 2 8
    self.res_prefix("D", 1)
    cycles(8)
if prefix == 0x8B: # RES 1,E     | ---- | 2 8
    self.res_prefix("E", 1)
    cycles(8)
if prefix == 0x8C: # RES 1,H     | ---- | 2 8
    self.res_prefix("H", 1)
    cycles(8)
if prefix == 0x8D: # RES 1,L     | ---- | 2 8
    self.res_prefix("L", 1)
    cycles(8)
if prefix == 0x8E: # RES 1,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 1)
    cycles(16)
if prefix == 0x8F: # RES 1,A     | ---- | 2 8
    self.res_prefix("A", 1)
    cycles(8)
if prefix == 0x90: # RES 2,B     | ---- | 2 8
    self.res_prefix("B", 2)
    cycles(8)
if prefix == 0x91: # RES 2,C     | ---- | 2 8
    self.res_prefix("C", 2)
    cycles(8)
if prefix == 0x92: # RES 2,D     | ---- | 2 8
    self.res_prefix("D", 2)
    cycles(8)
if prefix == 0x93: # RES 2,E     | ---- | 2 8
    self.res_prefix("E", 2)
    cycles(8)
if prefix == 0x94: # RES 2,H     | ---- | 2 8
    self.res_prefix("H", 2)
    cycles(8)
if prefix == 0x95: # RES 2,L     | ---- | 2 8
    self.res_prefix("L", 2)
    cycles(8)
if prefix == 0x96: # RES 2,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 2)
    cycles(16)
if prefix == 0x97: # RES 2,A     | ---- | 2 8
    self.res_prefix("A", 2)
    cycles(8)
if prefix == 0x98: # RES 3,B     | ---- | 2 8
    self.res_prefix("B", 3)
    cycles(8)
if prefix == 0x99: # RES 3,C     | ---- | 2 8
    self.res_prefix("C", 3)
    cycles(8)
if prefix == 0x9A: # RES 3,D     | ---- | 2 8
    self.res_prefix("D", 3)
    cycles(8)
if prefix == 0x9B: # RES 3,E     | ---- | 2 8
    self.res_prefix("E", 3)
    cycles(8)
if prefix == 0x9C: # RES 3,H     | ---- | 2 8
    self.res_prefix("H", 3)
    cycles(8)
if prefix == 0x9D: # RES 3,L     | ---- | 2 8
    self.res_prefix("L", 3)
    cycles(8)
if prefix == 0x9E: # RES 3,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 3)
    cycles(16)
if prefix == 0x9F: # RES 3,A     | ---- | 2 8
    self.res_prefix("A", 3)
    cycles(8)
if prefix == 0xA0: # RES 4,B     | ---- | 2 8
    self.res_prefix("B", 4)
    cycles(8)
if prefix == 0xA1: # RES 4,C     | ---- | 2 8
    self.res_prefix("C", 4)
    cycles(8)
if prefix == 0xA2: # RES 4,D     | ---- | 2 8
    self.res_prefix("D", 4)
    cycles(8)
if prefix == 0xA3: # RES 4,E     | ---- | 2 8
    self.res_prefix("E", 4)
    cycles(8)
if prefix == 0xA4: # RES 4,H     | ---- | 2 8
    self.res_prefix("H", 4)
    cycles(8)
if prefix == 0xA5: # RES 4,L     | ---- | 2 8
    self.res_prefix("L", 4)
    cycles(8)
if prefix == 0xA6: # RES 4,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 4)
    cycles(16)
if prefix == 0xA7: # RES 4,A     | ---- | 2 8
    self.res_prefix("A", 4)
    cycles(8)
if prefix == 0xA8: # RES 5,B     | ---- | 2 8
    self.res_prefix("B", 5)
    cycles(8)
if prefix == 0xA9: # RES 5,C     | ---- | 2 8
    self.res_prefix("C", 5)
    cycles(8)
if prefix == 0xAA: # RES 5,D     | ---- | 2 8
    self.res_prefix("D", 5)
    cycles(8)
if prefix == 0xAB: # RES 5,E     | ---- | 2 8
    self.res_prefix("E", 5)
    cycles(8)
if prefix == 0xAC: # RES 5,H     | ---- | 2 8
    self.res_prefix("H", 5)
    cycles(8)
if prefix == 0xAD: # RES 5,L     | ---- | 2 8
    self.res_prefix("L", 5)
    cycles(8)
if prefix == 0xAE: # RES 5,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 5)
    cycles(16)
if prefix == 0xAF: # RES 5,A     | ---- | 2 8
    self.res_prefix("A", 5)
    cycles(8)
if prefix == 0xB0: # RES 6,B     | ---- | 2 8
    self.res_prefix("B", 6)
    cycles(8)
if prefix == 0xB1: # RES 6,C     | ---- | 2 8
    self.res_prefix("C", 6)
    cycles(8)
if prefix == 0xB2: # RES 6,D     | ---- | 2 8
    self.res_prefix("D", 6)
    cycles(8)
if prefix == 0xB3: # RES 6,E     | ---- | 2 8
    self.res_prefix("E", 6)
    cycles(8)
if prefix == 0xB4: # RES 6,H     | ---- | 2 8
    self.res_prefix("H", 6)
    cycles(8)
if prefix == 0xB5: # RES 6,L     | ---- | 2 8
    self.res_prefix("L", 6)
    cycles(8)
if prefix == 0xB6: # RES 6,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 6)
    cycles(16)
if prefix == 0xB7: # RES 6,A     | ---- | 2 8
    self.res_prefix("A", 6)
    cycles(8)
if prefix == 0xB8: # RES 7,B     | ---- | 2 8
    self.res_prefix("B", 7)
    cycles(8)
if prefix == 0xB9: # RES 7,C     | ---- | 2 8
    self.res_prefix("C", 7)
    cycles(8)
if prefix == 0xBA: # RES 7,D     | ---- | 2 8
    self.res_prefix("D", 7)
    cycles(8)
if prefix == 0xBB: # RES 7,E     | ---- | 2 8
    self.res_prefix("E", 7)
    cycles(8)
if prefix == 0xBC: # RES 7,H     | ---- | 2 8
    self.res_prefix("H", 7)
    cycles(8)
if prefix == 0xBD: # RES 7,L     | ---- | 2 8
    self.res_prefix("L", 7)
    cycles(8)
if prefix == 0xBE: # RES 7,(HL)  | ---- | 2 16
    self.res_prefix("(HL)", 7)
    cycles(16)
if prefix == 0xBF: # RES 7,A     | ---- | 2 8
    self.res_prefix("A", 7)
    cycles(8)
if prefix == 0xC0: # SET 0,B     | ---- | 2 8
    self.set_prefix("B", 0)
    cycles(8)
if prefix == 0xC1: # SET 0,C     | ---- | 2 8
    self.set_prefix("C", 0)
    cycles(8)
if prefix == 0xC2: # SET 0,D     | ---- | 2 8
    self.set_prefix("D", 0)
    cycles(8)
if prefix == 0xC3: # SET 0,E     | ---- | 2 8
    self.set_prefix("E", 0)
    cycles(8)
if prefix == 0xC4: # SET 0,H     | ---- | 2 8
    self.set_prefix("H", 0)
    cycles(8)
if prefix == 0xC5: # SET 0,L     | ---- | 2 8
    self.set_prefix("L", 0)
    cycles(8)
if prefix == 0xC6: # SET 0,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 0)
    cycles(16)
if prefix == 0xC7: # SET 0,A     | ---- | 2 8
    self.set_prefix("A", 0)
    cycles(8)
if prefix == 0xC8: # SET 1,B     | ---- | 2 8
    self.set_prefix("B", 1)
    cycles(8)
if prefix == 0xC9: # SET 1,C     | ---- | 2 8
    self.set_prefix("C", 1)
    cycles(8)
if prefix == 0xCA: # SET 1,D     | ---- | 2 8
    self.set_prefix("D", 1)
    cycles(8)
if prefix == 0xCB: # SET 1,E     | ---- | 2 8
    self.set_prefix("E", 1)
    cycles(8)
if prefix == 0xCC: # SET 1,H     | ---- | 2 8
    self.set_prefix("H", 1)
    cycles(8)
if prefix == 0xCD: # SET 1,L     | ---- | 2 8
    self.set_prefix("L", 1)
    cycles(8)
if prefix == 0xCE: # SET 1,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 1)
    cycles(16)
if prefix == 0xCF: # SET 1,A     | ---- | 2 8
    self.set_prefix("A", 1)
    cycles(8)
if prefix == 0xD0: # SET 2,B     | ---- | 2 8
    self.set_prefix("B", 2)
    cycles(8)
if prefix == 0xD1: # SET 2,C     | ---- | 2 8
    self.set_prefix("C", 2)
    cycles(8)
if prefix == 0xD2: # SET 2,D     | ---- | 2 8
    self.set_prefix("D", 2)
    cycles(8)
if prefix == 0xD3: # SET 2,E     | ---- | 2 8
    self.set_prefix("E", 2)
    cycles(8)
if prefix == 0xD4: # SET 2,H     | ---- | 2 8
    self.set_prefix("H", 2)
    cycles(8)
if prefix == 0xD5: # SET 2,L     | ---- | 2 8
    self.set_prefix("L", 2)
    cycles(8)
if prefix == 0xD6: # SET 2,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 2)
    cycles(16)
if prefix == 0xD7: # SET 2,A     | ---- | 2 8
    self.set_prefix("A", 2)
    cycles(8)
if prefix == 0xD8: # SET 3,B     | ---- | 2 8
    self.set_prefix("B", 3)
    cycles(8)
if prefix == 0xD9: # SET 3,C     | ---- | 2 8
    self.set_prefix("C", 3)
    cycles(8)
if prefix == 0xDA: # SET 3,D     | ---- | 2 8
    self.set_prefix("D", 3)
    cycles(8)
if prefix == 0xDB: # SET 3,E     | ---- | 2 8
    self.set_prefix("E", 3)
    cycles(8)
if prefix == 0xDC: # SET 3,H     | ---- | 2 8
    self.set_prefix("H", 3)
    cycles(8)
if prefix == 0xDD: # SET 3,L     | ---- | 2 8
    self.set_prefix("L", 3)
    cycles(8)
if prefix == 0xDE: # SET 3,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 3)
    cycles(16)
if prefix == 0xDF: # SET 3,A     | ---- | 2 8
    self.set_prefix("A", 3)
    cycles(8)
if prefix == 0xE0: # SET 4,B     | ---- | 2 8
    self.set_prefix("B", 4)
    cycles(8)
if prefix == 0xE1: # SET 4,C     | ---- | 2 8
    self.set_prefix("C", 4)
    cycles(8)
if prefix == 0xE2: # SET 4,D     | ---- | 2 8
    self.set_prefix("D", 4)
    cycles(8)
if prefix == 0xE3: # SET 4,E     | ---- | 2 8
    self.set_prefix("E", 4)
    cycles(8)
if prefix == 0xE4: # SET 4,H     | ---- | 2 8
    self.set_prefix("H", 4)
    cycles(8)
if prefix == 0xE5: # SET 4,L     | ---- | 2 8
    self.set_prefix("L", 4)
    cycles(8)
if prefix == 0xE6: # SET 4,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 4)
    cycles(16)
if prefix == 0xE7: # SET 4,A     | ---- | 2 8
    self.set_prefix("A", 4)
    cycles(8)
if prefix == 0xE8: # SET 5,B     | ---- | 2 8
    self.set_prefix("B", 5)
    cycles(8)
if prefix == 0xE9: # SET 5,C     | ---- | 2 8
    self.set_prefix("C", 5)
    cycles(8)
if prefix == 0xEA: # SET 5,D     | ---- | 2 8
    self.set_prefix("D", 5)
    cycles(8)
if prefix == 0xEB: # SET 5,E     | ---- | 2 8
    self.set_prefix("E", 5)
    cycles(8)
if prefix == 0xEC: # SET 5,H     | ---- | 2 8
    self.set_prefix("H", 5)
    cycles(8)
if prefix == 0xED: # SET 5,L     | ---- | 2 8
    self.set_prefix("L", 5)
    cycles(8)
if prefix == 0xEE: # SET 5,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 5)
    cycles(16)
if prefix == 0xEF: # SET 5,A     | ---- | 2 8
    self.set_prefix("A", 5)
    cycles(8)
if prefix == 0xF0: # SET 6,B     | ---- | 2 8
    self.set_prefix("B", 6)
    cycles(8)
if prefix == 0xF1: # SET 6,C     | ---- | 2 8
    self.set_prefix("C", 6)
    cycles(8)
if prefix == 0xF2: # SET 6,D     | ---- | 2 8
    self.set_prefix("D", 6)
    cycles(8)
if prefix == 0xF3: # SET 6,E     | ---- | 2 8
    self.set_prefix("E", 6)
    cycles(8)
if prefix == 0xF4: # SET 6,H     | ---- | 2 8
    self.set_prefix("H", 6)
    cycles(8)
if prefix == 0xF5: # SET 6,L     | ---- | 2 8
    self.set_prefix("L", 6)
    cycles(8)
if prefix == 0xF6: # SET 6,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 6)
    cycles(16)
if prefix == 0xF7: # SET 6,A     | ---- | 2 8
    self.set_prefix("A", 6)
    cycles(8)
if prefix == 0xF8: # SET 7,B     | ---- | 2 8
    self.set_prefix("B", 7)
    cycles(8)
if prefix == 0xF9: # SET 7,C     | ---- | 2 8
    self.set_prefix("C", 7)
    cycles(8)
if prefix == 0xFA: # SET 7,D     | ---- | 2 8
    self.set_prefix("D", 7)
    cycles(8)
if prefix == 0xFB: # SET 7,E     | ---- | 2 8
    self.set_prefix("E", 7)
    cycles(8)
if prefix == 0xFC: # SET 7,H     | ---- | 2 8
    self.set_prefix("H", 7)
    cycles(8)
if prefix == 0xFD: # SET 7,L     | ---- | 2 8
    self.set_prefix("L", 7)
    cycles(8)
if prefix == 0xFE: # SET 7,(HL)  | ---- | 2 16
    self.set_prefix("(HL)", 7)
    cycles(16)
if prefix == 0xFF: # SET 7,A     | --- | 2 8
    self.set_prefix("A", 7)
    cycles(8)
