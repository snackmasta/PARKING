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

# Control Logic Flowchart

```mermaid
flowchart TD
    Start([Start])
    CarDetected{Car Detected at Ground?}
    Emergency{Emergency Stop?}
    FindEmpty{Find Empty Slot}
    RotateToEmpty{Rotate to Empty Slot}
    LoadCar{Load Car}
    Parked([Car Parked])
    RetrieveReq{Retrieval Request?}
    FindSlot{Find Requested Slot}
    RotateToSlot{Rotate to Requested Slot}
    UnloadCar{Unload Car}
    Retrieved([Car Retrieved])
    Shutdown([Shutdown All Outputs])
    Wait([Wait/Idle])

    Start --> Emergency
    Emergency -- Yes --> Shutdown
    Emergency -- No --> CarDetected
    CarDetected -- Yes --> FindEmpty
    CarDetected -- No --> RetrieveReq
    FindEmpty --> RotateToEmpty
    RotateToEmpty --> LoadCar
    LoadCar --> Parked
    Parked --> Wait
    RetrieveReq -- Yes --> FindSlot
    RetrieveReq -- No --> Wait
    FindSlot --> RotateToSlot
    RotateToSlot --> UnloadCar
    UnloadCar --> Retrieved
    Retrieved --> Wait
    Wait --> Emergency
```

# Hardware Spec
- 5 slot sensors
- 1 position sensor per slot
- 1 car detection sensor
- 1 emergency stop
- 1 rotary motor

# System Architecture

```mermaid
flowchart LR
    subgraph User Interface
        UI[HMI / Push Buttons]
    end
    subgraph PLC System
        PLC[PLC Controller]
    end
    subgraph Sensors
        SSlot[Slot Sensors]
        SPos[Position Sensors]
        SCar[Car Detection Sensor]
        SEStop[Emergency Stop]
    end
    subgraph Actuators
        Motor[Rotary Motor]
    end

    UI -- requests/commands --> PLC
    SSlot -- slot status --> PLC
    SPos -- position status --> PLC
    SCar -- car present --> PLC
    SEStop -- emergency --> PLC
    PLC -- control --> Motor
```
