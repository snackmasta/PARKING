# 2. Ruang Lingkup Sistem PARKING

## 2.1 Pendahuluan

Ruang lingkup sistem Parkir Otomatis (PARKING) mencakup semua aspek sistem yang dirancang untuk mengelola area parkir secara otomatis dan efisien. Dokumen ini menjelaskan batasan sistem secara detail, meliputi komponen fisik, operasional, dan kontrol yang tergabung dalam satu sistem manajemen parkir.

Pentingnya mendefinisikan ruang lingkup sistem secara jelas adalah untuk memastikan semua pihak memiliki pemahaman yang sama tentang cakupan proyek, tanggung jawab masing-masing bagian sistem, dan hubungan dengan sistem luar. Ruang lingkup yang jelas akan mengurangi ketidakjelasan dalam pelaksanaan dan memudahkan proses perawatan serta pemecahan masalah.

## 2.2 Definisi Ruang Lingkup Sistem

Ruang lingkup sistem PARKING meliputi seluruh proses, mulai dari deteksi kendaraan, praolah (validasi sensor), proses utama (kontrol akses dan monitoring slot), pascaolah (pencatatan data dan pelaporan), penyimpanan data, hingga distribusi informasi kepada pengguna. Selain itu, ruang lingkup juga mencakup sistem kontrol otomatis (PLC/HMI), pemantauan parameter sistem, alarm, serta integrasi dengan sistem pembayaran atau utilitas lain apabila diperlukan.

### 2.2.1 Cakupan Fungsional Sistem

Sistem PARKING dirancang untuk beroperasi sebagai instalasi manajemen parkir terpadu dengan kemampuan:
- **Otomasi proses**: Kontrol otomatis seluruh tahapan proses parkir
- **Jaminan ketersediaan**: Monitoring status slot parkir secara terus-menerus
- **Optimisasi efisiensi**: Mengoptimalkan penggunaan lahan dan waktu parkir
- **Manajemen keamanan**: Sistem keamanan dan proteksi kendaraan
- **Manajemen data**: Pengumpulan, analisis, dan pelaporan data operasional parkir

## 2.3 Komponen Utama Ruang Lingkup Sistem

Sistem PARKING terdiri dari beberapa bagian utama yang saling terhubung untuk membentuk proses manajemen parkir yang lengkap dan otomatis. Setiap bagian memiliki fungsi khusus dan berinteraksi dengan bagian lain melalui sistem kontrol terpusat.

### 2.3.1 Bagian Deteksi Kendaraan

Bagian deteksi kendaraan berfungsi sebagai titik awal masuknya kendaraan ke dalam sistem parkir dan merupakan tahap awal yang penting dalam proses manajemen parkir.

#### a) Komponen Utama Deteksi
- **Sensor Kendaraan**: Sensor ultrasonik atau induktif untuk mendeteksi keberadaan kendaraan pada slot parkir
- **Display Digital**: Menampilkan status ketersediaan slot parkir
- **Barrier Gate**: Mengatur akses masuk dan keluar kendaraan
- **Sistem Kontrol**: PLC atau komputer industri untuk mengelola logika kontrol dan komunikasi antar perangkat

### 2.3.2 Bagian Praolah

Bagian praolah bertugas untuk memvalidasi dan memproses data yang diterima dari sensor kendaraan sebelum diteruskan ke sistem kontrol utama.

#### a) Komponen Utama Praolah
- **Unit Pemrosesan Sinyal**: Mengolah sinyal dari sensor kendaraan
- **Modul Komunikasi**: Mengirimkan data yang telah diproses ke sistem kontrol utama
- **Sistem Cadangan Daya**: Menjamin kelangsungan operasional praolah saat terjadi gangguan listrik

### 2.3.3 Bagian Proses Utama

Bagian proses utama mengelola kontrol akses kendaraan dan monitoring slot parkir secara real-time.

#### a) Komponen Utama Proses
- **Kontrol Akses**: Mengelola buka/tutupnya barrier gate
- **Monitoring Slot**: Memantau dan memperbarui status ketersediaan slot parkir
- **Sistem Peringatan Dini**: Memberikan alarm atau notifikasi jika terjadi masalah pada sistem

### 2.3.4 Bagian Pascaolah

Bagian pascaolah bertanggung jawab untuk pencatatan data, pelaporan, dan distribusi informasi kepada pengguna.

#### a) Komponen Utama Pascaolah
- **Database**: Menyimpan seluruh data transaksi dan status parkir
- **Modul Pelaporan**: Menghasilkan laporan berkala mengenai aktivitas dan penggunaan sistem parkir
- **Antarmuka Pengguna**: Menyediakan informasi dan menerima masukan dari pengguna sistem

## 2.4 Batasan Ruang Lingkup Sistem

Beberapa hal yang menjadi batasan dalam ruang lingkup sistem PARKING antara lain:
- Sistem ini hanya untuk pengelolaan area parkir yang telah ditentukan
- Tidak mencakup pengelolaan kendaraan di luar area parkir
- Integrasi dengan sistem lain hanya sebatas yang telah ditentukan dalam spesifikasi
- Perawatan dan pemeliharaan sistem menjadi tanggung jawab pihak tertentu sesuai kesepakatan

Dengan mendefinisikan ruang lingkup sistem PARKING secara jelas, diharapkan pengembangan dan implementasi sistem ini dapat berjalan dengan lancar, sesuai dengan tujuan dan harapan yang telah ditetapkan.
