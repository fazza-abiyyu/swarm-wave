# Swarm Wave Backend Documentation

Dokumentasi ini menjelaskan struktur, fungsi, dan alur kerja dari backend Swarm Wave, sebuah sistem Multi-Agent Task Scheduling berbasis Swarm Intelligence.

## 1. Penjelasan Umum

**Swarm Wave Backend** adalah API server yang dibangun menggunakan **Flask (Python)**. Tujuan utamanya adalah menyelesaikan masalah penjadwalan tugas (Task Scheduling) yang kompleks menggunakan algoritma optimasi berbasis alam, yaitu:
*   **Ant Colony Optimization (ACO)**: Meniru perilaku semut mencari jalur terpendek.
*   **Particle Swarm Optimization (PSO)**: Meniru perilaku kawanan burung mencari sumber makanan.

Sistem ini dirancang untuk:
*   Menerima daftar tugas (tasks) dan agen (agents).
*   Mencari pembagian tugas ke agen yang paling optimal (waktu terpendek & beban seimbang).
*   Memberikan hasil secara **real-time** (streaming) kepada pengguna saat algoritma sedang bekerja.

## 2. Cara Kerja Detail

Sistem ini tidak sekadar "terima data -> proses -> kirim hasil". Ia menggunakan arsitektur **Event-Driven Streaming** yang kompleks untuk memastikan performa dan responsivitas. Berikut adalah bedah detail alurnya:

### Fase 1: Input & Validasi (Frontend -> Backend)
Proses dimulai ketika user menekan tombol "Start Simulation".

1.  **Payload Construction**: Frontend mengirim JSON ke `POST /stream_scheduling` berisi:
    *   `tasks`: List tugas (ID, durasi, prioritas, **cpu_usage**, **ram_usage**, dependensi).
        > **Catatan Penting**: `cpu_usage` dan `ram_usage` digunakan untuk menghitung **kompleksitas tugas**. Sistem akan otomatis **memperpanjang durasi task** berdasarkan formula: `duration_adjusted = duration * (1 + kompleksitas)` dimana `kompleksitas = (cpu + ram/1000) / 200`. Ini mempengaruhi scheduling di PSO dan ACO.
    *   `parameters`: Konfigurasi algoritma (jumlah semut/partikel, iterasi, dll).
    *   `agents`: (Opsional) Daftar agen kustom.
2.  **Data Normalization (Backend)**:
    *   **ID Cleaning**: Semua ID dikonversi ke string bersih (misal: `1.0` -> `"1"`).
    *   **Numeric Safety**: Nilai `null` atau string kosong pada durasi/biaya dikonversi ke `0.0` atau `1.0` (default).
    *   **Dependency Parsing**: String dependensi `"A;B"` dipecah menjadi list `["A", "B"]`.
3.  **Ghost Filtering**:
    *   Sistem memindai semua dependensi. Jika Task A bergantung pada Task Z, tapi Task Z tidak ada di daftar input, maka dependensi ini **dihapus** otomatis agar algoritma tidak crash.

### Fase 2: Inisialisasi & Eksekusi (The Loop)
Setelah data bersih, "mesin" algoritma dinyalakan.

1.  **Scheduler Instantiation**:
    *   Backend membuat objek `ACOScheduler` atau `PSOScheduler`.
    *   **Cost Function Factory**: Fungsi penilai (biaya) dibuat dinamis berdasarkan bobot yang diinput user (misal: lebih penting waktu vs keseimbangan beban).
2.  **The Iteration Loop**:
    Algoritma berjalan dalam loop (misal 100 iterasi). Di setiap iterasi:
    *   **Step A (Construction)**:
        *   *ACO*: Semut-semut berjalan membangun solusi berdasarkan feromon & heuristik.
        *   *PSO*: Partikel bergerak (update kecepatan & posisi) menuju solusi yang lebih baik.
    *   **Step B (Evaluation)**:
        *   Setiap solusi yang ditemukan dinilai skornya (Makespan & Load Balance).
        *   Solusi terbaik disimpan sebagai `Global Best`.
    *   **Step C (Update State)**:
        *   *ACO*: Feromon di jalur terbaik diperkuat (ditambah), jalur buruk menguap (dikurangi).
        *   *PSO*: Vektor kecepatan dan posisi partikel diperbarui.
    *   **Step D (Yield Data)**:
        *   Backend **tidak menunggu** loop selesai 100%.
        *   Setiap iterasi, ia melakukan `yield` (mengirim) data JSON parsial berisi progress saat ini.

### Fase 3: Real-time Streaming (Backend -> Frontend)
Ini adalah bagian yang membuat UI terasa "hidup".

1.  **SSE (Server-Sent Events)**:
    *   Koneksi HTTP tetap terbuka (Keep-Alive).
    *   Format data: `data: {"type": "progress", "iteration": 5, ...}\n\n`
2.  **Keepalive Mechanism**:
    *   Jika algoritma sedang berpikir keras (komputasi berat) dan tidak ada update selama beberapa detik, backend mengirim sinyal "ping" agar browser tidak mengira koneksi putus.
3.  **Final Handshake**:
    *   Setelah iterasi selesai, backend mengirim event `type: "final_metrics"`.
    *   Ini berisi tabel jadwal lengkap, statistik efisiensi tiap agen, dan total waktu eksekusi.
    *   Koneksi ditutup oleh server.

## 3. Bedah Codebase (Deep Dive)

Bagian ini membedah file-file utama dalam sistem, menjelaskan **apa** yang dilakukan kode tersebut dan **mengapa** diimplementasikan demikian.

### 3.1 `app.py` (The Gateway)
File ini adalah pintu gerbang aplikasi.

*   **`stream_scheduling()`**:
    *   **Fungsi**: Endpoint utama yang menerima request POST.
    *   **Detail Code**: Di dalamnya ada fungsi `generate()` yang menggunakan `yield`.
    *   **Alasan**: Kita menggunakan **Python Generators** untuk mendukung **Server-Sent Events (SSE)**. Jika kita pakai `return` biasa, user harus menunggu 100% proses selesai baru bisa lihat hasil. Dengan `yield`, data dikirim potong demi potong (chunk) secara real-time.

*   **`add_security_headers()`**:
    *   **Fungsi**: Middleware yang berjalan setelah setiap request.
    *   **Alasan**: Keamanan. Kita menyuntikkan header CSP (Content Security Policy) yang ketat untuk mencegah serangan XSS, serta header CORS agar frontend (Next.js/React) bisa mengakses API ini meskipun beda domain.

### 3.2 `models/base.py` (The Foundation)
Ini adalah pondasi (Parent Class) untuk semua algoritma.

*   **`MultiAgentScheduler` Class**:
    *   Kelas induk yang mewariskan fitur umum ke `ACOScheduler` dan `PSOScheduler`.

*   **`run()` Method (CRITICAL)**:
    *   **Detail Code**: Menggunakan `threading.Thread` dan `queue.Queue`.
    *   **Alasan**: Flask secara default berjalan sinkronus. Jika kita menjalankan loop optimasi berat di thread utama, server akan "hang" dan tidak bisa mengirim data streaming ke client.
    *   **Solusi**: Kita buat thread terpisah (`run_optimize`) untuk menghitung, lalu hasil per iterasinya dimasukkan ke `queue`. Thread utama hanya bertugas mengambil data dari `queue` dan mengirimnya ke user.

*   **`assign_to_agents()`**:
    *   **Fungsi**: Algoritma Greedy untuk membagi tugas ke agen.
    *   **Alasan**: Baik ACO maupun PSO pada akhirnya butuh cara konkret untuk menaruh Task A ke Agent 1. Fungsi ini mencari agen mana yang "paling cepat kosong" (finish time terendah) untuk menampung tugas tersebut.

### 3.3 `models/aco.py` (The Ant Logic)
Implementasi spesifik Ant Colony Optimization.

*   **`construct_solution()`**:
    *   **Fungsi**: Satu "semut" membangun jadwal lengkap.
    *   **Detail Code**: Loop sampai semua tugas selesai. Di setiap langkah, hitung probabilitas pilih tugas berdasarkan rumus ACO (Feromon^alpha * Heuristik^beta).

*   **`update_pheromones()`**:
    *   **Fungsi**: Belajar dari pengalaman.
    *   **Detail Code**: Menguapkan feromon lama (`feromon *= (1 - evaporation)`), lalu menambah feromon baru di jalur yang dilewati solusi terbaik.
    *   **Alasan**: Ini inti dari "kecerdasan" semut. Jalur yang menghasilkan jadwal lebih cepat akan semakin "harum" (nilai feromon tinggi), sehingga semut berikutnya lebih mungkin lewat situ.

### 3.4 `models/pso.py` (The Particle Logic)
Implementasi spesifik Particle Swarm Optimization.

*   **`position_to_sequence()` (CRITICAL)**:
    *   **Fungsi**: Mengubah posisi partikel (angka float) menjadi urutan tugas (list ID).
    *   **Detail Code**: Melakukan `np.argsort(posisi)`.
    *   **Alasan**: PSO bekerja di matematika vektor kontinu (tambah/kurang kecepatan). Penjadwalan adalah diskrit. Kita butuh "jembatan" (decoder) ini agar rumus fisika PSO bisa dipakai untuk mengurutkan tugas.

*   **`optimize()`**:
    *   **Fungsi**: Loop utama PSO.
    *   **Detail Code**: 
        - **Inisialisasi**: Posisi partikel diberi soft priority bias (`+0.025 * (priority-1)`) agar task priority tinggi sedikit lebih likely dipilih awal, tapi tidak dominant.
        - **Update**: Kecepatan (`v = w*v + c1*r1*(pbest-x) + c2*r2*(gbest-x)`) dan posisi (`x += v`).
    *   **Alasan**: Ini adalah simulasi pergerakan burung. Partikel ditarik ke dua arah: pengalaman terbaik dia sendiri (`pbest`) dan pengalaman terbaik kawanan (`gbest`). Priority bias bersifat probabilistic, tidak deterministic.

### 3.5 `models/utils.py` (The Helper)
Fungsi-fungsi pembantu yang "kotor" tapi penting.

*   **`normalize_id()`**:
    *   **Alasan**: User sering input data Excel yang aneh (misal ID "101" jadi "101.0"). Fungsi ini membersihkannya agar sistem tidak error saat mencocokkan ID.
*   **`filter_ghost_dependencies()`**:
    *   **Alasan**: User sering salah input (misal Task A butuh Task Z, tapi Task Z lupa diinput). Tanpa fungsi ini, algoritma akan crash dengan `KeyError`.
*   **`fungsi_biaya_per_tugas()`**:
    *   **Fungsi**: Menghitung biaya eksekusi untuk SATU tugas pada SATU agen (legacy function, tidak dipakai di flow utama).
    *   **Detail Code**: Rumus kompleksitas: `kompleksitas = (cpu_usage + ram_usage/1000) / 200`, lalu `biaya = (durasi * (1 + kompleksitas)) / (efisiensi * kapasitas)`.
    *   **Catatan**: Sejak implementasi terbaru, kompleksitas langsung diterapkan ke `task_length` di `app.py` (line 255-258), jadi PSO dan ACO otomatis dapat durasi yang sudah di-adjust.
*   **`fungsi_biaya_jadwal()`**:
    *   **Alasan**: Ini adalah "Scorecard". Kita tidak cuma peduli cepat (Makespan), tapi juga adil (Load Balance). Fungsi ini menggabungkan keduanya jadi satu angka agar algoritma punya satu tujuan optimasi yang jelas.

## 4. Alur (Flow) Detail

Berikut adalah urutan eksekusi ketika user menekan tombol "Start Simulation":

1.  **Start**: Request masuk ke `POST /stream_scheduling`.
2.  **Parsing**:
    *   Ambil `tasks` dan `parameters` dari JSON body.
    *   Set Random Seed (agar hasil bisa direproduksi).
3.  **Normalisasi Data**:
    *   Loop setiap task: Perbaiki ID, konversi angka (durasi/cost) ke float, parse dependensi.
    *   Panggil `filter_ghost_dependencies` untuk membersihkan relasi invalid.
4.  **Setup Agen**:
    *   Cek apakah user kirim data agen? Jika tidak, panggil `generate_agen_default`.
5.  **Init Algoritma**:
    *   Buat instance `ACOScheduler` atau `PSOScheduler` sesuai pilihan user.
    *   Inject `cost_function` yang sudah dikonfigurasi bobotnya.
6.  **Eksekusi & Stream**:
    *   Masuk ke loop `scheduler.run()`.
    *   **Yield Data**: Kirim JSON string ke client setiap ada update.
    *   **Keepalive**: Kirim ping setiap 10 iterasi agar koneksi tidak diputus browser/proxy.
7.  **Finalisasi**:
    *   Ambil hasil terbaik.
    *   Susun tabel jadwal (`full_schedule_table`) dan statistik agen (`agent_info_table`).
    *   Kirim event `final_metrics` ke client.
8.  **Stop**: Tutup koneksi stream.

## 5. Struktur Folder

```
backend/
├── app.py                 # Entry point aplikasi
├── models/
│   ├── aco.py            # Logika Ant Colony Optimization
│   ├── pso.py            # Logika Particle Swarm Optimization
│   ├── base.py           # Class Parent (MultiAgentScheduler)
│   └── utils.py          # Fungsi bantu (normalisasi, validasi, biaya)
├── docs/
│   └── README.md         # Dokumentasi ini
├── data/                  # Folder dataset contoh
└── requirements.txt       # Daftar library Python
```

## 6. Detail Algoritma

Bagian ini menjelaskan bagaimana algoritma bekerja secara mendalam, khususnya dalam konteks Multi-Agent.

### 6.1 Ant Colony Optimization (ACO)

ACO terinspirasi dari perilaku semut mencari jalur terpendek dari sarang ke sumber makanan.

*   **Analogi**:
    *   **Semut** = Agen pencari solusi (bukan Server/Worker).
    *   **Jalur** = Urutan penugasan Tugas ke Agen.
    *   **Feromon** = Jejak kimia yang ditinggalkan semut di jalur yang bagus (biaya rendah).

*   **Cara Kerja**:
    1.  Setiap "Semut" membangun solusi lengkap (jadwal) dari awal sampai akhir.
    2.  Saat memilih tugas berikutnya untuk dikerjakan, semut mempertimbangkan:
        *   **Heuristik ($\eta$)**: Seberapa "menarik" tugas ini (misal: durasi pendek, prioritas tinggi).
        *   **Feromon ($\tau$)**: Seberapa sering tugas ini dipilih oleh semut sukses sebelumnya.
    3.  Probabilitas memilih tugas $j$ setelah tugas $i$:
        $$P_{ij} = \frac{(\tau_{ij})^\alpha \cdot (\eta_{ij})^\beta}{\sum (\tau)^\alpha \cdot (\eta)^\beta}$$
    4.  Setelah semua semut selesai, feromon diupdate. Jalur dengan biaya (makespan) terendah mendapat tambahan feromon lebih banyak.

### 6.2 Particle Swarm Optimization (PSO)

PSO terinspirasi dari perilaku kawanan burung (flock) atau ikan (school) yang bergerak bersama mencari lokasi terbaik.

*   **Analogi**:
    *   **Partikel** = Agen pencari solusi.
    *   **Posisi** = Kandidat solusi (konfigurasi jadwal).
    *   **Kecepatan** = Arah perubahan solusi.

*   **Tantangan**:
    PSO aslinya bekerja di **ruang kontinu** (angka desimal), sedangkan penjadwalan adalah masalah **diskrit** (urutan tugas).

*   **Solusi: Konversi Partikel ke Diskrit (Decoding)**
    Ini adalah mekanisme kunci agar PSO bisa dipakai untuk penjadwalan.

    1.  **Representasi Posisi**:
        Setiap partikel memiliki vektor posisi sepanjang jumlah tugas ($N$). Nilainya adalah angka float acak (misal: `[0.55, 2.10, 0.15]`).
    
    2.  **Decoding (Sorting)**:
        Angka-angka tersebut dianggap sebagai "prioritas". Kita mengurutkan indeks tugas berdasarkan nilai posisinya.
        *   Contoh Posisi: `[Task A: 0.55, Task B: 2.10, Task C: 0.15]`
        *   Urutkan (Ascending): `Task C (0.15) -> Task A (0.55) -> Task B (2.10)`
        *   Hasil Sequence: `[C, A, B]`
    
    3.  **Assignment**:
        Urutan tugas `[C, A, B]` kemudian diberikan ke agen-agen yang tersedia menggunakan metode *Greedy* (berikan ke agen yang paling cepat kosong).

    > **Kenapa dikonversi?**
    > Karena PSO butuh matematika vektor (tambah, kurang, kali) untuk update kecepatan & posisi. Operasi ini tidak bisa dilakukan langsung pada urutan tugas (misal: `Task A + Task B` tidak valid). Dengan menggunakan angka float sebagai representasi, kita bisa hitung rumus PSO, lalu "menerjemahkan" (decode) hasilnya kembali ke urutan tugas.

## 7. Perspektif Multi-Agent

Penting untuk membedakan dua istilah "Agen" dalam sistem ini:

1.  **System Agents (Workers/Servers)**:
    *   Ini adalah entitas nyata yang mengerjakan tugas (misal: CPU Core, Server Cloud, Mesin Pabrik).
    *   Input dari user (misal: "Agent-1", "Agent-2").
    *   Memiliki atribut: Kapasitas, Efisiensi.

    *   Contoh: Jika kita set `n_ants=10`, berarti ada 10 "pencari solusi" yang bekerja paralel di setiap iterasi untuk menemukan jadwal terbaik bagi para Worker.

### 6.3 Analisis Komparabilitas (Apple-to-Apple)

Untuk memastikan hasil eksperimen valid secara ilmiah, implementasi ini menjamin perbandingan yang adil (*Apple-to-Apple*) antara ACO dan PSO melalui mekanisme berikut:

1.  **Input Data Identik**:
    *   Kedua algoritma menerima dataset yang sama persis setelah melalui proses normalisasi di `app.py`.
    *   Parameter tugas seperti `length`, `cost`, `priority`, `cpu_usage`, dan `ram_usage` tersedia dan digunakan oleh kedua algoritma.

2.  **Manajemen Sumber Daya & Constraints Sama**:
    *   Baik ACO maupun PSO menggunakan logika `assign_to_agents` yang sama (dari parent class `MultiAgentScheduler`).
    *   Artinya, cara mereka menghitung durasi tugas (termasuk penalti kompleksitas CPU/RAM) dan mengecek kapasitas agen adalah identik. Tidak ada algoritma yang mendapat "perlakuan khusus" dalam hal alokasi resource.

3.  **Objective Function Tunggal**:
    *   Keduanya mengoptimalkan `cost_function` yang sama. Skor akhir (fitness) dihitung menggunakan rumus yang seragam, menggabungkan *makespan* dan *load balance index*.

4.  **Pemanfaatan Fitur "Priority" yang Adil**:
    *   **ACO**: Menggunakan priority sebagai bagian dari nilai **Heuristik**. Semakin tinggi prioritas, semakin besar probabilitas semut memilih tugas tersebut.
    *   **PSO**: Menggunakan priority sebagai **Bias Inisialisasi**. Posisi awal partikel digeser sedikit (soft bias) agar tugas prioritas tinggi cenderung berada di urutan awal.
    *   **Kesimpulan**: Masing-masing algoritma memanfaatkan fitur prioritas sesuai dengan karakteristik alaminya (Probabilistik vs Search Space Bias), tanpa memaksakan logika deterministik yang akan merusak sifat stokastik algoritma.

