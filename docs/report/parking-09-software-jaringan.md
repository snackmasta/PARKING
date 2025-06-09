# 9. Perangkat Lunak Jaringan Kendali PARKING

Perangkat lunak jaringan kendali PARKING terdiri dari:
- **PLC Program**: Logika kontrol utama (Structured Text/ladder) untuk mengatur urutan operasi, safety, dan fault handling pada sistem parkir.
- **HMI/SCADA**: Antarmuka operator berbasis software (misal: Python Tkinter, WinCC, Wonderware) untuk monitoring status slot parkir, alarm, dan kontrol manual barrier gate.
- **Komunikasi**: Protokol komunikasi industri (Modbus, Ethernet/IP) untuk pertukaran data antara PLC, HMI, dan perangkat lain.
- **Simulasi**: Program simulasi (misal: Python) untuk pengujian logika dan visualisasi proses sebelum implementasi fisik.
- **Data Logging**: Fitur pencatatan data kendaraan, waktu masuk/keluar, dan status slot untuk analisis dan troubleshooting.

## 9.1 Lampiran: Control System Plan and I/O Table

### 9.1.1 Control Philosophy
- The system is fully automated with manual override for all barrier gates and display.
- Main control logic is based on vehicle detection, slot status, and access validation.
- Alarms are generated for abnormal conditions (slot full, barrier error, sensor failure, etc.).
- All critical parameters are monitored and logged.
- Local HMI/SCADA for operator interface; remote monitoring optional.
- **Architecture Update:** The system now uses a modular process and control architecture, with clear separation of sensors, logic, and actuators as shown in the updated flowcharts. PLC/SCADA or software logic group handles all process decisions and actuator commands.

### 9.1.2 Main Control Logic
- **Vehicle Detection**: Sensor triggers when a vehicle enters or exits, updating slot status and display.
- **Barrier Gate**: Opens if slot available and access valid, closes after vehicle passes or on error.
- **Display Update**: Real-time update of slot availability and system status.
- **Alarms**: Any abnormal sensor reading or device error triggers alarm and can stop relevant equipment.
- **Architecture Update:** Logic is now explicitly mapped from sensors to logic functions to actuators, as per the new flowcharts. All sensor values are routed to a central logic group (PLC or software), which then controls actuators.

### 9.1.3 I/O Table
| Tag/Name                | Type      | Description                                 | Location                | PLC Variable    | HMI Display |
|-------------------------|-----------|---------------------------------------------|-------------------------|-----------------|-------------|
| SENSOR-01               | DI        | Sensor Kendaraan Masuk                      | Pintu Masuk             | SENSOR_01       | masuk       |
| SENSOR-02               | DI        | Sensor Kendaraan Keluar                     | Pintu Keluar            | SENSOR_02       | keluar      |
| SLOT-01 ... SLOT-N      | DI        | Sensor Slot Parkir                          | Setiap Slot             | SLOT_01 ... N   | slot        |
| BARRIER-IN              | DO        | Barrier Gate Masuk Start/Stop               | Pintu Masuk             | BARRIER_IN      | barrier-in  |
| BARRIER-OUT             | DO        | Barrier Gate Keluar Start/Stop              | Pintu Keluar            | BARRIER_OUT     | barrier-out |
| DISPLAY                 | DO        | Display Digital Update                      | Area Parkir             | DISPLAY         | display     |
| ALARM                   | DO        | Alarm Aktif/Nonaktif                        | Panel Kontrol           | ALARM           | alarm       |
