import pytest
#import heartrate; heartrate.trace(browser=True)


import inspect
import time
import os
import sys
import glob
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import App
from cartridge import Cartridge
from cpu import CPU
from gameboy import GameBoy
from gpu import GPU
from input import Input
from logger import Logger
from memory import Memory
from pyboy_class import GameBoyInspector




ROMS_DIR = os.path.join(os.path.dirname(__file__), "gb-test-roms", "cpu_instrs", "individual")

def collect_roms():
    roms = []
    for pattern in ["*.gb"]:
        roms.extend(glob.glob(os.path.join(ROMS_DIR, pattern)))
    return sorted(set(os.path.abspath(p) for p in roms))

ROM_FILES = [collect_roms()[0]]
#R OM_FILES = collect_roms()



@pytest.mark.parametrize("path", ROM_FILES, ids=lambda p: f'"{os.path.basename(p)}"')
def test_cpu_instrs(path):
    gb = GameBoy(window=False)
    gb.load_rom(path)
    gb.initialize()
    gbi = GameBoyInspector(path)

    print()
    print("="*70)

    for i in range(0x100):
        gbi.pyboy.memory[i] = 0x00
    gbi.pyboy.memory[0xFF50] = 0x01
    rf = gbi.pyboy.register_file
    rf.PC = 0x100
    cpu = gb.cpu

    gb_cycles = 0
    gbi_cycles = 0

    gb_ram = bytearray([gb.memory.read_byte(i) for i in range(0xFFFF)])
    gbi_ram = bytearray([gbi.pyboy.memory[i] for i in range(0xFFFF)])



    for step in range(100000):
        gb_cycles = gb.cpu.step()
        gbi_cycles = gbi.step()

        gbi_log = f"pc: {rf.PC:04X}, sp: {rf.SP:04X}, a: {rf.A:02X}, b: {rf.B:02X}, c: {rf.C:02X}, d: {rf.D:02X}, e: {rf.E:02X}, hl: {rf.HL:04X}, f: {rf.F:02X}"
        gb_log  = f"pc: {cpu.pc:04X}, sp: {cpu.sp:04X}, a: {cpu.a:02X}, b: {cpu.b:02X}, c: {cpu.c:02X}, d: {cpu.d:02X}, e: {cpu.e:02X}, hl: {cpu.get_reg_pair("HL"):04X}, f: {cpu.f:02X}"

        
        #gbi_ram = gbi.pyboy.mb.ram.internal_ram0[0:0x2000]
        #print(len([gbi.pyboy.memory[i] for i in range(0xFFFF)]))
        #print(0xFFFF)
        #gb_ram = gb.memory.ram 
        


        gb_ram = bytearray([gb.memory.read_byte(i) for i in range(0xFFFF)])
        gbi_ram = bytearray([gbi.pyboy.memory[i] for i in range(0xFFFF)])

        for i in range(len(gb_ram)):
            if gb_ram[i] != gbi_ram[i]:
                print(gbi_ram[i], gb_ram[i], f"{i:02X}", "Error")
                #dump()
        exit()


        # gbi_ram = list(gbi.pyboy.memory)

        def dump():
            open("dump.gbi", "wb").write(gbi_ram)
            open("dump.gb", "wb").write(gb_ram)
        def log():
            print("gbi | ", gbi_log, step)
            print("gb  | ", gb_log, step)
            print(f"{gb.cpu.opcode:02X}")
            print(f"="*70)
            #dump()


        for i in range(len(gb_ram)):
            if gb_ram[i] != gbi_ram[i]:
                print(gbi_ram[i], gb_ram[i], f"{i:02X}", "Error")
                dump()
                exit()
        #assert gbi_ram == gb_ram, dump()
        print(100)


        assert gbi_log == gb_log, log()
        if step % 1 == 0:
            log()
        assert gbi_cycles == gb_cycles, log()
        # reference = gbi.get_cpu_state()
        #assert gb.cpu.pc == rf.PC
        #assert list(gb.memory.hram) == reference["STACK"]
        


# 16468 <- 16461
# E           AssertionError: assert 'pc: C249, sp: DFFF, a: C3, b: 00, c: 00, d: D0, e: 00, hl: C7B1, f: C0' == 'pc: C247, sp: DFFF, a: C3, b: 00, c: 00, d: D0, e: 00, hl: C7B1, f: C0'
# E             
# E             - pc: C247, sp: DFFF, a: C3, b: 00, c: 00, d: D0, e: 00, hl: C7B1, f: C0
# E             ?        ^
# E             + pc: C249, sp: DFFF, a: C3, b: 00, c: 00, d: D0, e: 00, hl: C7B1, f: C0
# E             ?        ^

