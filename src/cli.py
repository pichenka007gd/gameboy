import threading
import psutil
import time
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel

def memory_monitor(interval=1):
    process = psutil.Process()
    progress = Progress(
        TextColumn("[bold blue]Использование памяти:"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%")
    )
    task = progress.add_task("", total=100)

    with Live(progress, refresh_per_second=4):
        while True:
            mem = process.memory_percent()
            progress.update(task, completed=time.time()%100)
            time.sleep(interval)

if __name__ == "__main__":
    thread = threading.Thread(target=memory_monitor, daemon=True)
    thread.start()

    try:
        while True:
            time.sleep(0.1)  # Основной поток может выполнять работу
    except KeyboardInterrupt:
        print("Завершение программы")
