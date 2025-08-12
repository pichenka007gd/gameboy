"""
этот класс я накидал в perplexity
спасибо https://github.com/Baekalfen/PyBoy за открытый эмулятор
с его помощью я буду сравнивать поведение своего эмулятора с эталоном
i whipped up this class in Perplexity
thanks to https://github.com/Baekalfen/PyBoy for the open emulator
i'll use it to compare the behavior of my emulator with the reference implementation
"""

import time
import argparse
from typing import Optional

import warnings
warnings.filterwarnings(
    "ignore",
    message="Using SDL2 binaries from pysdl2-dll",
    category=UserWarning,
    module="sdl2._internal",
)

from pyboy import PyBoy


class GameBoyInspector:
    def __init__(self, rom_path: str, *, bootrom: Optional[str] = None, slow_delay: float = 0.0, window: bool = False):
        window_backend = "null" if not window else "SDL2"
        self.pyboy = PyBoy(
            rom_path,
            window=window_backend,
            bootrom=bootrom,
            sound_emulated=False,
            cgb=None,
            log_level="ERROR",
        )
        self.slow_delay = slow_delay
        self.step_count = 0

    def read_byte(self, addr: int) -> int:
        if not (0 <= addr <= 0xFFFF):
            raise ValueError("Address must be in range 0x0000..0xFFFF")
        return self.pyboy.memory[addr]

    def read_range(self, start: int, length: int) -> bytes:
        if length < 0:
            raise ValueError("Length must be non-negative")
        end = start + length
        if not (0 <= start <= 0xFFFF) or not (0 <= end - 1 <= 0xFFFF):
            raise ValueError("Range must be within 0x0000..0xFFFF")
        return bytes(self.pyboy.memory[addr] for addr in range(start, end))

    def read_memory_region(self, start: int, end: int) -> dict:
        """Read memory region and return as dictionary."""
        if start > end or start < 0 or end > 0xFFFF:
            raise ValueError("Invalid memory range")
        return {f"0x{addr:04X}": self.pyboy.memory[addr] for addr in range(start, end + 1)} # ps. йоу афигеть я не знал что так можно

    def get_cpu_state(self) -> dict:
        try:
            state = {
                # LCD registers
                "LCDC": self.pyboy.memory[0xFF40],    # LCD Control
                "STAT": self.pyboy.memory[0xFF41],    # LCD Status
                "SCY": self.pyboy.memory[0xFF42],     # Scroll Y
                "SCX": self.pyboy.memory[0xFF43],     # Scroll X
                "LY": self.pyboy.memory[0xFF44],      # LCD Y Coordinate
                "LYC": self.pyboy.memory[0xFF45],     # LCD Y Compare
                "WY": self.pyboy.memory[0xFF4A],      # Window Y Position
                "WX": self.pyboy.memory[0xFF4B],      # Window X Position
                
                # Timer
                "DIV": self.pyboy.memory[0xFF04],     # Divider Register
                "TIMA": self.pyboy.memory[0xFF05],    # Timer Counter
                "TMA": self.pyboy.memory[0xFF06],     # Timer Modulo
                "TAC": self.pyboy.memory[0xFF07],     # Timer Control
                
                # Interrupts
                "IF": self.pyboy.memory[0xFF0F],      # Interrupt Flag
                "IE": self.pyboy.memory[0xFFFF],      # Interrupt Enable
                
                # Joypad
                "JOYP": self.pyboy.memory[0xFF00],    # Joypad
            }
            
            stack_start = 0xFFFE
            state["STACK"] = [self.pyboy.memory[index] for index in range(0xFF80, 0xFFFF, 1)]

            state["MEMORY"] = self.pyboy.memory
            
            return state
            
        except Exception as e:
            return {"error": str(e)}

    def format_state_display(self) -> str:
        state = self.get_cpu_state()
        
        if "error" in state:
            return f"State reading error: {state['error']}"
        
        main_regs = (
            f"LCDC=0x{state['LCDC']:02X} STAT=0x{state['STAT']:02X} "
            f"LY=0x{state['LY']:02X} SCX=0x{state['SCX']:02X} SCY=0x{state['SCY']:02X}"
        )
        
        timer_int = (
            f"DIV=0x{state['DIV']:02X} TIMA=0x{state['TIMA']:02X} "
            f"IF=0x{state['IF']:02X} IE=0x{state['IE']:02X}"
        )
        
        stack_str = " ".join(f"0x{b:02X}" for b in state['STACK'])
        wram_str = " ".join(f"0x{b:02X}" for b in state['WRAM'])
        
        return f"{main_regs} | {timer_int} | STACK:[{stack_str}] | WRAM:[{wram_str}]"

    def step_and_print(self, steps: int = 1):
        print(f"\n=== Starting step-by-step execution ({steps} steps) ===")
        print("Note: Showing memory state and I/O registers, as CPU registers are not accessible through PyBoy public API")
        
        for i in range(steps):
            try:
                # Execute one emulator tick
                # In PyBoy 2.0+ tick() returns True while emulation is active
                alive = self.pyboy.tick()
                self.step_count += 1
                
                # Format and display state
                state_str = self.format_state_display()
                #print(f"Step {self.step_count:6d}: {state_str}")
                
                # Slow delay if enabled
                if self.slow_delay > 0:
                    time.sleep(self.slow_delay)
                
                # Check if emulation is alive (in v2.0+ logic is inverted)
                if not alive:
                    print("*** Emulation finished ***")
                    break
                    
            except KeyboardInterrupt:
                print("\n*** Interrupted by user (Ctrl+C) ***")
                break
            except Exception as e:
                print(f"*** Error at step {self.step_count}: {e} ***")
                break

    def step(self) -> bool:
        alive = self.pyboy.__mb.cpu.fetch_and_execute()
        #alive = self.pyboy.tick()
        self.step_count += 1
        return alive


    def run_continuous(self):
        """Run continuous execution with output on each tick."""
        print("\n=== Starting continuous execution ===")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # In PyBoy 2.0+ tick() returns True while emulation is running
                alive = self.pyboy.tick()
                self.step_count += 1
                
                #state_str = self.format_state_display()
                #print(f"Step {self.step_count:6d}: {state_str}")
                
                #if self.slow_delay > 0:
                #    time.sleep(self.slow_delay)
                
                if not alive:
                    print("*** Emulation finished ***")
                    break
                    
        except KeyboardInterrupt:
            print(f"\n*** Stopped by user after {self.step_count} steps ***")

    def get_current_memory_state(self) -> dict:
        """Get current memory state as dictionary."""
        return self.get_cpu_state()

    def close(self):
        self.pyboy.stop()


def main():
    path = "gb-test-roms/cpu_instrs/individual/01-special.gb"
    inspector = None
    try:
        print(f"Load ROM: {path}")

        inspector = GameBoyInspector(
            path,
            bootrom=None,
            slow_delay=0.0,
            window=True
        )
        
        initial_state = inspector.get_current_memory_state()
        print(f"\nInitial state:")
        for key, value in initial_state.items():
            if isinstance(value, list):
                print(f"  {key}: {value}")
            else:
                print(f"  {key}: 0x{value:02X}")
        
        inspector.run_continuous()
        
    except FileNotFoundError:
        print(f"Error: ROM file '{path}' not found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if inspector:
            try:
                inspector.close()
            except:
                pass


if __name__ == "__main__":
    main()
