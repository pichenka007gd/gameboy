import pytest

import inspect
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

@pytest.mark.parametrize("path", ROM_FILES, ids=lambda p: f'"{os.path.basename(p)}"')
def test_cpu_instrs(path):
    print("="*70)
    gb = GameBoy(window=False)
    gb.load_rom(path)
    gb.initialize()
    gbi = GameBoyInspector(path)


    for i in range(0x100):
        gbi.pyboy.memory[i] = 0x00
    gbi.pyboy.memory[0xFF50] = 0x01
    rf = gbi.pyboy.register_file
    rf.PC = 0x100
    cpu = gb.cpu

    for step in range(100):
        print(f"pc: {rf.PC:04X}, sp: {rf.SP:04X}, a: {rf.A:02X}, b: {rf.B:02X}, c: {rf.C:02X}, d: {rf.D:02X}, e: {rf.E:02X}, hl: {rf.HL:04X}, f: {rf.F:02X}")
        print(f"pc: {cpu.pc:04X}, sp: {cpu.sp:04X}, a: {cpu.a:02X}, b: {cpu.b:02X}, c: {cpu.c:02X}, d: {cpu.d:02X}, e: {cpu.e:02X}, hl: {cpu.h<<4&cpu.l:04X}, f: {cpu.f:02X}")
        print(f"="*70)
        # f"{gb.cpu.pc:04X}")
        cycles = gb.cpu.step()
        alive = gbi.step()
        reference = gbi.get_cpu_state()
        #assert gb.cpu.pc == rf.PC
        #assert list(gb.memory.hram) == reference["STACK"]
        




