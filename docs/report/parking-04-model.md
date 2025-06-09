# 4. Model Sistem PARKING

## 4.1 Pendahuluan

Model sistem Parkir Otomatis (PARKING) merupakan representasi sistem simulasi yang menggambarkan proses dasar manajemen parkir otomatis menggunakan teknologi sensor, barrier gate, dan kontrol otomatis. Model ini dirancang sebagai platform pembelajaran dan demonstrasi untuk memahami prinsip-prinsip fundamental operasi sistem parkir otomatis dalam lingkungan terkontrol.

## 4.2 Komponen Utama Sistem PARKING

Sistem PARKING terdiri dari beberapa subsistem utama yang saling terintegrasi untuk membentuk proses manajemen parkir yang komprehensif dan otomatis.

### 4.2.1 Subsistem Deteksi Kendaraan

Subsistem deteksi kendaraan berfungsi sebagai titik masuk data kendaraan ke dalam sistem simulasi. Sensor kendaraan disimulasikan untuk mendeteksi keberadaan kendaraan pada slot parkir dan pintu masuk/keluar. Data sensor dikirim ke sistem kontrol untuk monitoring dan pengambilan keputusan.

### 4.2.2 Subsistem Kontrol Akses (Barrier Gate)

Tahap ini mengatur akses kendaraan masuk dan keluar area parkir. Barrier gate dikendalikan secara otomatis berdasarkan status slot parkir dan validasi tiket/kartu akses. Sensor posisi memastikan barrier beroperasi dengan aman.

### 4.2.3 Subsistem Monitoring Slot Parkir

Sistem monitoring slot parkir memantau status setiap slot secara real-time dan menampilkan informasi ketersediaan pada display digital. Data ini juga digunakan untuk analisis penggunaan lahan parkir.

### 4.2.4 Subsistem Manajemen Data Parkir

Data kendaraan, waktu masuk, dan keluar dicatat secara otomatis untuk keperluan pelaporan dan analisis. Sistem ini juga dapat terintegrasi dengan sistem pembayaran otomatis.

### 4.2.5 Subsistem Kontrol Otomatis

Subsistem kontrol menggunakan logika sederhana untuk mengkoordinasikan operasi dasar sistem parkir. Sistem kontrol berbasis PLC atau Python memproses sinyal dari sensor dan mengontrol aktuator berdasarkan algoritma yang telah diprogram. HMI menyediakan interface operator untuk monitoring dan kontrol manual.

## 4.3 Prinsip Operasi dan Integrasi Sistem

Sistem PARKING beroperasi secara terintegrasi dengan mengutamakan efisiensi, keamanan, dan kemudahan akses bagi pengguna dan operator.

## 4.4 Lampiran: Diagram Arsitektur dan Flowchart Sistem PARKING

### 4.4.1 Diagram Arsitektur Sistem PARKING

Diagram berikut menggambarkan arsitektur sistem rotary parking 6 slot:

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

### 4.4.2 Diagram System Architecture

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

### 4.4.3 Flowchart Proses dan Kontrol PARKING

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

### 4.4.4 Detailed Control Logic Flowchart

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

Penjelasan detail dan diagram lain dapat dilihat pada file architecture.md dan parking-flowchart.md.
