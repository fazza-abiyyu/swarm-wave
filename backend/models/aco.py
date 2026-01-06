import numpy as np
import random
import json
import pandas as pd
import time
from .base import MultiAgentScheduler


class ACO_MultiAgent_Scheduler(MultiAgentScheduler):
    """
    Implementasi ACO (Ant Colony Optimization) untuk penjadwalan tugas multi-agen.
    """

    @staticmethod
    def default_heuristic_function(task):
        """
        Fungsi heuristik default: (1.0 / Durasi) * Prioritas.
        """
        duration = max(task.get("length", 1), 0.1)
        priority = max(task.get("priority", 1), 1.0)
        return (1.0 / duration) * priority

    def __init__(
        self,
        tasks,
        agents,
        cost_function,
        n_ants=10,
        n_iterations=100,
        alpha=0.9,
        beta=2.0,
        evaporation_rate=0.5,
        pheromone_deposit=100,
        **kwargs,
    ):
        """
        Inisialisasi Scheduler ACO dengan parameter koloni semut, feromon, dan heuristik.
        """
        super().__init__(tasks, agents, cost_function, **kwargs)
        self.fungsi_heuristik = self.default_heuristic_function
        self.jumlah_semut = n_ants if self.jumlah_tugas > 0 else 0
        self.jumlah_iterasi = n_iterations if self.jumlah_tugas > 0 else 0
        self.alpha, self.beta = alpha, beta
        self.tingkat_penguapan, self.deposit_feromon = (
            evaporation_rate,
            pheromone_deposit,
        )
        self.prioritize_balance = True

        if self.jumlah_tugas > 0:
            self.feromon = np.ones((self.jumlah_tugas, self.jumlah_tugas))
            self.heuristik = self.calculate_heuristics()
        else:
            self.feromon = self.heuristik = np.array([[]])

    def calculate_heuristics(self):
        """
        Hitung nilai heuristik statis untuk semua pasangan tugas (jarak/biaya invers).
        """
        heuristik = np.zeros((self.jumlah_tugas, self.jumlah_tugas))
        for i in range(self.jumlah_tugas):
            for j in range(self.jumlah_tugas):
                if i != j:
                    heuristik[i, j] = self.fungsi_heuristik(self.tugas[j])
        return heuristik

    def construct_solution(self):
        """
        Konstruksi solusi lengkap oleh satu semut, langkah demi langkah.
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

            # Identifikasi tugas yang siap (Hard Constraint: Dependensi)
            siap = self.get_ready_tasks(list(tersisa), selesai)

            # Deadlock Handling: Paksa pilih tugas dengan dependensi yang belum terpenuhi paling sedikit
            if not siap:
                min_tidak_terpenuhi = float("inf")
                tugas_paksa = None
                for idx in tersisa:
                    tid = self.peta_tugas_terbalik[idx]
                    tidak_terpenuhi = len(
                        [d for d in self.dependensi.get(tid, []) if d not in selesai]
                    )
                    if tidak_terpenuhi < min_tidak_terpenuhi:
                        min_tidak_terpenuhi, tugas_paksa = tidak_terpenuhi, idx
                siap = [tugas_paksa] if tugas_paksa is not None else []

            if not siap:
                break

            # Pilih tugas berikutnya (Roulette Wheel Selection)
            if saat_ini is None or saat_ini not in siap:
                tugas_berikutnya = random.choice(siap)
            else:
                probabilitas = self.calculate_probabilities(saat_ini, siap)
                tugas_berikutnya = (
                    np.random.choice(siap, p=probabilitas) if len(siap) > 1 else siap[0]
                )

            # Update State
            rute.append(tugas_berikutnya)
            tersisa.remove(tugas_berikutnya)
            selesai.add(self.peta_tugas_terbalik[tugas_berikutnya])
            saat_ini = tugas_berikutnya

        rute.extend(sorted(tersisa))
        return rute

    def calculate_probabilities(self, saat_ini, belum_dikunjungi):
        """
        Hitung probabilitas pemilihan (Feromon^Alpha * Heuristik^Beta).
        """
        if not belum_dikunjungi:
            return np.array([])
        phero = self.feromon[saat_ini, belum_dikunjungi] ** self.alpha
        heur = self.heuristik[saat_ini, belum_dikunjungi] ** self.beta
        keinginan = phero * heur
        total = np.sum(keinginan)
        return (
            keinginan / total
            if total > 0
            else np.ones(len(belum_dikunjungi)) / len(belum_dikunjungi)
        )

    def update_pheromones(self, rute_list, biaya_list):
        """
        Update feromon: Evaporasi lama, lalu deposit baru berdasarkan kualitas solusi.
        """
        if not rute_list or self.jumlah_tugas == 0:
            return
        self.feromon *= 1 - self.tingkat_penguapan
        for rute, biaya in zip(rute_list, biaya_list):
            if biaya == 0 or len(rute) < 2:
                continue
            tambah = self.deposit_feromon / biaya
            for i in range(len(rute) - 1):
                self.feromon[rute[i], rute[i + 1]] += tambah
            if len(rute) >= 2:
                self.feromon[rute[-1], rute[0]] += tambah

    def optimize(self, show_progress=True, progress_callback=None):
        """
        Jalankan loop utama optimasi ACO.
        """
        # Inisialisasi solusi awal (Sequential sederhana)
        urutan_awal = list(range(self.jumlah_tugas))
        jadwal_awal, waktu_agen_awal, keseimbangan_awal = self.assign_to_agents(
            urutan_awal
        )
        durasi_total_awal = max(waktu_agen_awal.values(), default=0)
        self.biaya_terbaik = self.fungsi_biaya(jadwal_awal, durasi_total_awal)
        self.durasi_terbaik = durasi_total_awal  # Simpan makespan aktual
        self.jadwal_terbaik = jadwal_awal
        self.indeks_keseimbangan_terbaik = keseimbangan_awal

        waktu_mulai = time.time()

        for i in range(self.jumlah_iterasi):
            rute_list, biaya_list = [], []
            ada_terbaik_baru = False

            # Konstruksi Solusi oleh Semut
            for _ in range(self.jumlah_semut):
                urutan = self.construct_solution()
                if urutan:
                    # Evaluasi oleh Greedy
                    jadwal, waktu_agen, indeks_keseimbangan = self.assign_to_agents(
                        urutan
                    )
                    durasi_total = max(waktu_agen.values(), default=0)
                    biaya = self.fungsi_biaya(jadwal, durasi_total)
                    rute_list.append(urutan)
                    biaya_list.append(biaya)

                    # Simpan solusi terbaik (Elitisme)
                    if biaya < self.biaya_terbaik or (
                        biaya == self.biaya_terbaik
                        and indeks_keseimbangan < self.indeks_keseimbangan_terbaik
                    ):
                        self.biaya_terbaik = biaya
                        self.durasi_terbaik = durasi_total
                        self.jadwal_terbaik = jadwal
                        self.indeks_keseimbangan_terbaik = indeks_keseimbangan
                        ada_terbaik_baru = True
                else:
                    rute_list.append([])
                    biaya_list.append(float("inf"))

            # Update Feromon Global
            self.update_pheromones(rute_list, biaya_list)

            # Tracking Riwayat
            self.riwayat_iterasi.append(
                {
                    "iteration": i + 1,
                    "best_makespan": self.durasi_terbaik
                    if self.durasi_terbaik != float("inf")
                    else 0.0,
                    "load_balance": self.indeks_keseimbangan_terbaik
                    if self.indeks_keseimbangan_terbaik != float("inf")
                    else 0.0,
                }
            )

            # Real-time streaming callback
            if progress_callback:
                progress_callback(
                    {
                        "iteration": i + 1,
                        "best_makespan": self.durasi_terbaik
                        if self.durasi_terbaik != float("inf")
                        else 0.0,
                        "load_balance": self.indeks_keseimbangan_terbaik
                        if self.indeks_keseimbangan_terbaik != float("inf")
                        else 0.0,
                    }
                )

            if show_progress and ada_terbaik_baru:
                print(
                    f"Iterasi {i + 1}: Terbaik baru! Makespan: {self.durasi_terbaik:.2f}, Load Balance: {self.indeks_keseimbangan_terbaik:.4f}"
                )
            elif show_progress:
                print(
                    f"Iterasi {i + 1}: Makespan Terbaik: {self.durasi_terbaik:.2f}, Load Balance: {self.indeks_keseimbangan_terbaik:.4f}"
                )

        # Rekap hasil akhir
        waktu_akhir_agen_final = {}
        if self.jadwal_terbaik:
            for penugasan in self.jadwal_terbaik:
                id_agen = penugasan["agent_id"]
                waktu_akhir = penugasan["finish_time"]
                waktu_akhir_agen_final[id_agen] = max(
                    waktu_akhir_agen_final.get(id_agen, 0), waktu_akhir
                )

        return {
            "schedule": pd.DataFrame(self.jadwal_terbaik)
            if self.jadwal_terbaik
            else pd.DataFrame(),
            "makespan": self.durasi_terbaik
            if self.durasi_terbaik != float("inf")
            else 0.0,
            "load_balance_index": self.indeks_keseimbangan_terbaik
            if self.indeks_keseimbangan_terbaik != float("inf")
            else 0.0,
            "agent_finish_times": waktu_akhir_agen_final,
            "computation_time": time.time() - waktu_mulai,
            "iteration_history": pd.DataFrame(self.riwayat_iterasi),
            "algorithm": self.__class__.__name__,
        }


# Alias untuk kompatibilitas
ACOScheduler = ACO_MultiAgent_Scheduler
