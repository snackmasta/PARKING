# 3. Elemen Dasar dan Jaringan Sistem PARKING

## 3.1 Pendahuluan

Sistem Parkir Otomatis (PARKING) merupakan sistem kompleks yang terdiri dari berbagai komponen yang saling terintegrasi. Pemahaman tentang elemen dasar dan arsitektur jaringan sistem ini sangat penting untuk merancang sistem yang efisien, handal, dan mudah dioperasikan. Bab ini akan menguraikan komponen-komponen fundamental sistem PARKING serta topologi jaringan yang menghubungkan seluruh elemen sistem.

## 3.2 Elemen Dasar Sistem PARKING

### 3.2.1 Sistem Sensor dan Aktuator

Sistem sensor dan aktuator merupakan mata dan tangan dari sistem PARKING yang bertugas mengumpulkan data operasional dan mengatur perangkat secara real-time.

#### a) Sensor Kendaraan
- **Fungsi**: Mendeteksi keberadaan kendaraan pada slot parkir dan pintu masuk/keluar
- **Teknologi**: Ultrasonik, induktif, atau kamera
- **Output signal**: Digital (on/off) atau komunikasi Modbus

#### b) Display Digital
- **Fungsi**: Menampilkan status ketersediaan slot parkir
- **Jenis**: LED display atau LCD
- **Aplikasi**: Informasi jumlah slot kosong, arah parkir, dan status gate

#### c) Barrier Gate
- **Fungsi**: Mengatur akses masuk dan keluar kendaraan
- **Teknologi**: Motorized gate dengan sensor posisi
- **Kontrol**: Otomatis via PLC atau manual via HMI

#### d) Sistem Kontrol
- **Fungsi**: Mengelola logika kontrol, komunikasi antar perangkat, dan alarm
- **Platform**: PLC, komputer industri, atau mikrokontroler
- **Komunikasi**: Modbus, Ethernet, atau wireless

#### e) HMI (Human Machine Interface)
- **Fungsi**: Menyediakan antarmuka visual untuk operator
- **Teknologi**: Touchscreen, komputer, atau aplikasi mobile
- **Aplikasi**: Monitoring status sistem, kontrol manual, dan pelaporan
