# Architecture

```mermaid
flowchart TD
    Ground([Ground Level])
    S1([Slot 1])
    S2([Slot 2])
    S3([Slot 3])
    S4([Slot 4])
    S5([Slot 5])
    S6([Slot 6])

    Ground --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> Ground
```

- Vertical rotary parking system with 6 slots arranged in a loop
- Cars are loaded/unloaded at the ground level
- Mechanism rotates to bring the desired slot to ground
- Sensors detect slot occupancy and position
- PLC controls rotation and slot selection

# Control Plan
- On car detection at ground, rotate to empty slot, load car
- On retrieval request, rotate to requested slot, unload car
- Emergency stop disables all outputs

# Hardware Spec
- 6 slot sensors
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

# Detailed Control Logic (Step-by-Step)

1. **System Initialization**
   - Initialize all sensors and actuators.
   - Ensure rotary motor is stopped and system is in safe state.
   - Check all slots and position sensors for status.

2. **Idle/Waiting State**
   - Continuously monitor for car detection at ground level or retrieval request from user interface.
   - Monitor emergency stop at all times.

3. **Parking Sequence**
   - On car detection at ground level:
     1. Scan all slot sensors to find the first available (empty) slot.
     2. If no slot is available, display "Full" on HMI and return to idle.
     3. If a slot is available, determine the shortest rotation direction (clockwise/counterclockwise) to bring the empty slot to ground.
     4. Activate rotary motor in the chosen direction.
     5. Use position sensors to stop rotation when the empty slot aligns with ground level.
     6. Confirm slot is at ground and empty, then signal user to load car.
     7. Wait for car to be loaded (can use a load sensor or user confirmation button).
     8. Mark slot as occupied, update HMI, and return to idle.

4. **Retrieval Sequence**
   - On retrieval request (user selects slot):
     1. Check if requested slot is occupied.
     2. If not occupied, display error on HMI and return to idle.
     3. If occupied, determine shortest rotation direction to bring requested slot to ground.
     4. Activate rotary motor in the chosen direction.
     5. Use position sensors to stop rotation when requested slot aligns with ground level.
     6. Signal user to unload car.
     7. Wait for car to be removed (can use a load sensor or user confirmation button).
     8. Mark slot as empty, update HMI, and return to idle.

5. **Emergency Stop Handling**
   - At any time, if emergency stop is pressed:
     1. Immediately cut power to rotary motor and halt all movement.
     2. Display emergency message on HMI.
     3. Wait for manual reset before resuming operation.

6. **Fault Handling**
   - Monitor for sensor or actuator faults (e.g., sensor stuck, motor overload).
   - If a fault is detected, stop all operations, display fault on HMI, and require maintenance intervention.

7. **Manual Override (Optional)**
   - Allow maintenance personnel to manually rotate or access slots for service, with safety interlocks.

# Detailed Control Logic Flowchart

```mermaid
%%{init: { 'layout': 'elk', 'theme': 'base' }}%%
flowchart TD
    START([Start])
    STOP([Stop])
    INIT([System Initialization])
    IDLE([Idle/Waiting])
    EMGSTOP{Emergency Stop?}
    FAULT{Fault Detected?}
    CAR_DET{Car Detected at Ground?}
    RETR_REQ{Retrieval Request?}
    FIND_EMPTY([Find Empty Slot])
    SLOT_AVAIL{Slot Available?}
    DISP_FULL([Display 'Full' on HMI])
    ROTATE_EMPTY([Rotate to Empty Slot])
    ALIGN_EMPTY([Align Empty Slot to Ground])
    SIGNAL_LOAD([Signal User to Load Car])
    WAIT_LOAD([Wait for Car to be Loaded])
    MARK_OCC([Mark Slot as Occupied])
    FIND_SLOT([Find Requested Slot])
    SLOT_OCC{Slot Occupied?}
    DISP_ERR([Display Error on HMI])
    ROTATE_SLOT([Rotate to Requested Slot])
    ALIGN_SLOT([Align Requested Slot to Ground])
    SIGNAL_UNLOAD([Signal User to Unload Car])
    WAIT_UNLOAD([Wait for Car to be Removed])
    MARK_EMPTY([Mark Slot as Empty])
    STOP_MOTOR([Stop Rotary Motor])
    DISP_EMG([Display Emergency on HMI])
    WAIT_RESET([Wait for Manual Reset])
    DISP_FAULT([Display Fault on HMI])
    WAIT_MAINT([Wait for Maintenance])

    START --> INIT
    INIT --> IDLE
    IDLE --> EMGSTOP
    EMGSTOP -- Yes --> STOP_MOTOR --> DISP_EMG --> WAIT_RESET --> INIT
    EMGSTOP -- No --> FAULT
    FAULT -- Yes --> STOP_MOTOR --> DISP_FAULT --> WAIT_MAINT --> INIT
    FAULT -- No --> CAR_DET
    CAR_DET -- Yes --> FIND_EMPTY
    CAR_DET -- No --> RETR_REQ
    FIND_EMPTY --> SLOT_AVAIL
    SLOT_AVAIL -- No --> DISP_FULL --> IDLE
    SLOT_AVAIL -- Yes --> ROTATE_EMPTY --> ALIGN_EMPTY --> SIGNAL_LOAD --> WAIT_LOAD --> MARK_OCC --> IDLE
    RETR_REQ -- Yes --> FIND_SLOT
    RETR_REQ -- No --> IDLE
    FIND_SLOT --> SLOT_OCC
    SLOT_OCC -- No --> DISP_ERR --> IDLE
    SLOT_OCC -- Yes --> ROTATE_SLOT --> ALIGN_SLOT --> SIGNAL_UNLOAD --> WAIT_UNLOAD --> MARK_EMPTY --> IDLE
    %% Add STOP transition for system shutdown (e.g., after WAIT_MAINT or WAIT_RESET if desired)
    WAIT_MAINT --> STOP
    WAIT_RESET --> STOP
    style START fill:#b6fcb6,stroke:#2e8b57,stroke-width:3px
    style STOP fill:#ffb3b3,stroke:#c0392b,stroke-width:3px
```
