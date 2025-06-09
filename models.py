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
