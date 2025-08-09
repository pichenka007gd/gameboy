from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge
from app import App
from logger import Logger

import sys
import time

import numpy as np
import cv2
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
        self.cartridge.load(rom_path)
        for i in range(len(self.cartridge.rom_data)):
            self.memory.rom[i] = self.cartridge.rom_data[i]
            
    def handle_input(self):
        pass
                    
    def update_screen(self):
        screen_buffer = self.gpu.get_screen()
        screen_surface = np.repeat(screen_buffer[:, :, np.newaxis] * 85, 3, axis=2)
        self.app.update_memory(self.memory.rom, self.cpu)
        self.app.update_info(self.cpu)
        self.app.update_ram(self.memory, self.cpu)
        #cv2.imshow('Game Boy Screen', screen_surface)
        #cv2.waitKey(1)
        #self.screen.blit(screen_surface, (0, 0))

    def run(self, speed_percent=100):
        self.initialize()
        self.cycles = 0
        self.steps = 0



        Hz = 419.00000
        speed_coef = speed_percent / 100.0
        effective_Hz = Hz * speed_coef

        last_fps_time = time.time()
        last_cycles = time.time()
        last_update = time.time()
        cycles = 0
        steps = 0
        wait_time = 0.01

        last_cycles = int(time.time())
        while int(time.time()) == last_cycles:
            pass

        while not self.cpu.halted or not self.cpu.stopped:
            if time.time() - last_update > 1/30:
                self.update_screen()
                time.sleep(0.01)
                last_update = time.time()


            if int(time.time()) == int(last_cycles) and steps < effective_Hz*(time.time()-int(time.time())):

                cycles += self.cpu.step()
                self.cycles += cycles
                self.steps += 1
                steps += 1

                #self.gpu.step(cycles)

            if int(time.time()) != int(last_cycles):
                last_cycles = int(time.time())
                steps = 0
                cycles = 0
            if self.steps >= 1000:
                pass



            #self.handle_input()
            
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
    gameboy.load_rom("/storage/emulated/0/300/gameboy/tests/tests-roms/test.gb")
    gameboy.load_rom("/storage/emulated/0/300/gameboy/tests/gb-test-roms/cgb_sound/rom_singles/01-registers.gb")
        
    #gameboy.load_rom("../assets/Tetris (World) (Rev A).gb")
    gameboy.run()
    """if len(sys.argv) > 1:
        if gameboy.load_rom(sys.argv[1]):
            gameboy.run()
        else:
            print("Failed to load ROM file")"""