# gui.py - Contains the ParkingHMI class for the GUI
import tkinter as tk
import threading
import time
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ParkingHMI:
    def __init__(self, root, system):
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
        # --- Main container with two columns ---
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)

        # --- Left column: Main UI ---
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky='n')

        frame_status = tk.LabelFrame(left_frame, text="System Status", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_status.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        tk.Label(frame_status, textvariable=self.vars['status_msg'], font=("Arial", 12, "bold"), fg='blue').grid(row=0, column=0, columnspan=2, sticky='w')
        tk.Label(frame_status, text="Emergency:", font=("Arial", 11)).grid(row=1, column=0, sticky='e')
        tk.Label(frame_status, textvariable=self.vars['emergency'], font=("Arial", 11)).grid(row=1, column=1, sticky='w')
        tk.Label(frame_status, text="Fault:", font=("Arial", 11)).grid(row=2, column=0, sticky='e')
        tk.Label(frame_status, textvariable=self.vars['fault'], font=("Arial", 11)).grid(row=2, column=1, sticky='w')

        # --- Animation Viewfinder ---
        frame_anim = tk.LabelFrame(left_frame, text="Site Animation", padx=10, pady=10, font=("Arial", 11, "bold"))
        frame_anim.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.canvas = tk.Canvas(frame_anim, width=220, height=320, bg='white')
        self.canvas.grid(row=0, column=0)
        self._draw_site()

        frame_slots = tk.LabelFrame(left_frame, text="Parking Slots", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_slots.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        for i in range(self.system.num_slots):
            tk.Label(frame_slots, text=f"Slot {i+1}", font=("Arial", 11)).grid(row=i, column=0, sticky='e')
            tk.Label(frame_slots, textvariable=self.vars['slots'][i], font=("Arial", 11)).grid(row=i, column=1, sticky='w')
        tk.Label(frame_slots, text="At Ground:", font=("Arial", 11, "bold")).grid(row=self.system.num_slots, column=0, sticky='e')
        tk.Label(frame_slots, textvariable=self.vars['ground_slot'], font=("Arial", 11, "bold"), fg='green').grid(row=self.system.num_slots, column=1, sticky='w')

        # --- Controls ---
        frame_ctrl = tk.LabelFrame(left_frame, text="Controls", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_ctrl.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        tk.Button(frame_ctrl, text="Park Car", width=12, command=self.park_car).grid(row=0, column=0, padx=5)
        tk.Button(frame_ctrl, text="Retrieve Car", width=12, command=self.retrieve_car).grid(row=0, column=1, padx=5)
        tk.Button(frame_ctrl, text="Emergency Stop", width=14, command=self.emergency_stop, bg='red', fg='white').grid(row=0, column=2, padx=5)
        tk.Button(frame_ctrl, text="Reset Emergency", width=14, command=self.reset_emergency).grid(row=0, column=3, padx=5)
        tk.Button(frame_ctrl, text="Induce Fault", width=12, command=self.induce_fault).grid(row=1, column=0, padx=5)
        tk.Button(frame_ctrl, text="Reset Fault", width=12, command=self.reset_fault).grid(row=1, column=1, padx=5)
        tk.Button(frame_ctrl, text="Start System", width=12, command=self.start_system, bg='green', fg='white').grid(row=2, column=0, padx=5)
        tk.Button(frame_ctrl, text="Stop System", width=12, command=self.stop_system, bg='orange', fg='black').grid(row=2, column=1, padx=5)
        tk.Button(frame_ctrl, text="Quit", width=10, command=self.root.quit).grid(row=1, column=2, padx=5)

        # --- Retrieve Section ---
        self.frame_retrieve = tk.LabelFrame(left_frame, text="Retrieve Car", padx=10, pady=5, font=("Arial", 11, "bold"))
        self.frame_retrieve.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.retrieve_var = tk.IntVar()
        self.retrieve_dropdown = tk.OptionMenu(self.frame_retrieve, self.retrieve_var, "-")
        self.retrieve_dropdown.grid(row=0, column=0, padx=5)
        self.retrieve_btn = tk.Button(self.frame_retrieve, text="Confirm Retrieve", command=self.confirm_retrieve)
        self.retrieve_btn.grid(row=0, column=1, padx=5)
        self.update_retrieve_section()

        # --- Right column: Trend Graph ---
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky='ns', padx=(0,10), pady=10)
        frame_trend = tk.LabelFrame(right_frame, text="I/O Trend Graph", padx=10, pady=5, font=("Arial", 11, "bold"))
        frame_trend.pack(fill='both', expand=True)
        self.fig, (self.ax_sensor, self.ax_motor) = plt.subplots(2, 1, figsize=(5, 4), dpi=80, sharex=True, gridspec_kw={'height_ratios': [1, 1]})
        self.trend_canvas = FigureCanvasTkAgg(self.fig, master=frame_trend)
        self.trend_canvas.get_tk_widget().pack()
        self.trend_time = []
        self.trend_sensor = []
        self.trend_motor_deg = []
        self.trend_maxlen = 100
        self.trend_start_time = time.time()
        self._init_trend_plot()

    def update_retrieve_section(self):
        # Save current selection
        current_selection = self.retrieve_var.get()
        occ_slots = [i+1 for i, s in enumerate(self.system.slots) if s.occupied]
        # Only update menu if the set of occupied slots has changed
        if hasattr(self, '_last_occ_slots') and self._last_occ_slots == occ_slots:
            return
        self._last_occ_slots = occ_slots.copy()
        menu = self.retrieve_dropdown['menu']
        menu.delete(0, 'end')
        if occ_slots:
            for slot in occ_slots:
                menu.add_command(label=str(slot), command=lambda v=slot: self.retrieve_var.set(v))
            # Only set selection if current is not valid
            if current_selection in occ_slots:
                self.retrieve_var.set(current_selection)
            else:
                self.retrieve_var.set(occ_slots[0])
            self.retrieve_btn.config(state='normal')
        else:
            menu.add_command(label="-", command=lambda: self.retrieve_var.set(0))
            self.retrieve_var.set(0)
            self.retrieve_btn.config(state='disabled')

    def start_system(self):
        if self.system.emergency:
            self.system.status_msg = "Cannot start: Emergency Stop is active! Press Reset Emergency."
            return
        self.system.stopped = False
        self.system.status_msg = "System Started. Ready."

    def stop_system(self):
        self.system.stopped = True
        self.system.status_msg = "System Stopped."

    def park_car(self):
        def do_park():
            if getattr(self.system, 'stopped', False):
                self.system.status_msg = "Cannot park: System is stopped!"
                return
            self.system.park_car(draw_callback=self._draw_site)
        threading.Thread(target=do_park, daemon=True).start()

    def retrieve_car(self):
        if getattr(self.system, 'stopped', False):
            self.system.status_msg = "Cannot retrieve: System is stopped!"
            return
        occ_slots = [i for i, s in enumerate(self.system.slots) if s.occupied]
        if not occ_slots:
            self.system.status_msg = "No cars to retrieve."
            self.update_retrieve_section()
            return
        self.update_retrieve_section()
        self.system.status_msg = "Select a slot and press Confirm Retrieve."

    def confirm_retrieve(self):
        slot = self.retrieve_var.get() - 1
        if slot < 0 or slot >= self.system.num_slots or not self.system.slots[slot].occupied:
            self.system.status_msg = "Invalid or empty slot."
            return
        def retrieve():
            self.system.rotate_to_slot(slot, self._draw_site)
            self.system.slots[slot].occupied = False
            self.system.status_msg = f"Car retrieved from slot {slot+1}."
            self.update_retrieve_section()
        threading.Thread(target=retrieve, daemon=True).start()

    def emergency_stop(self):
        self.system.emergency_stop()

    def reset_emergency(self):
        self.system.reset_emergency()

    def induce_fault(self):
        self.system.induce_fault()

    def reset_fault(self):
        self.system.reset_fault()

    def _init_trend_plot(self):
        self.ax_sensor.clear()
        self.ax_motor.clear()
        self.ax_sensor.set_title('Sensor (Car at Ground)')
        self.ax_sensor.set_ylabel('Detected')
        self.ax_sensor.set_ylim(-0.1, 1.1)
        self.ax_sensor.grid(True)
        self.sensor_line, = self.ax_sensor.plot([], [], label='Sensor', color='blue', drawstyle='steps-post')
        self.ax_sensor.legend(loc='upper right')
        self.ax_motor.set_title('Motor Output (Platform Angle)')
        self.ax_motor.set_ylabel('Angle (deg)')
        self.ax_motor.set_ylim(-10, 370)
        self.ax_motor.set_xlabel('Time (s)')
        self.ax_motor.grid(True)
        self.motor_line, = self.ax_motor.plot([], [], label='Angle', color='orange')
        self.ax_motor.legend(loc='upper right')
        self.fig.tight_layout()
        self.trend_canvas.draw()

    def _update_trend_plot(self, sensor_val, motor_deg):
        t = time.time() - self.trend_start_time
        self.trend_time.append(t)
        self.trend_sensor.append(sensor_val)
        self.trend_motor_deg.append(motor_deg)
        # Keep only the last N points
        if len(self.trend_time) > self.trend_maxlen:
            self.trend_time = self.trend_time[-self.trend_maxlen:]
            self.trend_sensor = self.trend_sensor[-self.trend_maxlen:]
            self.trend_motor_deg = self.trend_motor_deg[-self.trend_maxlen:]
        self.sensor_line.set_data(self.trend_time, self.trend_sensor)
        self.motor_line.set_data(self.trend_time, self.trend_motor_deg)
        self.ax_sensor.set_xlim(max(0, self.trend_time[0] if self.trend_time else 0), max(10, self.trend_time[-1] if self.trend_time else 10))
        self.ax_motor.set_xlim(self.ax_sensor.get_xlim())
        self.trend_canvas.draw()

    def _draw_site(self, anim_ground_slot=None):
        self.canvas.delete('all')
        cx, cy = 110, 160
        r = 100
        slot_r = 30
        n = self.system.num_slots
        angle_step = 360 / n
        ground_pos = anim_ground_slot if anim_ground_slot is not None else self.system.ground_slot
        for i in range(n):
            rel_idx = (i - ground_pos) % n
            angle = (90 + angle_step * rel_idx) * math.pi / 180
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            fill = 'gray' if self.system.slots[i].occupied else 'white'
            outline = 'green' if int(round(ground_pos)) % n == i else 'black'
            self.canvas.create_rectangle(x-slot_r, y-slot_r, x+slot_r, y+slot_r, fill=fill, outline=outline, width=3)
            self.canvas.create_text(x, y, text=str(i+1), font=("Arial", 16, "bold"))
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline='blue', width=4)
        self.canvas.create_rectangle(cx-40, cy+100, cx+40, cy+120, fill='tan', outline='brown', width=3)
        self.canvas.create_text(cx, cy+110, text='Ground', font=("Arial", 12, "bold"))

    def _run_loop(self):
        while self._running:
            self.update()
            self._draw_site()
            # Sensor: car detected at ground (digital)
            sensor_val = 1.0 if any(not s.occupied and i == self.system.ground_slot for i, s in enumerate(self.system.slots)) else 0.0
            # Motor: current platform angle in degrees
            motor_deg = (self.system.ground_slot * 360.0) / self.system.num_slots
            self._update_trend_plot(sensor_val, motor_deg)
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
        self.update_retrieve_section()
