from cpu import CPU
from memory import Memory
from gpu import GPU
from input import Input
from cartridge import Cartridge

import sys
import time
from queue import Queue, Empty
import threading

import tkinter as tk

class App(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.daemon = True
        self.command_queue = Queue()

        self.ready_event = threading.Event()

    def run(self) -> None:
        self.root = tk.Tk()
        self.root.title("Game Boy Debugger")

        self.memory_text = tk.Text(self.root, width=80, height=9, font=("Courier", 4))
        self.memory_text.pack()
        self.memory_text.tag_configure("red", foreground="red")

        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack()
        self.reg_label = tk.Label(self.root, text="")
        self.reg_label.pack()

        self.ram_text = tk.Text(self.root, width=80, height=34, font=("Courier", 4))
        self.ram_text.pack()
        self.ram_text.tag_configure("green", foreground="green")

        self.root.after(100, self.process_commands)

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
                elif cmd == "close":
                    self.root.destroy()
                    return
        except Empty:
            pass
        self.root.after(10, self.process_commands)

    def update_ram(self, ram_bytes: bytearray, cpu: CPU) -> None:
        self.command_queue.put(("update_ram", (ram_bytes, cpu,)))

    def _update_ram(self, ram_bytes: bytearray, cpu: CPU) -> None:
        self.ram_text.delete("1.0", tk.END)

        for i in range(0, 256, 16):
            chunk = ram_bytes[i:i+16]
            hex_bytes = ' '.join(f"{b:02X}" for b in chunk)
            ascii_bytes = ''.join((chr(b) if 32 <= b <= 126 else '.') for b in chunk)
            line = f"{i:04X}  {hex_bytes:<48}  {ascii_bytes}\n"
            self.ram_text.insert(tk.END, line)
        #self.ram_text.see(f"{int(cpu.pc/16)}.0")
        #self.ram_text.tag_add("red", f"{1}.{6+int(cpu.pc%16*3)}", f"{1}.{6+int(cpu.pc%16*3)+2}")

    def update_memory(self, memory_bytes: bytearray, cpu: CPU) -> None:
        self.command_queue.put(("update_memory", (memory_bytes, cpu,)))

    def _update_memory(self, memory_bytes: bytearray, cpu: CPU) -> None:
        self.memory_text.delete("1.0", tk.END)

        for i in range(int(cpu.pc/16), int(cpu.pc/16)+16*8, 16):
            chunk = memory_bytes[i:i+16]
            hex_bytes = ' '.join(f"{b:02X}" for b in chunk)
            ascii_bytes = ''.join((chr(b) if 32 <= b <= 126 else '.') for b in chunk)
            line = f"{i:04X}  {hex_bytes:<48}  {ascii_bytes}\n"
            self.memory_text.insert(tk.END, line)
        #self.memory_text.see(f"{int(cpu.pc/16)}.0")
        self.memory_text.tag_add("red", f"{1}.{6+int(cpu.pc%16*3)}", f"{1}.{6+int(cpu.pc%16*3)+2}")

    def update_info(self, cpu: CPU) -> None:
        self.command_queue.put(("update_info", (cpu,)))

    def _update_info(self, cpu: CPU) -> None:
        self.info_label.config(text=f"pc: {cpu.pc}, Z: {int(bool(cpu.f & cpu.FLAG_Z))}, N: {int(bool(cpu.f & cpu.FLAG_N))}, H: {int(bool(cpu.f & cpu.FLAG_H))}, C: {int(bool(cpu.f & cpu.FLAG_C))}")
        self.reg_label.config(text=f"a:{str(cpu.a).ljust(3)}, b: {str(cpu.b).ljust(3)}, c: {str(cpu.c).ljust(3)}, d: {str(cpu.d).ljust(3)}, e: {str(cpu.e).ljust(3)}, h: {str(cpu.h).ljust(3)}, l: {str(cpu.l).ljust(3)}")

    def close(self) -> None:
        self.command_queue.put(("close", ()))

if __name__ == "__main__":
    import random
    import time

    from types import SimpleNamespace

    dbg_window = App()
    dbg_window.start()

    dbg_window.ready_event.wait()

    cpu = CPU()

    for i in range(10):
        fake_memory = bytearray(random.getrandbits(8) for _ in range(256))
        fake_ram = bytearray(random.getrandbits(8) for _ in range(512))
        cpu.pc = 0x100 + i * 1

        dbg_window.update_memory(fake_memory, cpu)
        dbg_window.update_ram(fake_ram, cpu)
        dbg_window.update_info(cpu)
        time.sleep(1)