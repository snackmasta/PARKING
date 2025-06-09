# hmi.py - Example HMI/Simulator for Vertical Parking

# This is a placeholder for a Python script that could simulate or interface with the PLC logic.
# You can expand this with a simple CLI or GUI for testing.

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

    def display_status(self):
        print("\n--- Parking System Status ---")
        for i, slot in enumerate(self.slots):
            pos = "<-- Ground" if i == self.ground_slot else ""
            occ = "Occupied" if slot.occupied else "Empty"
            print(f"Slot {slot.slot_id}: {occ} {pos}")
        print(f"Emergency: {self.emergency}")
        print(f"Fault: {self.fault}")

    def rotate_to_slot(self, target_slot):
        print(f"Rotating to slot {target_slot+1}...")
        while self.ground_slot != target_slot:
            if self.emergency or self.fault:
                print("Rotation stopped due to emergency/fault.")
                return False
            self.ground_slot = (self.ground_slot + 1) % self.num_slots
            self.display_status()
            time.sleep(0.5)
        print(f"Slot {target_slot+1} is now at ground level.")
        return True

    def park_car(self):
        if self.emergency or self.fault:
            print("Cannot park: Emergency or fault active.")
            return
        empty_slots = [i for i, s in enumerate(self.slots) if not s.occupied]
        if not empty_slots:
            print("No empty slots available. Parking Full!")
            return
        target = empty_slots[0]
        if not self.rotate_to_slot(target):
            return
        input("Load car and press Enter...")
        self.slots[target].occupied = True
        print(f"Car parked in slot {target+1}.")

    def retrieve_car(self):
        if self.emergency or self.fault:
            print("Cannot retrieve: Emergency or fault active.")
            return
        occ_slots = [i for i, s in enumerate(self.slots) if s.occupied]
        if not occ_slots:
            print("No cars to retrieve.")
            return
        print("Occupied slots:", [s+1 for s in occ_slots])
        try:
            slot_num = int(input("Enter slot number to retrieve: "))
        except ValueError:
            print("Invalid input.")
            return
        if slot_num < 1 or slot_num > self.num_slots or not self.slots[slot_num-1].occupied:
            print("Invalid or empty slot selected.")
            return
        if not self.rotate_to_slot(slot_num-1):
            return
        input("Unload car and press Enter...")
        self.slots[slot_num-1].occupied = False
        print(f"Car retrieved from slot {slot_num}.")

    def emergency_stop(self):
        self.emergency = True
        print("EMERGENCY STOP ACTIVATED! All operations halted.")

    def reset_emergency(self):
        self.emergency = False
        print("Emergency reset. System ready.")

    def induce_fault(self):
        self.fault = True
        print("FAULT DETECTED! All operations halted.")

    def reset_fault(self):
        self.fault = False
        print("Fault reset. System ready.")


def main():
    system = ParkingSystem(num_slots=5)
    while True:
        system.display_status()
        print("\nOptions:")
        print("1. Park Car")
        print("2. Retrieve Car")
        print("3. Emergency Stop")
        print("4. Reset Emergency")
        print("5. Induce Fault")
        print("6. Reset Fault")
        print("0. Exit")
        choice = input("Select option: ")
        if choice == "1":
            system.park_car()
        elif choice == "2":
            system.retrieve_car()
        elif choice == "3":
            system.emergency_stop()
        elif choice == "4":
            system.reset_emergency()
        elif choice == "5":
            system.induce_fault()
        elif choice == "6":
            system.reset_fault()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option.")
        time.sleep(1)

if __name__ == "__main__":
    main()
