import time

class Logger:
    def __init__(self, filename="../gameboy.log", enable_console=True, level="INFO"):
        self.filename = filename
        self.enable_console = enable_console
        self.levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        self.level = level


    def set_level(self, level: str):
        if level in self.levels:
            self.level = level

    def log(self, msg, level="INFO"):
        if self.levels.index(level) < self.levels.index(self.level):
            return

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        #line = f"[{timestamp}] [{level}] {msg}\n"
        line = msg+"\n"

        with open(self.filename, "a") as f:
            f.write(line)
        if self.enable_console:
            print(line, end="")

    def step_log(self):
        def tracer(fn):
            def wrapped(this, *args, **kwargs):
                self.info(f"{this.memory.read_byte(this.pc):02X}")
                return fn(this, *args, **kwargs)
            return wrapped
        return tracer

    def debug(self, msg):
        self.log(msg, level="DEBUG")

    def info(self, msg):
        self.log(msg, level="INFO")

    def warning(self, msg):
        self.log(msg, level="WARNING")

    def error(self, msg):
        self.log(msg, level="ERROR")
