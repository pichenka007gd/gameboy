from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge
from app import App

import sys
import time

import numpy as np
from tkinter import *
from tkinter import ttk




class GameBoy:
    def __init__(self):
        self.running = False
        self.cpu = CPU()
        self.memory = Memory()
        self.gpu = GPU()
        self.input = Input()
        self.cartridge = Cartridge()

        self.cpu.connect_memory(self.memory)
        self.gpu.connect_memory(self.memory)

        self.app = App() # (160 * 3, 144 * 3)
        self.app.start()

        
    def initialize(self):
        self.cpu.reset()
        self.running = True
        self.app.ready_event.wait()
        
    def load_rom(self, rom_path: str) -> bool:
        if self.cartridge.load(rom_path):
            for i in range(len(self.cartridge.rom_data)):
                self.memory.rom[i] = self.cartridge.rom_data[i]
            return True
        return False
            
    def handle_input(self):
        pass
                    
    def update_screen(self):
        #screen_buffer = self.gpu.get_screen()
        #screen_surface = np.repeat(screen_buffer[:, :, np.newaxis] * 85, 3, axis=2)
        self.app.update_memory(self.memory.rom, self.cpu)
        self.app.update_info(self.cpu)
        #self.screen.blit(screen_surface, (0, 0))
            
    def run(self):
        self.initialize()
        last_time = time.time()
        self.cycles = 0
        while self.running:
            while True:
                cycles = self.cpu.step()
                self.cycles += cycles
                self.gpu.step(cycles)
                self.update_screen()
                time.sleep(0.001)
            self.handle_input()
            
            # Эмуляция одного кадра (примерно 70224 циклов)
            #cycles_this_frame = 0
            #while cycles_this_frame < 70224:
            #    cycles = self.cpu.step()
            #    self.gpu.step(cycles)
            #    cycles_this_frame += cycles
            
            # Обновление экрана
            #self.update_screen()
            
            # Поддержание частоты кадров (примерно 60 FPS)
            #current_time = time.time()
            #frame_time = current_time - last_time
            #if frame_time < 1/60:
            #    time.sleep(1/60 - frame_time)
            #last_time = current_time

if __name__ == "__main__":
    gameboy = GameBoy()
    print(gameboy.load_rom("../assets/Tetris (World) (Rev A).gb"))
    gameboy.run()
    """if len(sys.argv) > 1:
        if gameboy.load_rom(sys.argv[1]):
            gameboy.run()
        else:
            print("Failed to load ROM file")"""