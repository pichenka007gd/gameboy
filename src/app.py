from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge

import sys
import os
import random
import time
from queue import Queue, Empty
import threading
import platform

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np





class App(threading.Thread):
    def __init__(self, gb) -> None:
        super().__init__()
        self.daemon = False
        self.command_queue = Queue()

        self.gb = gb
        self.platform = platform.system()
        self.view_type = "last"

        self.ready_event = threading.Event()

    def exit(self):
        self.root.destroy()
        self.gb.close()
        os._exit(0)

    def run(self) -> None:
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.title("Game Boy Debugger")

        if self.platform == "Android":
            self.memory_text = tk.Text(self.root, width=75, height=9, font=("Courier", 4))
            self.memory_text.pack(pady=20)
            self.memory_text.tag_configure("red", foreground="red")
            self.info_label = tk.Label(self.root, text="")
            self.info_label.pack()
            self.reg_label = tk.Label(self.root, text="")
            self.reg_label.pack()
            self.ram_text = tk.Text(self.root, width=75, height=24, font=("Courier", 4))
            self.ram_text.pack(pady=20)
            self.ram_text.tag_configure("green", foreground="green")
            array = np.zeros((144, 160, 3), dtype=np.uint8)
            array[:, :] = [0, 0, 0] 
            img = Image.fromarray(array).resize((160, 144))
            self.image = ImageTk.PhotoImage(img)
            self.screen = tk.Label(self.root, image=self.image)
            self.screen.pack()
            self.root.Button(self.root, text="dump", command=lambda: self.gb.dump())

        elif self.platform in ["Windows", "Linux"]:
            self.memory_text = tk.Text(self.root, width=80, height=17, font=("Courier", 8))
            self.memory_text.pack(padx=10, pady=15)
            self.memory_text.tag_configure("red", foreground="red")
            self.info_label = tk.Label(self.root, text="")
            self.info_label.pack()
            self.reg_label = tk.Label(self.root, text="")
            self.reg_label.pack()
            self.ram_text = tk.Text(self.root, width=80, height=17, font=("Courier", 8))
            self.ram_text.pack(padx=10, pady=15)
            self.ram_text.tag_configure("green", foreground="green")
            self.down_container = tk.Frame(self.root)
            self.down_container.grid_columnconfigure(0, weight=0)
            self.down_container.grid_columnconfigure(1, weight=1)
            self.down_container.pack(fill="x", padx=10)
            array = np.zeros((144, 160, 3), dtype=np.uint8)
            img = Image.fromarray(array)
            self.image = ImageTk.PhotoImage(img)
            self.screen = tk.Label(self.down_container, image=self.image)
            self.screen.pack(pady=10, side="left")
            self.button_container = tk.Frame(self.down_container)
            self.button_container.pack(fill="y", side="left", padx=10, pady=10)
            self.columns = 5
            for c in range(self.columns):
                self.button_container.columnconfigure(c, weight=1)
            self.q = 0
            def add_button(text, func):
                setattr(self, f"{text}_button", tk.Button(self.button_container, text=text, command=func, font=("Courier", 7)))
                getattr(self, f"{text}_button").grid(column=self.q//(self.columns)+1, row=self.q%self.columns, padx=3, pady=2)
                self.q += 1
            add_button(f"dump vram", lambda: self.gb.dump("vram"))
            add_button(f"dump ram", lambda: self.gb.dump("ram"))
            add_button(f"dump oam", lambda: self.gb.dump("oam"))
            add_button(f"dump io", lambda: self.gb.dump("io"))
            add_button(f"dump hram", lambda: self.gb.dump("hram"))

            add_button(f"view vram", lambda: {setattr(self, "view_type", "vram"), self._update_ram(self.gb.memory, self.gb.cpu)})
            add_button(f"view ram", lambda: {setattr(self, "view_type", "ram"), self._update_ram(self.gb.memory, self.gb.cpu)})
            add_button(f"view oam", lambda: {setattr(self, "view_type", "oam"), self._update_ram(self.gb.memory, self.gb.cpu)})
            add_button(f"view io", lambda: {setattr(self, "view_type", "io"), self._update_ram(self.gb.memory, self.gb.cpu)})
            add_button(f"view hram", lambda: {setattr(self, "view_type", "hram"), self._update_ram(self.gb.memory, self.gb.cpu)})

            add_button(f"last", lambda: {setattr(self, "view_type", "last"), self._update_ram(self.gb.memory, self.gb.cpu)})
            add_button(f"continue", lambda: {setattr(self.gb.cpu, "stopped", False), setattr(self.gb, "Hz", self.gb.Hz*2)})
            add_button(f"stop", lambda: {setattr(self.gb.cpu, "stopped", True), setattr(self.gb, "Hz", max(1, self.gb.Hz//2)), self._update_info(self.gb.cpu)})
            add_button(f"next", lambda: {setattr(self.gb, "next", True), time.sleep(0.02), self.root.update()})
            add_button(f"reset", lambda: {setattr(self.gb.cpu, "stopped", True), self.gb.reset()})


        self.root.after(20, self.process_commands)

        self.ready_event.set()

        self.root.mainloop()

    def process_commands(self) -> None:
        try:
            while True:
                cmd, args = self.command_queue.get_nowait()
                if cmd == "update_memory":
                    self._update_memory(*args)
                elif cmd == "update_ram":
                    self._update_ram(*args)
                elif cmd == "update_info":
                    self._update_info(*args)
                elif cmd == "update_image":
                    self._update_image(*args)
                elif cmd == "close":
                    self.root.destroy()
                    return
        except Empty:
            pass
        self.root.after(20, self.process_commands)

    def update_ram(self, ram_bytes: bytearray, cpu: CPU) -> None:
        self.command_queue.put(("update_ram", (ram_bytes, cpu,)))

    def _update_ram(self, memory: Memory, cpu: CPU) -> None:
        self.ram_text.delete("1.0", tk.END)
        def get_line(chunk: bytearray) -> str:
            hex_bytes = ' '.join(f"{b:02X}" for b in chunk)
            ascii_bytes = ''.join((chr(b) if 32 <= b <= 126 else '.') for b in chunk)
            return f"{i:04X}  {hex_bytes:<48}  {ascii_bytes}\n"
        if self.view_type == "last":
            for i in range(abs(memory.last//16*16-16*3), abs(memory.last//16*16+16*16-16*3), 16):
                chunk = [memory.read_byte(i&0xFFFF) for i in range(i, i+16, 1)]
                self.ram_text.insert(tk.END, get_line(chunk))
            self.ram_text.tag_add("green", f"{4}.{6+int(memory.last%16*3)}", f"{4}.{6+int(memory.last%16*3)+2}")
        elif self.view_type == "vram":
            for i in range(0x8000, 0xA000, 16):
                chunk = [memory.read_byte(i&0xFFFF) for i in range(i, i+16, 1)]
                self.ram_text.insert(tk.END, get_line(chunk))
        elif self.view_type == "ram":
            for i in range(0xC000, 0xE000, 16):
                chunk = [memory.read_byte(i&0xFFFF) for i in range(i, i+16, 1)]
                self.ram_text.insert(tk.END, get_line(chunk))
        elif self.view_type == "oam":
            for i in range(0xFE00, 0xFF80, 16):
                chunk = [memory.read_byte(i&0xFFFF) for i in range(i, i+16, 1)]
                self.ram_text.insert(tk.END, get_line(chunk))
        elif self.view_type == "io":
            for i in range(0xFF00, abs(memory.last//16*16+16*16-16*3), 16):
                chunk = [memory.read_byte(i&0xFFFF) for i in range(i, i+16, 1)]
                self.ram_text.insert(tk.END, get_line(chunk))
        elif self.view_type == "hram":
            for i in range(0xFF80, 0xFFFF, 16):
                chunk = [memory.read_byte(i&0xFFFF) for i in range(i, i+16, 1)]
                self.ram_text.insert(tk.END, get_line(chunk))

        #self.ram_text.see(f"{int(cpu.pc/16)}.0")

    def update_memory(self, memory_bytes: bytearray, cpu: CPU) -> None:
        self.command_queue.put(("update_memory", (memory_bytes, cpu,)))

    def _update_memory(self, ram_bytes: bytearray, cpu: CPU) -> None:
        self.memory_text.delete("1.0", tk.END)

        for i in range(cpu.pc//16*16, cpu.pc//16*16+16*16, 16):
            chunk = ram_bytes[i:i+16]
            hex_bytes = ' '.join(f"{b:02X}" for b in chunk)
            ascii_bytes = ''.join((chr(b) if 32 <= b <= 126 else '.') for b in chunk)
            line = f"{i:04X}  {hex_bytes:<48}  {ascii_bytes}\n"
            self.memory_text.insert(tk.END, line)
        #self.memory_text.see(f"{int(cpu.pc/16)}.0")
        self.memory_text.tag_add("red", f"{1}.{6+int(cpu.pc%16*3)}", f"{1}.{6+int(cpu.pc%16*3)+2}")

    def update_info(self, cpu: CPU) -> None:
        self.command_queue.put(("update_info", (cpu,)))

    def _update_info(self, cpu: CPU) -> None:
        self.info_label.config(text=f"pc: {cpu.pc}, Z: {int(bool(cpu.f & cpu.FLAG_Z))}, N: {int(bool(cpu.f & cpu.FLAG_N))}, H: {int(bool(cpu.f & cpu.FLAG_H))}, C: {int(bool(cpu.f & cpu.FLAG_C))}, Hz: {self.gb.Hz}")
        self.reg_label.config(text=f"a: {str(cpu.a).ljust(3)}, b: {str(cpu.b).ljust(3)}, c: {str(cpu.c).ljust(3)}, d: {str(cpu.d).ljust(3)}, e: {str(cpu.e).ljust(3)}, h: {str(cpu.h).ljust(3)}, l: {str(cpu.l).ljust(3)}")
        
    def update_image(self, buffer: bytearray) -> None:
        self.command_queue.put(("update_image", (buffer,)))

    def _update_image(self, buffer: bytearray) -> None:
        buffer = np.array(buffer).reshape(144, 160)
        self.image = ImageTk.PhotoImage(Image.fromarray(buffer))
        self.screen.config(image=self.image)
        
        
    def close(self) -> None:
        self.command_queue.put(("close", ()))

if __name__ == "__main__":
    from gameboy import GameBoy


    dbg_window = App(GameBoy())
    dbg_window.start()

    dbg_window.ready_event.wait()

    cpu = CPU()
    cpu.connect_memory(Memory())

    for i in range(0xFF):
        fake_image = bytearray(random.getrandbits(8) for _ in range(160*144))
        fake_memory = bytearray(random.getrandbits(8) for _ in range(256))
        fake_ram = bytearray(random.getrandbits(8) for _ in range(512))
        cpu.memory.rom = fake_ram
        cpu.pc = 0x00 + i * 1

        dbg_window.update_memory(fake_memory, cpu)
        if not dbg_window.gb.cpu.stopped: dbg_window.update_ram(cpu.memory, cpu)
        dbg_window.update_info(cpu)
        dbg_window.update_image(fake_image)
        time.sleep(0.5)

    dbg_window.close()