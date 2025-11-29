import numpy as np
import random
import json
import pandas as pd
import time
from .base import MultiAgentScheduler

class PSO_MultiAgent_Scheduler(MultiAgentScheduler):
    """Implementasi PSO (Particle Swarm Optimization)."""

    def __init__(self, tasks, agents, cost_function, n_particles=30, n_iterations=100, 
                 w=0.5, c1=1.5, c2=1.5, **kwargs):
        super().__init__(tasks, agents, cost_function, **kwargs)
        self.jumlah_partikel = n_particles if self.jumlah_tugas > 0 else 0
        self.jumlah_iterasi = n_iterations if self.jumlah_tugas > 0 else 0
        self.w, self.c1, self.c2 = w, c1, c2

        if self.jumlah_tugas > 0 and self.jumlah_partikel > 0:
            self.posisi = np.random.rand(self.jumlah_partikel, self.jumlah_tugas)
            
            # Soft priority bias (probabilistic, not deterministic)
            for i, task in enumerate(self.tugas):
                priority = task.get('priority', 1)
                # Small additive bias: priority 5 → +0.1, priority 1 → +0.0
                priority_bias = (priority - 1) * 0.025  # Subtle influence
                self.posisi[:, i] += priority_bias
            
            # Clip to avoid extreme values
            self.posisi = np.clip(self.posisi, 0, 2)
            
            self.kecepatan = np.random.rand(self.jumlah_partikel, self.jumlah_tugas) * 0.1
            self.posisi_pbest = self.posisi.copy()
            self.biaya_pbest = np.full(self.jumlah_partikel, float('inf'))
            self.durasi_pbest = np.full(self.jumlah_partikel, float('inf'))
            self.posisi_gbest = None

            if self.jumlah_partikel > 0:
                self.posisi_gbest = self.posisi[0].copy()
        else:
            self.posisi = self.kecepatan = self.posisi_pbest = np.array([[]])
            self.biaya_pbest = np.array([])
            self.durasi_pbest = np.array([])
            self.posisi_gbest = None

    def position_to_sequence(self, posisi):
        """Konversi posisi partikel ke urutan tugas."""
        if self.jumlah_tugas == 0:
            return []
        if not self.enable_dependencies:
            return np.argsort(posisi)

        # Koreksi berbasis penalti
        urutan = np.argsort(posisi)
        penalti = {}
        selesai = set()
        tersedia = set(urutan)
        terkoreksi = []
        iterasi_maks = self.jumlah_tugas * 2

        daftar_id_tugas = [str(tugas[self.task_id_col]) for tugas in self.tugas]

        for indeks_tugas in urutan:
            tid = daftar_id_tugas[indeks_tugas]
            prioritas_dasar = posisi[indeks_tugas]
            dep_tidak_terpenuhi = sum(1 for dep in self.dependensi.get(tid, []) if dep not in selesai)
            penalti[indeks_tugas] = prioritas_dasar - (dep_tidak_terpenuhi * 0.5)

        hitung_iterasi = 0
        while tersedia and hitung_iterasi < iterasi_maks:
            hitung_iterasi += 1
            siap = [idx for idx in tersedia if self.is_dependency_satisfied(daftar_id_tugas[idx], selesai)]
            if siap:
                terbaik = max(siap, key=lambda t: penalti[t])
                terkoreksi.append(terbaik)
                tersedia.remove(terbaik)
                selesai.add(daftar_id_tugas[terbaik])
            else:
                # Fallback: min deps (SAMA DENGAN NOTEBOOK)
                fallback = min(tersedia, key=lambda t: len(self.dependensi.get(daftar_id_tugas[t], [])))
                terkoreksi.append(fallback)
                tersedia.remove(fallback)
                selesai.add(daftar_id_tugas[fallback])

        terkoreksi.extend(sorted(tersedia))
        return np.array(terkoreksi)

    def position_to_schedule(self, posisi):
        """Konversi posisi ke jadwal."""
        urutan = self.position_to_sequence(posisi)
        jadwal, waktu_selesai_agen, keseimbangan_beban = self.assign_to_agents(urutan)
        return jadwal, waktu_selesai_agen

    def optimize(self, show_progress=True, progress_callback=None):
        """Optimasi menggunakan PSO."""
        if self.jumlah_partikel == 0 or self.jumlah_tugas == 0:
            return super().optimize(show_progress=False, progress_callback=progress_callback)

        waktu_mulai = time.time()
        if show_progress:
            print(f"Memulai optimasi {self.__class__.__name__}...")

        urutan_awal = self.position_to_sequence(self.posisi[0])
        jadwal_awal, waktu_agen_awal, keseimbangan_awal = self.assign_to_agents(urutan_awal)
        durasi_total_awal = max(waktu_agen_awal.values(), default=0)
        self.biaya_terbaik = self.fungsi_biaya(jadwal_awal, durasi_total_awal)
        self.durasi_terbaik = durasi_total_awal  # Simpan makespan aktual
        self.jadwal_terbaik = jadwal_awal
        self.indeks_keseimbangan_terbaik = keseimbangan_awal

        for i in range(self.jumlah_iterasi):
            ada_terbaik_baru = False

            for p in range(self.jumlah_partikel):
                jadwal, waktu_agen = self.position_to_schedule(self.posisi[p])
                durasi_total = max(waktu_agen.values(), default=0)
                indeks_keseimbangan = self.calculate_load_balance_index(waktu_agen)
                biaya = self.fungsi_biaya(jadwal, durasi_total)

                if biaya < self.biaya_pbest[p]:
                    self.biaya_pbest[p] = biaya
                    self.durasi_pbest[p] = durasi_total
                    self.posisi_pbest[p] = self.posisi[p].copy()

                if biaya < self.biaya_terbaik or (biaya == self.biaya_terbaik and indeks_keseimbangan < self.indeks_keseimbangan_terbaik):
                    self.biaya_terbaik = biaya
                    self.durasi_terbaik = durasi_total  # Simpan makespan aktual
                    self.jadwal_terbaik = jadwal
                    self.indeks_keseimbangan_terbaik = indeks_keseimbangan
                    self.posisi_gbest = self.posisi[p].copy()
                    ada_terbaik_baru = True

            if self.posisi_gbest is not None:
                for p in range(self.jumlah_partikel):
                    r1, r2 = np.random.rand(self.jumlah_tugas), np.random.rand(self.jumlah_tugas)
                    kognitif = self.c1 * r1 * (self.posisi_pbest[p] - self.posisi[p])
                    sosial = self.c2 * r2 * (self.posisi_gbest - self.posisi[p])
                    self.kecepatan[p] = self.w * self.kecepatan[p] + kognitif + sosial
                    self.posisi[p] += self.kecepatan[p]

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
        if self.posisi_gbest is not None:
            self.jadwal_terbaik, waktu_akhir_agen_final = self.position_to_schedule(self.posisi_gbest)

        waktu_komputasi = time.time() - waktu_mulai

        return {
            'schedule': pd.DataFrame(self.jadwal_terbaik) if self.jadwal_terbaik else pd.DataFrame(),
            'makespan': self.durasi_terbaik if self.durasi_terbaik != float('inf') else 0.0,
            'load_balance_index': self.indeks_keseimbangan_terbaik if self.indeks_keseimbangan_terbaik != float('inf') else 0.0,
            'agent_finish_times': waktu_akhir_agen_final,
            'computation_time': waktu_komputasi,
            'iteration_history': pd.DataFrame(self.riwayat_iterasi),
            'algorithm': self.__class__.__name__
        }


# Alias untuk kompatibilitas
PSOScheduler = PSO_MultiAgent_Scheduler
