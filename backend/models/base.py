import numpy as np
import random
import json
import pandas as pd
import time

class MultiAgentScheduler:
    """Kelas dasar untuk penjadwalan tugas multi-agen dengan utilitas bersama."""

    def __init__(self, tasks, agents, cost_function, task_id_col='id', agent_id_col='id',
                 enable_dependencies=False, random_seed=None, num_default_agents=3):
        # Konversi input ke list jika DataFrame
        self.tugas = tasks.to_dict('records') if isinstance(tasks, pd.DataFrame) else tasks
        
        # Generate default agents dengan heterogenitas (seperti notebook)
        if agents is None or (isinstance(agents, list) and len(agents) == 0):
            self.agen = self._generate_default_agents(num_default_agents, agent_id_col)
        else:
            self.agen = agents.to_dict('records') if isinstance(agents, pd.DataFrame) else agents

        self.fungsi_biaya = cost_function
        self.task_id_col = task_id_col
        self.agent_id_col = agent_id_col
        self.enable_dependencies = enable_dependencies
        self.jumlah_tugas = len(self.tugas)
        self.jumlah_agen = len(self.agen)

        if self.jumlah_tugas == 0:
            print("Peringatan: Tidak ada tugas yang diberikan. Scheduler tidak akan berjalan.")

        # Penanganan dependensi
        self.peta_tugas = {str(task[self.task_id_col]): i for i, task in enumerate(self.tugas)}
        self.peta_tugas_terbalik = {i: str(task[self.task_id_col]) for i, task in enumerate(self.tugas)}
        self.dependensi = self.parse_dependencies() if enable_dependencies and self.jumlah_tugas > 0 else {}
        self.graf_dependensi = self.build_dependency_graph() if enable_dependencies and self.jumlah_tugas > 0 else None

        if enable_dependencies and self.jumlah_tugas > 0 and self.detect_circular_dependencies():
            print("Peringatan: Dependensi sirkular terdeteksi. Menggunakan fallback.")

        # Random seed
        if random_seed is not None:
            np.random.seed(random_seed)
            random.seed(random_seed)

        # Pelacakan
        self.jadwal_terbaik = None
        self.biaya_terbaik = float('inf')
        self.indeks_keseimbangan_terbaik = float('inf')
        self.riwayat_iterasi = []

    def _generate_default_agents(self, jumlah_agen, agent_id_col):
        """Generate default agents dengan kapabilitas bervariasi (sesuai notebook)."""
        if jumlah_agen <= 0:
            return []
        
        tipe_agen = ['High_Performance', 'Medium_Performance', 'Standard', 'Basic']
        kapasitas = [1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]
        efisiensi = [1.2, 1.1, 1.0, 0.9, 0.8, 0.7]
        
        return [{
            agent_id_col: f'Agent-{i+1}',
            'type': tipe_agen[i % len(tipe_agen)],
            'capacity': random.choice(kapasitas),
            'efficiency': random.choice(efisiensi)
        } for i in range(jumlah_agen)]

    def parse_dependencies(self):
        """Parse dependensi secara robust."""
        dependensi = {}
        for tugas in self.tugas:
            id_tugas = str(tugas[self.task_id_col])
            deps = None
            for field in ['dependencies', 'depends_on', 'prerequisites', 'requires', 'Dependencies']:
                if field in tugas and tugas[field] is not None:
                    deps = tugas[field]
                    break
            if deps:
                if isinstance(deps, str):
                    deps = [str(d).strip() for d in deps.replace(';', ',').split(',') if d.strip() and str(d).lower() not in ['null', 'nan', 'none', '']]
                elif isinstance(deps, (list, tuple)):
                    deps = [str(d).strip() for d in deps if d is not None and str(d).strip() and str(d).lower() not in ['null', 'nan', 'none']]
                else:
                    deps = [str(deps).strip()] if str(deps).strip() and str(deps).lower() not in ['null', 'nan', 'none'] else []
            dependensi[id_tugas] = deps or []
        return dependensi

    def build_dependency_graph(self):
        """Membangun graf dependensi."""
        return {id_tugas: self.dependensi[id_tugas] for id_tugas in self.dependensi}

    def detect_circular_dependencies(self):
        """Deteksi siklus menggunakan DFS."""
        if not self.enable_dependencies or self.jumlah_tugas == 0:
            return False
        visited, rec_stack = set(), set()
        def has_cycle(id_tugas):
            if id_tugas in rec_stack:
                return True
            if id_tugas in visited:
                return False
            visited.add(id_tugas)
            rec_stack.add(id_tugas)
            for dep_id in self.dependensi.get(id_tugas, []):
                if has_cycle(dep_id):
                    return True
            rec_stack.remove(id_tugas)
            return False
        for id_tugas in self.dependensi:
            if id_tugas not in visited and has_cycle(id_tugas):
                return True
        return False

    def is_dependency_satisfied(self, id_tugas, tugas_selesai):
        """Cek apakah dependensi terpenuhi."""
        return all(dep_id in tugas_selesai for dep_id in self.dependensi.get(id_tugas, []))

    def get_ready_tasks(self, tugas_tersisa, tugas_selesai):
        """Dapatkan tugas yang siap dijalankan."""
        if not self.enable_dependencies:
            return tugas_tersisa
        return [idx for idx in tugas_tersisa if self.is_dependency_satisfied(self.peta_tugas_terbalik[idx], tugas_selesai)]

    def calculate_load_balance_index(self, waktu_selesai_agen):
        """Hitung indeks keseimbangan beban."""
        times = list(waktu_selesai_agen.values())
        if len(times) <= 1:
            return 0.0
        waktu_rata = sum(times) / len(times)
        if waktu_rata == 0:
            return 0.0
        variance = sum((t - waktu_rata) ** 2 for t in times) / len(times)
        return (variance ** 0.5) / waktu_rata

    def find_best_agent(self, waktu_selesai_agen, durasi_tugas, id_tugas=None, waktu_selesai_tugas=None, prioritize_balance=True):
        """Temukan agen terbaik untuk tugas."""
        if not waktu_selesai_agen:
            return self.agen[0][self.agent_id_col] if self.agen else None

        agen_terbaik = None
        skor_terbaik = float('inf')
        max_saat_ini = max(waktu_selesai_agen.values(), default=0)

        waktu_dep_selesai = 0
        if self.enable_dependencies and id_tugas and waktu_selesai_tugas:
            dep_finish_times = [waktu_selesai_tugas.get(dep_id, 0) for dep_id in self.dependensi.get(id_tugas, [])]
            waktu_dep_selesai = max(dep_finish_times) if dep_finish_times else 0

        for agen in self.agen:
            id_agen = agen[self.agent_id_col]
            waktu_temp = waktu_selesai_agen.copy()
            waktu_mulai = max(waktu_temp.get(id_agen, 0), waktu_dep_selesai)
            waktu_temp[id_agen] = waktu_mulai + durasi_tugas
            durasi_total_baru = max(waktu_temp.values())

            if prioritize_balance:
                skor_keseimbangan = self.calculate_load_balance_index(waktu_temp)
                skor = skor_keseimbangan * 1000 + (durasi_total_baru / 1000)
            else:
                penalti_keseimbangan = self.calculate_load_balance_index(waktu_temp) * max_saat_ini * 2
                skor = durasi_total_baru + penalti_keseimbangan

            if skor < skor_terbaik:
                skor_terbaik = skor
                agen_terbaik = id_agen

        return agen_terbaik or min(waktu_selesai_agen, key=waktu_selesai_agen.get, default=self.agen[0][self.agent_id_col] if self.agen else None)

    def assign_to_agents(self, urutan_indeks_tugas):
        """Assign tugas ke agen."""
        if not self.agen or (isinstance(urutan_indeks_tugas, np.ndarray) and urutan_indeks_tugas.size == 0) or (isinstance(urutan_indeks_tugas, list) and not urutan_indeks_tugas):
            return [], {}, 0.0

        waktu_selesai_agen = {agen[self.agent_id_col]: 0 for agen in self.agen}
        waktu_selesai_tugas = {}
        jadwal = []

        for indeks_tugas in urutan_indeks_tugas:
            tugas = self.tugas[indeks_tugas]
            id_tugas = str(tugas[self.task_id_col])
            durasi = tugas.get('length', tugas.get('duration', 1))

            agen_terbaik = self.find_best_agent(waktu_selesai_agen, durasi, id_tugas, waktu_selesai_tugas)
            if agen_terbaik is None:
                continue

            waktu_dep_selesai = 0
            if self.enable_dependencies and id_tugas in self.dependensi:
                dep_finish_times = [waktu_selesai_tugas.get(dep_id, 0) for dep_id in self.dependensi[id_tugas]]
                waktu_dep_selesai = max(dep_finish_times) if dep_finish_times else 0

            waktu_mulai = max(waktu_selesai_agen[agen_terbaik], waktu_dep_selesai)
            waktu_akhir = waktu_mulai + durasi
            waktu_selesai_agen[agen_terbaik] = waktu_akhir
            waktu_selesai_tugas[id_tugas] = waktu_akhir

            jadwal.append({'task_id': id_tugas, 'agent_id': agen_terbaik, 'start_time': waktu_mulai, 'finish_time': waktu_akhir})

        durasi_total = max(waktu_selesai_agen.values(), default=0)
        keseimbangan_beban = self.calculate_load_balance_index(waktu_selesai_agen)
        return jadwal, waktu_selesai_agen, keseimbangan_beban

    def optimize(self, n_iterations=100, show_progress=True, progress_callback=None):
        """Metode optimasi utama."""
        if self.jumlah_tugas == 0 or self.jumlah_agen == 0:
            if show_progress:
                print("Tidak dapat berjalan: Tidak ada tugas atau agen.")
            return {
                'schedule': pd.DataFrame(), 'makespan': 0.0, 'load_balance_index': 0.0,
                'agent_finish_times': {}, 'computation_time': 0.0,
                'iteration_history': pd.DataFrame(), 'algorithm': self.__class__.__name__
            }

        waktu_mulai = time.time()
        if show_progress:
            print(f"Memulai optimasi {self.__class__.__name__}...")

        # Inisialisasi jadwal dan biaya terbaik
        urutan_awal = list(range(self.jumlah_tugas))
        jadwal_awal, waktu_agen_awal, keseimbangan_awal = self.assign_to_agents(urutan_awal)
        durasi_total_awal = max(waktu_agen_awal.values(), default=0)
        self.biaya_terbaik = self.fungsi_biaya(jadwal_awal, durasi_total_awal)
        self.jadwal_terbaik = jadwal_awal
        self.indeks_keseimbangan_terbaik = keseimbangan_awal

        for i in range(n_iterations):
            # Subclass mengimplementasikan logika spesifik di sini
            pass

        waktu_komputasi = time.time() - waktu_mulai
        waktu_akhir_agen = {}
        if self.jadwal_terbaik:
            for penugasan in self.jadwal_terbaik:
                waktu_akhir_agen[penugasan['agent_id']] = max(waktu_akhir_agen.get(penugasan['agent_id'], 0), penugasan['finish_time'])

        return {
            'schedule': pd.DataFrame(self.jadwal_terbaik) if self.jadwal_terbaik else pd.DataFrame(),
            'makespan': self.biaya_terbaik if self.biaya_terbaik != float('inf') else 0.0,
            'load_balance_index': self.indeks_keseimbangan_terbaik if self.indeks_keseimbangan_terbaik != float('inf') else 0.0,
            'agent_finish_times': waktu_akhir_agen,
            'computation_time': waktu_komputasi,
            'iteration_history': pd.DataFrame(self.riwayat_iterasi),
            'algorithm': self.__class__.__name__
        }

    def run(self):
        """Jalankan optimasi dengan yield progress secara real-time menggunakan threading."""
        import json
        import threading
        import queue
        import time
        
        # Queue untuk komunikasi antar thread
        progress_queue = queue.Queue()
        result_container = {'result': None, 'error': None}
        
        # Callback untuk mengirim progress ke queue
        def progress_callback(data):
            iteration = float(data["iteration"])
            makespan = float(data["best_makespan"])
            progress_queue.put(json.dumps({
                "type": "iteration", 
                "iteration": iteration, 
                "makespan": makespan,
                "log_message": f"Iteration {int(iteration)}: Best Makespan = {makespan:.2f}s"
            }))
        
        # Function untuk menjalankan optimize di thread terpisah
        def run_optimize():
            try:
                result_container['result'] = self.optimize(show_progress=False, progress_callback=progress_callback)
            except Exception as e:
                result_container['error'] = e
            finally:
                # Sinyal bahwa optimasi selesai
                progress_queue.put(None)
        
        # Mulai thread optimasi
        thread = threading.Thread(target=run_optimize, daemon=True)
        thread.start()
        
        # Yield progress secara real-time dari queue
        while True:
            try:
                # Timeout untuk menghindari blocking forever
                item = progress_queue.get(timeout=1.0)
                
                if item is None:
                    # Sinyal selesai
                    break
                    
                yield item
                
            except queue.Empty:
                # Tidak ada data, cek apakah thread masih hidup
                if not thread.is_alive():
                    break
                continue
        
        # Tunggu thread selesai
        thread.join(timeout=5.0)
        
        # Check for errors
        if result_container['error']:
            raise result_container['error']
        
        # Yield hasil akhir
        hasil = result_container['result']
        if hasil:
            final_makespan = float(hasil["makespan"])
            computation_time = float(hasil.get("computation_time", 0)) * 1000  # Convert to ms
            
            # Convert iteration_history from DataFrame to list of records
            iteration_history = []
            if "iteration_history" in hasil and not hasil["iteration_history"].empty:
                iteration_history = hasil["iteration_history"].to_dict("records")
            
            yield json.dumps({
                "type": "done", 
                "schedule": hasil["schedule"].to_dict("records"), 
                "makespan": final_makespan, 
                "load_balance_index": float(hasil["load_balance_index"]), 
                "agent_finish_times": hasil["agent_finish_times"],
                "computation_time": computation_time,
                "iteration_history": iteration_history,
                "log_message": f"Optimization complete! Best Makespan: {final_makespan:.2f}s (computed in {computation_time:.2f}ms)"
            })
