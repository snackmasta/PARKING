# Control Plan

## Parking Sequence
1. Detect car at entry
2. Find first available slot
3. Move lift to slot level
4. Open door
5. Move car in with conveyor
6. Mark slot as occupied

## Retrieval Sequence
1. User requests retrieval (specifies slot)
2. Move lift to slot level
3. Open door
4. Move car out with conveyor
5. Mark slot as empty

## Fault Handling
- Emergency stop disables all actuators
- Faults shut down all outputs
