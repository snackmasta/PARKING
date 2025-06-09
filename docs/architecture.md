# Architecture

```mermaid
flowchart TD
    Ground([Ground Level])
    S1([Slot 1])
    S2([Slot 2])
    S3([Slot 3])
    S4([Slot 4])
    S5([Slot 5])

    Ground --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> Ground
```

- Vertical rotary parking system with 5 slots arranged in a loop
- Cars are loaded/unloaded at the ground level
- Mechanism rotates to bring the desired slot to ground
- Sensors detect slot occupancy and position
- PLC controls rotation and slot selection

# Control Plan
- On car detection at ground, rotate to empty slot, load car
- On retrieval request, rotate to requested slot, unload car
- Emergency stop disables all outputs

# Hardware Spec
- 5 slot sensors
- 1 position sensor per slot
- 1 car detection sensor
- 1 emergency stop
- 1 rotary motor
