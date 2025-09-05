import pytest

import inspect
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cpu import CPU
from memory import Memory
from gameboy import GameBoy


def test_cpu_initial():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    assert cpu.a == 0
    assert cpu.b == 0
    assert cpu.c == 0
    assert cpu.d == 0
    assert cpu.e == 0
    assert cpu.h == 0
    assert cpu.l == 0
    assert cpu.f == 0x0000
    assert cpu.pc == 0x100
    assert cpu.sp == 0x0000 #0xFFFE
    assert cpu.cycles == 0
    assert cpu.interrupts_enabled is False
    assert cpu.halted is False
    assert cpu.stopped is False
    cpu.a, cpu.b, cpu.c, cpu.d, cpu.e, cpu.h, cpu.l, cpu.f = [0xFF]*8
    cpu.pc = 0x1
    cpu.sp = 0xFFFE
    cpu.cycles = 1
    cpu.interrupts_enabled = True
    cpu.halted = True
    cpu.stopped = True
    cpu.reset()
    assert cpu.a == 0
    assert cpu.b == 0
    assert cpu.c == 0
    assert cpu.d == 0
    assert cpu.e == 0
    assert cpu.h == 0
    assert cpu.l == 0
    assert cpu.f == 0
    assert cpu.pc == 0x100
    assert cpu.sp == 0x0000
    assert cpu.cycles == 0
    assert cpu.interrupts_enabled == False
    assert cpu.halted == False
    assert cpu.stopped == False

def test_register():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.set_reg('A', 0xAA)
    assert cpu.get_reg('A') == 0xAA

def test_register_pair():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.b = 0x12
    cpu.c = 0x34
    assert cpu.get_reg_pair('BC') == 0x1234
    cpu.set_reg_pair('BC', 0xABCD)
    assert cpu.b == 0xAB
    assert cpu.c == 0xCD

    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.d = 0x56
    cpu.e = 0x78
    assert cpu.get_reg_pair('DE') == 0x5678
    cpu.set_reg_pair('DE', 0x7A3F)
    assert cpu.d == 0x7A
    assert cpu.e == 0x3F

    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.h = 0x48
    cpu.l = 0x26
    assert cpu.get_reg_pair('HL') == 0x4826
    cpu.set_reg_pair('HL', 0xF7C9)
    assert cpu.h == 0xF7
    assert cpu.l == 0xC9

    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.a = 0x90
    cpu.f = 0x36
    assert cpu.get_reg_pair('AF') == 0x9036
    cpu.set_reg_pair('AF', 0x2E0F)
    assert cpu.a == 0x2E
    assert cpu.f == 0x0F

def test_flags():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.set_flag(cpu.FLAG_Z, True)
    assert cpu.get_flag(cpu.FLAG_Z)
    cpu.set_flag(cpu.FLAG_Z, False)
    assert not cpu.get_flag(cpu.FLAG_Z)

    cpu.set_flag(cpu.FLAG_N, True)
    assert cpu.get_flag(cpu.FLAG_N)
    cpu.set_flag(cpu.FLAG_N, False)
    assert not cpu.get_flag(cpu.FLAG_N)

    cpu.set_flag(cpu.FLAG_H, True)
    assert cpu.get_flag(cpu.FLAG_H)
    cpu.set_flag(cpu.FLAG_H, False)
    assert not cpu.get_flag(cpu.FLAG_H)

    cpu.set_flag(cpu.FLAG_C, True)
    assert cpu.get_flag(cpu.FLAG_C)
    cpu.set_flag(cpu.FLAG_C, False)
    assert not cpu.get_flag(cpu.FLAG_C)

def test_add():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.a = 10
    cpu.add_reg("A", 5)
    assert cpu.a == 15
    cpu.add_reg("A", 241)
    assert cpu.a == 0

def test_sub():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.a = 5
    cpu.sub_reg("A", 5)
    assert cpu.a == 0
    assert cpu.get_flag(cpu.FLAG_Z)
    cpu.set_reg('A', 2)
    cpu.sub_reg("A", 3)
    assert cpu.a == (2 - 3) & 0xFF

def test_inc_register():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.set_reg('B', 0xFF)
    cpu.inc_reg('B')
    assert cpu.get_reg('B') == 0
    assert cpu.get_flag(cpu.FLAG_Z)
    cpu.set_reg('C', 0x0F)
    cpu.inc_reg('C')
    assert cpu.get_reg('C') == 0x10
    assert cpu.get_flag(cpu.FLAG_H)

def test_dec_register():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.set_reg('B', 1)
    cpu.dec_reg('B')
    assert cpu.get_reg('B') == 0
    assert cpu.get_flag(cpu.FLAG_Z)
    cpu.set_reg('C', 0x00)
    cpu.dec_reg('C')
    assert cpu.get_reg('C') == 0xFF

"""def test_stack_push_pop():
    cpu = CPU()
    mem = Memory()
    cpu.memory = mem
    cpu.sp = 0xFF00
    cpu.push(0xABCD)
    assert cpu.sp == 0xFF00 - 2
    value = cpu.pop()
    assert value == 0xABCD
    assert cpu.sp == 0xFF00"""

def test_reset():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.pc = 0x77
    cpu.reset()
    assert cpu.pc == 0x100

def test_and_or_xor_cp():
    gb = GameBoy(window = False)
    cpu = gb.cpu
    cpu.a = 0b10101010
    cpu.and_reg("A", 0b11001100)
    assert cpu.a == (0b10101010 & 0b11001100)
    cpu.a = 0b10101010
    cpu.or_reg("A", 0b01010101)
    assert cpu.a == (0b10101010 | 0b01010101)
    cpu.a = 0b11110000
    cpu.xor_reg("A", 0b11111111)
    assert cpu.a == (0b11110000 ^ 0b11111111)
    cpu.a = 0x5A
    cpu.cp_reg("A", 0x5A)
    assert cpu.get_flag(cpu.FLAG_Z)




if __name__ == "__main__":


    current_module = sys.modules[__name__]

    functions = inspect.getmembers(current_module, inspect.isfunction)

    errors = set()

    for name, func in sorted(functions, key=lambda x: x[0]):
        try:
            func()
            print(f'Func: {name.ljust(30)}PASS')
        except:
            errors.add(name)
    for e in errors:
        print(f"Func: {e.ljust(30)}ERROR")


