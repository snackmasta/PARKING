# 8. Perangkat Keras Kendali Utilitas Dalam Sistem PARKING

Perangkat keras utama pada sistem PARKING (Automated Parking System) meliputi:
- **PLC (Programmable Logic Controller)**: Mengendalikan seluruh proses otomatisasi manajemen parkir. PLC yang digunakan dapat tipe Siemens S7-1200 atau setara, mendukung komunikasi Modbus/TCP dan integrasi HMI.
- **Sensor Kendaraan**: Sensor ultrasonik, induktif, atau kamera untuk mendeteksi keberadaan kendaraan pada slot parkir dan pintu masuk/keluar.
- **Display Digital**: LED display atau LCD untuk menampilkan status ketersediaan slot parkir dan informasi kepada pengguna.
- **Barrier Gate**: Motorized gate dengan sensor posisi untuk mengatur akses masuk dan keluar kendaraan secara otomatis.
- **Alarm (ALM-101)**: Sirine dan lampu indikator untuk memberikan peringatan kondisi abnormal (misal: slot penuh, barrier error, sensor rusak).
- **Panel Kontrol**: Panel berbahan mild steel IP54, berisi PLC, relay, terminal, proteksi, dan HMI touchscreen 7 inci.

---

## 8.1 Tabel Ringkasan Spesifikasi Perangkat Keras

| Perangkat         | Tipe/Model         | Fungsi Utama                        | Lokasi Pemasangan         |
|------------------|--------------------|-------------------------------------|--------------------------|
| PLC              | Siemens S7-1200    | Otomasi & kendali proses            | Panel Kontrol            |
| Sensor Kendaraan | Ultrasonik/Induktif| Deteksi kendaraan                   | Slot Parkir/Pintu Masuk  |
| Display Digital  | LED/LCD            | Informasi slot parkir               | Area Parkir              |
| Barrier Gate     | Motorized AC 220V  | Kontrol akses kendaraan             | Pintu Masuk/Keluar       |
| Alarm            | Sirine + Lampu     | Indikasi kondisi abnormal           | Panel Kontrol            |
| Panel Kontrol    | Mild Steel IP54    | Integrasi & proteksi sistem         | Ruang Panel              |

---

## 8.2 Lampiran: Spesifikasi Hardware Sistem PARKING

(Lihat detail pada dokumen hardware-spec.md untuk spesifikasi lengkap sensor, barrier gate, display, dan panel kontrol yang digunakan pada sistem PARKING.)

---

*Catatan: Semua perangkat keras di atas telah diintegrasikan dan dikendalikan secara otomatis melalui PLC dan HMI sesuai dengan dokumentasi dan program pada project ini.*
