import numpy as np
import random
import json
import pandas as pd
import time
from .base import MultiAgentScheduler

class ACO_MultiAgent_Scheduler(MultiAgentScheduler):
    """
    Implementasi ACO (Ant Colony Optimization) untuk penjadwalan tugas multi-agen.
    
    Algoritma ini menggunakan sekumpulan "semut" buatan yang membangun solusi secara iteratif.
    Semut memilih tugas berdasarkan probabilitas yang dipengaruhi oleh jejak feromon (pengalaman masa lalu)
    dan nilai heuristik (informasi lokal problem-specific).
    """

    def __init__(self, tasks, cost_function, heuristic_function, agents=None, n_ants=10, n_iterations=100,
                 alpha=0.9, beta=2.0, evaporation_rate=0.5, pheromone_deposit=100, **kwargs):
        """
        Inisialisasi Scheduler ACO.
        
        Args:
            tasks (list | pd.DataFrame): Daftar tugas.
            cost_function (callable): Fungsi biaya untuk evaluasi jadwal.
            heuristic_function (callable): Fungsi heuristik untuk menghitung ketertarikan antar tugas.
            agents (list, optional): Daftar agen. Defaults to None (generate default).
            n_ants (int, optional): Jumlah semut per iterasi. Defaults to 10.
            n_iterations (int, optional): Jumlah iterasi optimasi. Defaults to 100.
            alpha (float, optional): Bobot pengaruh feromon. Defaults to 0.9.
            beta (float, optional): Bobot pengaruh heuristik. Defaults to 2.0.
            evaporation_rate (float, optional): Tingkat penguapan feromon (0-1). Defaults to 0.5.
            pheromone_deposit (float, optional): Jumlah feromon yang ditinggalkan semut. Defaults to 100.
            **kwargs: Argumen tambahan untuk MultiAgentScheduler parent class.
        """
        super().__init__(tasks, agents, cost_function, **kwargs)
        self.fungsi_heuristik = heuristic_function
        self.jumlah_semut = n_ants if self.jumlah_tugas > 0 else 0
        self.jumlah_iterasi = n_iterations if self.jumlah_tugas > 0 else 0
        self.alpha, self.beta = alpha, beta
        self.tingkat_penguapan, self.deposit_feromon = evaporation_rate, pheromone_deposit
        self.prioritize_balance = True

        if self.jumlah_tugas > 0:
            self.feromon = np.ones((self.jumlah_tugas, self.jumlah_tugas))
            self.heuristik = self.calculate_heuristics()
        else:
            self.feromon = self.heuristik = np.array([[]])

    def calculate_heuristics(self):
        """
        Hitung nilai heuristik untuk semua pasangan tugas.
        
        Nilai heuristik (eta) biasanya statis dan dihitung di awal.
        Merepresentasikan "jarak" atau "biaya" invers antara tugas i dan j,
        atau seberapa bagus memilih tugas j setelah tugas i.
        
        Returns:
            np.ndarray: Matriks heuristik ukuran (jumlah_tugas x jumlah_tugas).
        """
        heuristik = np.zeros((self.jumlah_tugas, self.jumlah_tugas))
        for i in range(self.jumlah_tugas):
            for j in range(self.jumlah_tugas):
                if i != j:
                    heuristik[i, j] = self.fungsi_heuristik(self.tugas[j])
        return heuristik

    def construct_solution(self):
        """
        Konstruksi solusi lengkap oleh satu semut.
        
        Semut membangun jadwal langkah demi langkah:
        1. Identifikasi tugas yang siap (dependensi terpenuhi).
        2. Jika tidak ada yang siap tapi ada tugas tersisa (deadlock), paksa pilih tugas dengan unmet dependencies paling sedikit.
        3. Pilih tugas berikutnya secara probabilistik (Roulette Wheel Selection) atau acak jika belum ada rute.
        4. Update state (tugas selesai, posisi semut).
        
        Returns:
            list: Urutan indeks tugas yang merepresentasikan jadwal/solusi.
        """
        if self.jumlah_tugas == 0:
            return []
        rute, tersisa = [], set(range(self.jumlah_tugas))
        selesai = set()
        saat_ini = None
        iterasi_maks = self.jumlah_tugas * 2
        hitung_iterasi = 0

        while tersisa and hitung_iterasi < iterasi_maks:
            hitung_iterasi += 1
            siap = self.get_ready_tasks(list(tersisa), selesai)

            if not siap:
                min_tidak_terpenuhi = float('inf')
                tugas_paksa = None
                for idx in tersisa:
                    tid = self.peta_tugas_terbalik[idx]
                    tidak_terpenuhi = len([d for d in self.dependensi.get(tid, []) if d not in selesai])
                    if tidak_terpenuhi < min_tidak_terpenuhi:
                        min_tidak_terpenuhi, tugas_paksa = tidak_terpenuhi, idx
                siap = [tugas_paksa] if tugas_paksa is not None else []

            if not siap:
                break

            if saat_ini is None or saat_ini not in siap:
                tugas_berikutnya = random.choice(siap)
            else:
                probabilitas = self.calculate_probabilities(saat_ini, siap)
                tugas_berikutnya = np.random.choice(siap, p=probabilitas) if len(siap) > 1 else siap[0]

            rute.append(tugas_berikutnya)
            tersisa.remove(tugas_berikutnya)
            selesai.add(self.peta_tugas_terbalik[tugas_berikutnya])
            saat_ini = tugas_berikutnya

        rute.extend(sorted(tersisa))
        return rute

    def calculate_probabilities(self, saat_ini, belum_dikunjungi):
        """
        Hitung probabilitas pemilihan tugas berikutnya.
        
        Probabilitas P(i,j) = [tau(i,j)^alpha] * [eta(i,j)^beta] / Sigma(...)
        Dimana:
        - tau: intensitas feromon
        - eta: nilai heuristik
        
        Args:
            saat_ini (int): Indeks tugas tempat semut berada sekarang.
            belum_dikunjungi (list): List indeks tugas kandidat yang bisa dikunjungi.
            
        Returns:
            np.ndarray: Array probabilitas untuk setiap tugas kandidat.
        """
        if not belum_dikunjungi:
            return np.array([])
        phero = self.feromon[saat_ini, belum_dikunjungi] ** self.alpha
        heur = self.heuristik[saat_ini, belum_dikunjungi] ** self.beta
        keinginan = phero * heur
        total = np.sum(keinginan)
        return keinginan / total if total > 0 else np.ones(len(belum_dikunjungi)) / len(belum_dikunjungi)

    def update_pheromones(self, rute_list, biaya_list):
        """
        Update matriks feromon berdasarkan kumpulan solusi dari semut-semut.
        
        Langkah:
        1. Evaporasi: Kurangi semua feromon dengan faktor evaporation_rate.
        2. Deposit: Tambahkan feromon pada jalur yang dilewati semut, proporsional dengan kualitas solusi (1/biaya).
           Jalur yang menghasilkan biaya lebih rendah mendapat lebih banyak feromon.
           
        Args:
            rute_list (list): List dari list urutan tugas (solusi).
            biaya_list (list): List biaya (makespan/penalty) untuk setiap solusi.
        """
        if not rute_list or self.jumlah_tugas == 0:
            return
        self.feromon *= (1 - self.tingkat_penguapan)
        for rute, biaya in zip(rute_list, biaya_list):
            if biaya == 0 or len(rute) < 2:
                continue
            tambah = self.deposit_feromon / biaya
            for i in range(len(rute) - 1):
                self.feromon[rute[i], rute[i+1]] += tambah
            if len(rute) >= 2:
                self.feromon[rute[-1], rute[0]] += tambah

    def optimize(self, show_progress=True, progress_callback=None):
        """
        Jalankan algoritma optimasi ACO utama.
        
        Iterasi sebanyak n_iterations. Pada setiap iterasi:
        1. Setiap semut membangun solusi.
        2. Evaluasi solusi (hitung makespan & load balance).
        3. Perbarui solusi terbaik global jika ditemukan yang lebih baik.
        4. Update feromon berdasarkan hasil iterasi ini.
        5. Log progress & stream update jika ada callback.
        
        Args:
            show_progress (bool): Print progress ke console.
            progress_callback (callable): Fungsi untuk mengirim update progress real-time.
            
        Returns:
            dict: Laporan hasil optimasi lengkap.
        """
        urutan_awal = list(range(self.jumlah_tugas))
        jadwal_awal, waktu_agen_awal, keseimbangan_awal = self.assign_to_agents(urutan_awal)
        durasi_total_awal = max(waktu_agen_awal.values(), default=0)
        self.biaya_terbaik = self.fungsi_biaya(jadwal_awal, durasi_total_awal)
        self.durasi_terbaik = durasi_total_awal  # Simpan makespan aktual
        self.jadwal_terbaik = jadwal_awal
        self.indeks_keseimbangan_terbaik = keseimbangan_awal

        waktu_mulai = time.time()

        for i in range(self.jumlah_iterasi):
            rute_list, biaya_list = [], []
            ada_terbaik_baru = False

            for _ in range(self.jumlah_semut):
                urutan = self.construct_solution()
                if urutan:
                    jadwal, waktu_agen, indeks_keseimbangan = self.assign_to_agents(urutan)
                    durasi_total = max(waktu_agen.values(), default=0)
                    biaya = self.fungsi_biaya(jadwal, durasi_total)
                    rute_list.append(urutan)
                    biaya_list.append(biaya)

                    if biaya < self.biaya_terbaik or (biaya == self.biaya_terbaik and indeks_keseimbangan < self.indeks_keseimbangan_terbaik):
                        self.biaya_terbaik = biaya
                        self.durasi_terbaik = durasi_total  # Simpan makespan aktual
                        self.jadwal_terbaik = jadwal
                        self.indeks_keseimbangan_terbaik = indeks_keseimbangan
                        ada_terbaik_baru = True
                else:
                    rute_list.append([])
                    biaya_list.append(float('inf'))

            self.update_pheromones(rute_list, biaya_list)

            self.riwayat_iterasi.append({
                'iteration': i + 1,
                'best_makespan': self.durasi_terbaik if self.durasi_terbaik != float('inf') else 0.0,
                'load_balance': self.indeks_keseimbangan_terbaik if self.indeks_keseimbangan_terbaik != float('inf') else 0.0
            })

            # Real-time streaming callback
            if progress_callback:
                progress_callback({
                    'iteration': i + 1,
                    'best_makespan': self.durasi_terbaik if self.durasi_terbaik != float('inf') else 0.0,
                    'load_balance': self.indeks_keseimbangan_terbaik if self.indeks_keseimbangan_terbaik != float('inf') else 0.0
                })

            if show_progress and ada_terbaik_baru:
                print(f"Iterasi {i+1}: Terbaik baru! Makespan: {self.durasi_terbaik:.2f}, Load Balance: {self.indeks_keseimbangan_terbaik:.4f}")
            elif show_progress:
                print(f"Iterasi {i+1}: Makespan Terbaik: {self.durasi_terbaik:.2f}, Load Balance: {self.indeks_keseimbangan_terbaik:.4f}")

        waktu_akhir_agen_final = {}
        if self.jadwal_terbaik:
            for penugasan in self.jadwal_terbaik:
                id_agen = penugasan['agent_id']
                waktu_akhir = penugasan['finish_time']
                waktu_akhir_agen_final[id_agen] = max(waktu_akhir_agen_final.get(id_agen, 0), waktu_akhir)

        return {
            'schedule': pd.DataFrame(self.jadwal_terbaik) if self.jadwal_terbaik else pd.DataFrame(),
            'makespan': self.durasi_terbaik if self.durasi_terbaik != float('inf') else 0.0,
            'load_balance_index': self.indeks_keseimbangan_terbaik if self.indeks_keseimbangan_terbaik != float('inf') else 0.0,
            'agent_finish_times': waktu_akhir_agen_final,
            'computation_time': time.time() - waktu_mulai,
            'iteration_history': pd.DataFrame(self.riwayat_iterasi),
            'algorithm': self.__class__.__name__
        }


# Alias untuk kompatibilitas
ACOScheduler = ACO_MultiAgent_Scheduler