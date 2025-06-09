# hmi.py - Main Entry Point for Vertical Parking System

from models import ParkingSystem
from gui import ParkingHMI

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    system = ParkingSystem(num_slots=5)
    system.stopped = True  # Start system in OFF condition
    gui = ParkingHMI(root, system)
    root.mainloop()
