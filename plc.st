(* plc.st - Main PLC Program for Automatic Vending Machine Vertical Parking *)

PROGRAM VerticalParking_Control
VAR
    (* Sensors and Inputs *)
    CarDetected      : BOOL;   (* Car present at entry *)
    SlotSensors      : ARRAY[1..10] OF BOOL;  (* Slot occupancy sensors for 10 slots *)
    RequestRetrieve  : BOOL;   (* User requests car retrieval *)
    RequestedSlot    : INT;    (* Slot number requested for retrieval *)
    EmergencyStop    : BOOL;   (* Emergency stop button *)

    (* Actuators and Outputs *)
    LiftUp           : BOOL;   (* Lift motor up *)
    LiftDown         : BOOL;   (* Lift motor down *)
    LiftAtLevel      : ARRAY[1..10] OF BOOL;  (* Lift at each slot level *)
    ConveyorIn       : BOOL;   (* Conveyor to move car in *)
    ConveyorOut      : BOOL;   (* Conveyor to move car out *)
    DoorOpen         : BOOL;   (* Entry/exit door open *)

    (* Internal Variables *)
    CurrentLevel     : INT := 1;   (* Current lift level *)
    ParkingInProcess : BOOL := FALSE;
    RetrievalInProcess : BOOL := FALSE;
    Fault            : BOOL := FALSE;
END_VAR

(* System Startup and Initialization *)
IF EmergencyStop THEN
    Fault := TRUE;
    LiftUp := FALSE;
    LiftDown := FALSE;
    ConveyorIn := FALSE;
    ConveyorOut := FALSE;
    DoorOpen := FALSE;
END_IF;

(* Parking Logic *)
IF CarDetected AND NOT ParkingInProcess AND NOT Fault THEN
    (* Find first available slot *)
    FOR i := 1 TO 10 DO
        IF NOT SlotSensors[i] THEN
            ParkingInProcess := TRUE;
            (* Move lift to slot level *)
            IF CurrentLevel < i THEN
                LiftUp := TRUE;
                LiftDown := FALSE;
            ELSIF CurrentLevel > i THEN
                LiftUp := FALSE;
                LiftDown := TRUE;
            ELSE
                LiftUp := FALSE;
                LiftDown := FALSE;
                (* Open door and move car in *)
                DoorOpen := TRUE;
                ConveyorIn := TRUE;
                (* Assume car is parked after some time, set SlotSensors[i] := TRUE externally *)
                ParkingInProcess := FALSE;
                DoorOpen := FALSE;
                ConveyorIn := FALSE;
                CurrentLevel := i;
            END_IF;
            EXIT;
        END_IF;
    END_FOR;
END_IF;

(* Retrieval Logic *)
IF RequestRetrieve AND NOT RetrievalInProcess AND NOT Fault THEN
    RetrievalInProcess := TRUE;
    (* Move lift to requested slot *)
    IF CurrentLevel < RequestedSlot THEN
        LiftUp := TRUE;
        LiftDown := FALSE;
    ELSIF CurrentLevel > RequestedSlot THEN
        LiftUp := FALSE;
        LiftDown := TRUE;
    ELSE
        LiftUp := FALSE;
        LiftDown := FALSE;
        (* Open door and move car out *)
        DoorOpen := TRUE;
        ConveyorOut := TRUE;
        (* Assume car is retrieved after some time, set SlotSensors[RequestedSlot] := FALSE externally *)
        RetrievalInProcess := FALSE;
        DoorOpen := FALSE;
        ConveyorOut := FALSE;
        CurrentLevel := RequestedSlot;
    END_IF;
END_IF;

(* Safety and Fault Handling *)
IF Fault THEN
    (* Shut down all outputs *)
    LiftUp := FALSE;
    LiftDown := FALSE;
    ConveyorIn := FALSE;
    ConveyorOut := FALSE;
    DoorOpen := FALSE;
END_IF;

END_PROGRAM
