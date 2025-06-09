# hmi.py - Example HMI/Simulator for Vertical Parking

# This is a placeholder for a Python script that could simulate or interface with the PLC logic.
# You can expand this with a simple CLI or GUI for testing.

import tkinter as tk
import threading
import time

class ParkingSlot:
    def __init__(self, slot_id):
        self.slot_id = slot_id
        self.occupied = False

class ParkingSystem:
    def __init__(self, num_slots=5):
        self.num_slots = num_slots
        self.slots = [ParkingSlot(i+1) for i in range(num_slots)]
        self.ground_slot = 0  # index of slot at ground
        self.emergency = False
        self.fault = False
        self.status_msg = "System Ready"

    def get_status(self):
        return {
            'slots': [s.occupied for s in self.slots],
            'ground_slot': self.ground_slot,
            'emergency': self.emergency,
            'fault': self.fault,
            'status_msg': self.status_msg
        }

    def park_car(self):
        if self.emergency or self.fault:
            self.status_msg = "Cannot park: Emergency or Fault!"
            return
        empty_slots = [i for i, s in enumerate(self.slots) if not s.occupied]
        if not empty_slots:
            self.status_msg = "No empty slots. Parking Full!"
            return
        target = empty_slots[0]
        self.rotate_to_slot(target)
        self.slots[target].occupied = True
        self.status_msg = f"Car parked in slot {target+1}."

    def retrieve_car(self, slot_num):
        if self.emergency or self.fault:
            self.status_msg = "Cannot retrieve: Emergency or Fault!"
            return
        if slot_num < 0 or slot_num >= self.num_slots or not self.slots[slot_num].occupied:
            self.status_msg = "Invalid or empty slot."
            return
        self.rotate_to_slot(slot_num)
        self.slots[slot_num].occupied = False
        self.status_msg = f"Car retrieved from slot {slot_num+1}."

    def rotate_to_slot(self, target_slot):
        while self.ground_slot != target_slot:
            if self.emergency or self.fault:
                self.status_msg = "Rotation stopped: Emergency or Fault!"
                return
            self.ground_slot = (self.ground_slot + 1) % self.num_slots
            time.sleep(0.3)

    def emergency_stop(self):
        self.emergency = True
        self.status_msg = "EMERGENCY STOP!"

    def reset_emergency(self):
        self.emergency = False
        self.status_msg = "Emergency reset. System Ready."

    def induce_fault(self):
        self.fault = True
        self.status_msg = "FAULT DETECTED!"

    def reset_fault(self):
        self.fault = False
        self.status_msg = "Fault reset. System Ready."

class ParkingHMI:
    def __init__(self, root, system: ParkingSystem):
        self.root = root
        self.system = system
        self.vars = {
            'slots': [tk.StringVar() for _ in range(system.num_slots)],
            'ground_slot': tk.StringVar(),
            'emergency': tk.StringVar(),
            'fault': tk.StringVar(),
            'status_msg': tk.StringVar()
        }
        self._build_gui()
        self._running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def _build_gui(self):
        self.root.title("Rotary Parking System HMI Simulation")
        frame_status = tk.LabelFrame(self.root, text="System Status", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_status.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        tk.Label(frame_status, textvariable=self.vars['status_msg'], font=("Arial", 12, "bold"), fg='blue').grid(row=0, column=0, columnspan=2, sticky='w')
        tk.Label(frame_status, text="Emergency:", font=("Arial", 11)).grid(row=1, column=0, sticky='e')
        tk.Label(frame_status, textvariable=self.vars['emergency'], font=("Arial", 11)).grid(row=1, column=1, sticky='w')
        tk.Label(frame_status, text="Fault:", font=("Arial", 11)).grid(row=2, column=0, sticky='e')
        tk.Label(frame_status, textvariable=self.vars['fault'], font=("Arial", 11)).grid(row=2, column=1, sticky='w')
        frame_slots = tk.LabelFrame(self.root, text="Parking Slots", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_slots.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        for i in range(self.system.num_slots):
            tk.Label(frame_slots, text=f"Slot {i+1}", font=("Arial", 11)).grid(row=i, column=0, sticky='e')
            tk.Label(frame_slots, textvariable=self.vars['slots'][i], font=("Arial", 11)).grid(row=i, column=1, sticky='w')
        tk.Label(frame_slots, text="At Ground:", font=("Arial", 11, "bold")).grid(row=self.system.num_slots, column=0, sticky='e')
        tk.Label(frame_slots, textvariable=self.vars['ground_slot'], font=("Arial", 11, "bold"), fg='green').grid(row=self.system.num_slots, column=1, sticky='w')
        frame_ctrl = tk.LabelFrame(self.root, text="Controls", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_ctrl.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        tk.Button(frame_ctrl, text="Park Car", width=12, command=self.park_car).grid(row=0, column=0, padx=5)
        tk.Button(frame_ctrl, text="Retrieve Car", width=12, command=self.retrieve_car).grid(row=0, column=1, padx=5)
        tk.Button(frame_ctrl, text="Emergency Stop", width=14, command=self.emergency_stop, bg='red', fg='white').grid(row=0, column=2, padx=5)
        tk.Button(frame_ctrl, text="Reset Emergency", width=14, command=self.reset_emergency).grid(row=0, column=3, padx=5)
        tk.Button(frame_ctrl, text="Induce Fault", width=12, command=self.induce_fault).grid(row=1, column=0, padx=5)
        tk.Button(frame_ctrl, text="Reset Fault", width=12, command=self.reset_fault).grid(row=1, column=1, padx=5)
        tk.Button(frame_ctrl, text="Quit", width=10, command=self.root.quit).grid(row=1, column=2, padx=5)

    def _run_loop(self):
        while self._running:
            self.update()
            time.sleep(0.5)

    def update(self):
        status = self.system.get_status()
        for i, occ in enumerate(status['slots']):
            txt = "Occupied" if occ else "Empty"
            if i == status['ground_slot']:
                txt += " (Ground)"
            self.vars['slots'][i].set(txt)
        self.vars['ground_slot'].set(f"Slot {status['ground_slot']+1}")
        self.vars['emergency'].set("YES" if status['emergency'] else "NO")
        self.vars['fault'].set("YES" if status['fault'] else "NO")
        self.vars['status_msg'].set(status['status_msg'])

    def park_car(self):
        threading.Thread(target=self.system.park_car, daemon=True).start()

    def retrieve_car(self):
        occ_slots = [i for i, s in enumerate(self.system.slots) if s.occupied]
        if not occ_slots:
            self.system.status_msg = "No cars to retrieve."
            return
        popup = tk.Toplevel(self.root)
        popup.title("Select Slot to Retrieve")
        tk.Label(popup, text="Occupied Slots:", font=("Arial", 11)).pack(pady=5)
        var = tk.IntVar()
        for i in occ_slots:
            tk.Radiobutton(popup, text=f"Slot {i+1}", variable=var, value=i, font=("Arial", 11)).pack(anchor='w')
        def do_retrieve():
            slot = var.get()
            popup.destroy()
            threading.Thread(target=self.system.retrieve_car, args=(slot,), daemon=True).start()
        tk.Button(popup, text="Retrieve", command=do_retrieve).pack(pady=5)

    def emergency_stop(self):
        self.system.emergency_stop()

    def reset_emergency(self):
        self.system.reset_emergency()

    def induce_fault(self):
        self.system.induce_fault()

    def reset_fault(self):
        self.system.reset_fault()

if __name__ == "__main__":
    root = tk.Tk()
    system = ParkingSystem(num_slots=5)
    gui = ParkingHMI(root, system)
    root.mainloop()
