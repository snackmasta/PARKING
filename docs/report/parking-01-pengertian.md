# 1. Pengertian Sistem PARKING

## 1.1 Definisi Umum

Sistem PARKING (Sistem Parkir Otomatis) adalah sistem simulasi terintegrasi yang dirancang untuk mempelajari dan memahami proses manajemen parkir otomatis dengan fokus pada integrasi teknologi sensor kendaraan, barrier gate, dan sistem monitoring slot parkir. Sistem ini merupakan platform pembelajaran yang menggabungkan prinsip-prinsip rekayasa sistem parkir dengan implementasi kontrol otomatis untuk memberikan pemahaman komprehensif tentang operasi sistem parkir modern yang terintegrasi dengan teknologi sensor dan kontrol.

## 1.2 Konsep Dasar Sistem Parkir Otomatis

Sistem Parkir Otomatis (PARKING) merupakan sistem terintegrasi yang menggabungkan aspek deteksi kendaraan, pengelolaan slot parkir, dan distribusi informasi secara efisien menggunakan konsep monitoring real-time. Fokus utama sistem ini adalah pada manajemen slot parkir yang optimal dengan memanfaatkan teknologi sensor kendaraan sebagai sumber data dan sistem display digital sebagai komponen kunci distribusi informasi.

Sensor kendaraan dalam konteks sistem PARKING berfungsi sebagai teknologi deteksi untuk menghasilkan data status slot parkir yang kemudian didistribusikan melalui sistem monitoring dan display yang terintegrasi. Teknologi sensor bekerja dengan mendeteksi keberadaan kendaraan pada slot parkir menggunakan metode ultrasonik, induktif, atau kamera.

Sistem display digital menjadi komponen strategis dalam distribusi informasi parkir karena memungkinkan penyampaian status slot secara efisien dan menyediakan informasi ketersediaan slot secara real-time tanpa ketergantungan pada pengecekan manual. Konsep dual display (utama dan area) memberikan fleksibilitas operasional dan redundansi dalam penyampaian informasi parkir.

## 1.3 Komponen Utama Sistem PARKING

### 1.3.1 Tahapan Proses Sistem PARKING

Sistem PARKING terdiri dari enam tahapan proses utama yang saling terintegrasi untuk mencapai manajemen parkir yang optimal:

- **Deteksi Kendaraan (Vehicle Detection)**: Tahap awal dimana kendaraan yang masuk dan keluar area parkir dideteksi menggunakan sensor kendaraan. Data sensor dikirim ke sistem kontrol untuk memastikan supply data yang memadai bagi proses monitoring.
- **Pra-proses (Pre-processing)**: Proses validasi awal untuk memastikan data sensor akurat dan bebas dari gangguan. Sistem melakukan filtering data untuk menghindari false detection.
- **Unit Kontrol Akses (Barrier Gate)**: Komponen pengendali akses kendaraan yang memastikan hanya kendaraan dengan validasi yang dapat masuk atau keluar. Barrier gate dikendalikan secara otomatis berdasarkan status slot parkir dan validasi tiket/kartu akses.
- **Pasca-proses (Post-processing)**: Tahap finalisasi data yang meliputi pencatatan waktu masuk/keluar dan update status slot parkir. Data ini diproses untuk keperluan pelaporan dan analisis.
- **Penyimpanan dan Distribusi Data Primer**: Database utama yang berfungsi sebagai buffer storage data hasil deteksi dan kontrol sebelum didistribusikan ke sistem display dan pelaporan.
- **Distribusi Sekunder dan Display Digital**: Sistem display digital mengalirkan informasi dari database ke area parkir dan pintu masuk/keluar yang menjadi komponen kunci distribusi informasi untuk melayani pengguna dengan status slot yang akurat dan efisien.

### 1.3.2 Sistem Kontrol dan Instrumentasi PARKING

Sistem PARKING menggunakan arsitektur kontrol otomatis yang dirancang khusus untuk mengoptimalkan manajemen parkir:

- **Sensor Network**: Sensor kendaraan dan slot parkir yang mengumpulkan data operasional secara real-time untuk monitoring parameter kritis seperti status slot, jumlah kendaraan, dan waktu parkir.
- **Control Logic**: Sistem kontrol berbasis PLC atau Python yang memproses data sensor dan mengimplementasikan algoritma kontrol untuk mengatur operasi barrier gate, display, dan alarm.
- **Human Machine Interface (HMI)**: Interface berbasis komputer atau touchscreen yang menyediakan visualisasi real-time status sistem parkir, kontrol manual barrier gate, dan monitoring slot parkir untuk operator.
