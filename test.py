import os
import time

file = b"C:\Users\Vaynes\Documents\SEGA\PHANTASYSTARONLINE2_NA_STEAM\log_ngs\ChatLog20250329_00.txt"

def _observer_thread_func() -> None:
    last_size = os.path.getsize(file)

    time.sleep(1)  
    current_size = os.path.getsize(file)
    if current_size > last_size:  
        with open(file, "r", encoding="utf-16") as f:
            f.seek(last_size) 
            new_lines = f.readlines()
            print(new_lines)

        last_size = current_size  

print("Watching")
while True:
    _observer_thread_func()