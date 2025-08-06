from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge

import sys
import time

import pygame
import numpy as np

class GameBoy:
    def __init__(self):
        self.running = False
        self.cpu = CPU()
        self.memory = Memory()
        self.gpu = GPU()
        self.input = Input()
        self.cartridge = Cartridge()
        
        # Подключаем компоненты друг к другу
        self.cpu.connect_memory(self.memory)
        self.gpu.connect_memory(self.memory)
        
        # Инициализируем pygame для отображения
        pygame.init()
        self.screen = pygame.display.set_mode((160 * 3, 144 * 3))
        pygame.display.set_caption("GameBoy Emulator")
        
    def initialize(self):
        """Initialize GameBoy hardware components"""
        self.cpu.reset()
        self.running = True
        
    def load_rom(self, rom_path: str) -> bool:
        """Load ROM file into memory"""
        if self.cartridge.load(rom_path):
            # Копируем ROM в память
            for i in range(len(self.cartridge.rom_data)):
                self.memory.rom[i] = self.cartridge.rom_data[i]
            return True
        return False
            
    def handle_input(self):
        """Обработка ввода"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.input.press('up')
                elif event.key == pygame.K_DOWN:
                    self.input.press('down')
                elif event.key == pygame.K_LEFT:
                    self.input.press('left')
                elif event.key == pygame.K_RIGHT:
                    self.input.press('right')
                elif event.key == pygame.K_z:
                    self.input.press('a')
                elif event.key == pygame.K_x:
                    self.input.press('b')
                elif event.key == pygame.K_RETURN:
                    self.input.press('start')
                elif event.key == pygame.K_SPACE:
                    self.input.press('select')
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.input.release('up')
                elif event.key == pygame.K_DOWN:
                    self.input.release('down')
                elif event.key == pygame.K_LEFT:
                    self.input.release('left')
                elif event.key == pygame.K_RIGHT:
                    self.input.release('right')
                elif event.key == pygame.K_z:
                    self.input.release('a')
                elif event.key == pygame.K_x:
                    self.input.release('b')
                elif event.key == pygame.K_RETURN:
                    self.input.release('start')
                elif event.key == pygame.K_SPACE:
                    self.input.release('select')
                    
    def update_screen(self):
        """Обновление экрана"""
        # Получаем текущий буфер экрана и масштабируем его
        screen_buffer = self.gpu.get_screen()
        # Преобразуем в формат RGB
        screen_surface = np.repeat(screen_buffer[:, :, np.newaxis] * 85, 3, axis=2)
        # Масштабируем
        screen_surface = pygame.surfarray.make_surface(screen_surface)
        screen_surface = pygame.transform.scale(screen_surface, (160 * 3, 144 * 3))
        self.screen.blit(screen_surface, (0, 0))
        pygame.display.flip()
            
    def run(self):
        """Main emulation loop"""
        self.initialize()
        last_time = time.time()
        while self.running:
            while True:
                cycles = self.cpu.step()
                self.gpu.step(cycles)
                self.update_screen()
            # Обработка ввода
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
    gameboy.load_rom("/run/media/root/1EAE9FF1AE9FC027/python/gameboy/src/Tetris (World) (Rev A).gb")
    gameboy.run()
    """if len(sys.argv) > 1:
        if gameboy.load_rom(sys.argv[1]):
            gameboy.run()
        else:
            print("Failed to load ROM file")"""
