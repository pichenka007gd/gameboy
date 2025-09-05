from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge
from app import App
from logger import Logger
from common import Common

import time
import numpy as np

class GameBoy:
    def __init__(self, window: bool = True, screen: bool = True) -> None:
        self.running = False
        self.cpu = CPU()
        self.memory = Memory()
        self.gpu = GPU()
        self.input = Input()
        self.cartridge = Cartridge()
        self.common = Common(self)


        self.screen = screen
        self.stopped = False
        self.defualt_Hz = 4

        self.window = window
        if self.window:
            self.app = App(self)
        
    def initialize(self) -> None:
        self.cpu.reset()
        self.cpu.connect(self)
        self.gpu.connect_memory(self.memory)
        self.running = True
        if self.window:
            self.app.start()
            self.app.ready_event.wait()

    def reset(self) -> None:
        self.cpu.reset()
        memory = Memory()
        memory.rom = self.memory.rom
        self.memory = memory
        self.cpu.connect(self)

    def load_rom(self, rom_path: str) -> bool:
        self.cartridge.load(rom_path)
        for i in range(len(self.cartridge.rom_data)):
            self.memory.rom[i] = self.cartridge.rom_data[i]
            
    def handle_input(self):
        pass
                    
    def update_screen(self, force=False):
        if self.window:
            screen_buffer = self.gpu.get_screen()
            screen_surface = np.repeat(screen_buffer[:, :, np.newaxis] * 85, 3, axis=2)
            if force or not (self.cpu.halted or self.cpu.stopped):
                self.app.update_memory(self.memory.rom, self.cpu)
                self.app.update_info(self.cpu)
                if force or self.app.view_type in ["last", "oam", "io", "hram"]:
                    self.app.update_ram(self.memory, self.cpu)
                if self.screen:
                    self.app.update_image(self.gpu.get_screen())
            else:
                self.app.root.update()

        #cv2.imshow('Game Boy Screen', screen_surface)
        #cv2.waitKey(1)
        #self.screen.blit(screen_surface, (0, 0))

    def run(self, speed_percent=100):
        self.initialize()
        self.cycles = 0
        self.steps = 0

        self.next = False



        self.Hz = self.defualt_Hz
        speed_coef = speed_percent / 100.0
        effective_Hz = self.Hz * speed_coef

        last_fps_time = time.time()
        last_cycles = time.time()
        last_update = time.time()
        cycles = 0
        steps = 0
        wait_time = 0.01

        last_cycles = int(time.time())
        while int(time.time()) == last_cycles:
            pass

        while True:

            if time.time() - last_update > 1/(2 if self.screen else 30):
                effective_Hz = self.Hz * speed_coef
                self.update_screen()
                time.sleep(0.01)
                last_update = time.time()

            if self.next or (not (self.cpu.halted or self.cpu.stopped) and int(time.time()) == int(last_cycles) and steps < effective_Hz*(time.time()-int(time.time()))):
                cycles = self.cpu.step()
                self.cycles += cycles
                self.steps += 1
                steps += 1
                self.gpu.step(cycles)
                if self.next: self.update_screen(force=True)
                self.next = False

            if int(time.time()) != int(last_cycles):
                last_cycles = int(time.time())
                steps = 0
                cycles = 0
            if self.steps >= 10000:
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

    def dump(self, type: str) -> None:
        path = f"../dump.{type}"
        with open(path, "wb") as f:
            f.write(getattr(self.memory,  type))
        print(f"dumped by: {path}")

    def close(self):
        SystemExit()