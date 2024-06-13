# speed meter by Sin
# Cs2 Da goat
import pymem
from pymem.process import module_from_name
import time
import tkinter as tk
import math
import pygetwindow as gw

dwLocalPlayerPawn = 0x181A998
m_vecAbsVelocity = 0x3D0

def initialize_pymem(process_name):
    pm = pymem.Pymem(process_name)
    client_base = module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    return pm, client_base

def read_vector(pm, client_base):
    local_player_pawn_ptr = pm.read_ulonglong(client_base + dwLocalPlayerPawn)
    if local_player_pawn_ptr:
        return [
            pm.read_float(local_player_pawn_ptr + m_vecAbsVelocity),
            pm.read_float(local_player_pawn_ptr + m_vecAbsVelocity + 4),
            pm.read_float(local_player_pawn_ptr + m_vecAbsVelocity + 8)
        ]
    return None

def calculate_speed(velocity):
    return math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)

def update_overlay(label, velocity):
    if velocity:
        speed = round(calculate_speed(velocity))
        label.config(text=f"Speed: {speed}")
    else:
        label.config(text="Speed: N/A")

def main():
    process_name = "cs2.exe"
    pm, client_base = initialize_pymem(process_name)
    
    root = tk.Tk()
    root.title("Speed Overlay")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 200
    window_height = 50
    x = screen_width - window_width - 10
    y = screen_height - window_height - 10
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    speed_label = tk.Label(root, text="Speed: N/A", font=("Arial", 18), bg="black", fg="white")
    speed_label.pack(pady=10)
    
    try:
        while True:
            active_window = gw.getActiveWindow()
            if active_window and active_window.title == "Counter-Strike 2":
                root.deiconify()
                vec_abs_velocity = read_vector(pm, client_base)
                update_overlay(speed_label, vec_abs_velocity)
            else:
                root.withdraw()
            
            root.update()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        root.destroy()
        del pm

if __name__ == "__main__":
    main()
