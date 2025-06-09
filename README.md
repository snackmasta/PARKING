# Automatic Vending Machine Vertical Parking - PLC Project

This project implements a basic PLC logic for an automatic vending machine style vertical parking system. It includes:
- PLC logic for parking and retrieval
- Fault and safety handling
- Example HMI Python script (see `hmi.py`)

## Files
- `plc.st`: Main PLC program (Structured Text)
- `hmi.py`: Example HMI/Simulator script
- `docs/`: Documentation (architecture, control plan, etc.)

## How it works
- Detects cars at entry
- Finds available slot and parks car using lift and conveyor
- Handles retrieval requests
- Emergency stop and fault logic

---

See `docs/` for more details.
