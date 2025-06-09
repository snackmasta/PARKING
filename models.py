# models.py - Parking system data models and logic

import time
import math

class ParkingSlot:
    def __init__(self, slot_id):
        self.slot_id = slot_id
        self.occupied = False

class ParkingSystem:
    def __init__(self, num_slots=6):
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

    def park_car(self, draw_callback=None):
        if self.emergency or self.fault:
            self.status_msg = "Cannot park: Emergency or Fault!"
            print("[DEBUG] Parking aborted: Emergency or Fault!", flush=True)
            return
        n = self.num_slots
        empty_slots = [i for i, s in enumerate(self.slots) if not s.occupied]
        if not empty_slots:
            self.status_msg = "No empty slots. Parking Full!"
            print("[DEBUG] Parking aborted: No empty slots.", flush=True)
            return
        print(f"[DEBUG] Current ground slot: {self.ground_slot+1}", flush=True)
        print(f"[DEBUG] Empty slots: {[i+1 for i in empty_slots]}", flush=True)
        best_slot = None
        min_steps = None
        min_cw = None
        for slot in empty_slots:
            cw_steps = (slot - self.ground_slot) % n
            ccw_steps = (self.ground_slot - slot) % n
            steps = min(cw_steps, ccw_steps)
            print(f"[DEBUG] Slot {slot+1}: CW={cw_steps}, CCW={ccw_steps}, min={steps}", flush=True)
            if (min_steps is None or steps < min_steps or (steps == min_steps and cw_steps < min_cw)):
                min_steps = steps
                min_cw = cw_steps
                best_slot = slot
        print(f"[DEBUG] Selected slot: {best_slot+1} (steps={min_steps}, CW={min_cw})", flush=True)
        self.rotate_to_slot(best_slot, draw_callback)
        self.slots[best_slot].occupied = True
        self.status_msg = f"Car parked in slot {best_slot+1}."

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

    def rotate_to_slot(self, target_slot, draw_callback=None):
        n = self.num_slots
        cw_steps = (target_slot - self.ground_slot) % n
        ccw_steps = (self.ground_slot - target_slot) % n
        if cw_steps <= ccw_steps:
            step = 1
            steps = cw_steps
        else:
            step = -1
            steps = ccw_steps
        frames_per_slot = 8
        for _ in range(steps):
            for f in range(frames_per_slot):
                if self.emergency or self.fault:
                    self.status_msg = "Rotation stopped: Emergency or Fault!"
                    return
                frac = (self.ground_slot + step * (f+1)/frames_per_slot) % n
                if draw_callback:
                    draw_callback(frac)
                time.sleep(0.02)
            self.ground_slot = (self.ground_slot + step) % n
        if draw_callback:
            draw_callback()  # Final position

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
