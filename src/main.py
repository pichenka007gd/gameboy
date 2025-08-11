from gameboy import GameBoy
from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge
from app import App
from logger import Logger

import sys
import time
import signal
from functools import partial

import numpy as np
import cv2
from tkinter import *
from tkinter import ttk
import atexit



if __name__ == "__main__":
    gameboy = GameBoy(screen=False)
    gameboy.load_rom("../tests/gb-test-roms/instr_timing/instr_timing.gb")
    #gameboy.load_rom("/storage/emulated/0/300/gameboy/assets/Battle City.gb")
        
    #gameboy.load_rom("../assets/Tetris (World) (Rev A).gb")




    gameboy.run()

    """if len(sys.argv) > 1:
        if gameboy.load_rom(sys.argv[1]):
            gameboy.run()
        else:
            print("Failed to load ROM file")"""