"""
Utility functions untuk Multi-Agent Task Scheduling.
Berisi fungsi helper untuk parsing, validasi, dan kalkulasi biaya.
"""

import pandas as pd
import random


# ========== FUNGSI HELPER ==========
def coba_ambil_nilai(obj, keys, default=None):
    """Coba ambil nilai dari dict dengan multiple key alternatif, return default jika tidak ada."""
    if not isinstance(obj, dict):
        return default
    for key in (keys if isinstance(keys, list) else [keys]):
        if key in obj and obj[key] is not None:
            # Handle NaN values
            try:
                if pd.notna(obj[key]):
                    return obj[key]
            except (TypeError, ValueError):
                return obj[key]
    return default


def dapatkan_id_tugas(tugas):
    """Dapatkan ID tugas dari berbagai format."""
    if not isinstance(tugas, dict):
        return str(tugas)
    nilai = coba_ambil_nilai(tugas, ['id', 'task_id', 'Task_ID', 'TaskID'])
    if nilai is not None:
        # Normalisasi: hilangkan desimal jika integer (1.0 -> "1")
        try:
            if isinstance(nilai, float) and nilai.is_integer():
                return str(int(nilai))
            if isinstance(nilai, (int, float)):
                return str(int(nilai))
        except (ValueError, TypeError):
            pass
        return str(nilai).strip()
    return str(random.randint(1000, 9999))


def dapatkan_id_agen(agen):
    """Dapatkan ID agen dari berbagai format."""
    if not isinstance(agen, dict):
        return str(agen)
    return coba_ambil_nilai(agen, ['id', 'agent_id', 'Agent_ID'], str(agen))


def dapatkan_durasi_tugas(tugas):
    """Dapatkan durasi tugas dari berbagai format."""
    if not isinstance(tugas, dict):
        return 1.0
    nilai = coba_ambil_nilai(tugas, [
        'duration', 'Duration', 'length', 'Length',
        'execution_time', 'execution_time (s)', 'Execution_Time',
        'Execution_Time (s)'
    ])
    if nilai is not None:
        try:
            return max(float(nilai), 0.1)
        except (ValueError, TypeError):
            pass
    return 1.0


def dapatkan_efisiensi_agen(agen):
    """Dapatkan efisiensi agen dari berbagai format."""
    if not isinstance(agen, dict):
        return 1.0
    nilai = coba_ambil_nilai(agen, ['efficiency', 'Efficiency', 'capacity', 'Capacity'])
    if nilai is not None:
        try:
            return max(float(nilai), 0.1)
        except (ValueError, TypeError):
            pass
    return 1.0


# ========== FUNGSI PARSING ==========
def parse_nilai(nilai, tipe_nilai=float, default=None, karakter_bersih=''):
    """Parse nilai dengan pembersihan karakter dan konversi tipe."""
    try:
        if nilai is None:
            return default
        if isinstance(nilai, float) and pd.isna(nilai):
            return default
        dibersihkan = str(nilai)
        for char in karakter_bersih:
            dibersihkan = dibersihkan.replace(char, '')
        return tipe_nilai(dibersihkan.strip())
    except (ValueError, TypeError):
        return default


def parse_dependensi(string_dep):
    """Parse string dependencies menjadi list."""
    if string_dep is None:
        return []
    
    try:
        if pd.isna(string_dep):
            return []
    except (TypeError, ValueError):
        pass
    
    if not str(string_dep).strip():
        return []

    dep_str = str(string_dep).strip()
    pemisah = ';' if ';' in dep_str else ','
    deps = [d.strip() for d in dep_str.split(pemisah) if d.strip()]

    # Filter nilai tidak valid
    nilai_tidak_valid = {'null', 'nan', 'none', ''}
    hasil = []
    for d in deps:
        if str(d).lower() not in nilai_tidak_valid:
            # Normalisasi ID (hilangkan desimal)
            try:
                val = float(d)
                if val.is_integer():
                    hasil.append(str(int(val)))
                else:
                    hasil.append(str(d))
            except (ValueError, TypeError):
                hasil.append(str(d))
    return hasil


def normalize_id(val):
    """Normalisasi ID ke string, hilangkan desimal jika angka bulat."""
    if val is None:
        return None
    try:
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        if isinstance(val, (int, float)):
            return str(int(val))
    except (ValueError, TypeError):
        pass
    return str(val).strip()


def safe_convert_to_float(value, default=0.0):
    """Konversi nilai ke float dengan aman."""
    if value is None or value == '':
        return default
    if isinstance(value, str) and value.lower() in ['null', 'nan', 'none']:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# ========== GENERATE AGEN ==========
def generate_agen_default(jumlah_agen, agent_id_col='id'):
    """
    Generate default agents dengan kapabilitas bervariasi (deterministik dengan modulo).
    
    Parameters:
    - jumlah_agen: Jumlah agen yang akan dibuat
    - agent_id_col: Nama kolom untuk ID agen
    
    Returns:
    - List of agent dictionaries
    """
    if jumlah_agen <= 0:
        return []

    tipe_agen = ['High_Performance', 'Medium_Performance', 'Standard', 'Basic']
    kapasitas = [1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]
    efisiensi = [1.2, 1.1, 1.0, 0.9, 0.8, 0.7]

    # Gunakan MODULO agar agen selalu identik di setiap run (deterministik)
    return [{
        agent_id_col: f'Agent-{i+1}',
        'type': tipe_agen[i % len(tipe_agen)],
        'capacity': kapasitas[i % len(kapasitas)],
        'efficiency': efisiensi[i % len(efisiensi)]
    } for i in range(jumlah_agen)]


# ========== FUNGSI BIAYA ==========
def fungsi_biaya_per_tugas(tugas, agen):
    """
    Fungsi biaya untuk menghitung cost assignment SATU tugas ke SATU agen.
    Digunakan untuk: Heuristic function di ACO, perhitungan individual.
    """
    # Ambil durasi tugas
    waktu_dasar = dapatkan_durasi_tugas(tugas)
    
    # Ambil efisiensi agen
    efisiensi_agen = coba_ambil_nilai(agen, ['efficiency', 'Efficiency'], 1.0) if isinstance(agen, dict) else 1.0
    efisiensi_agen = max(float(efisiensi_agen) if efisiensi_agen else 1.0, 0.1)
    
    # Ambil kapasitas agen
    kapasitas_agen = coba_ambil_nilai(agen, ['capacity', 'Capacity'], 1.0) if isinstance(agen, dict) else 1.0
    kapasitas_agen = max(float(kapasitas_agen) if kapasitas_agen else 1.0, 0.1)
    
    # Ambil kompleksitas tugas
    kompleksitas = 0.5
    if isinstance(tugas, dict):
        komp_val = tugas.get('complexity')
        if komp_val is not None:
            try:
                kompleksitas = float(komp_val)
            except (ValueError, TypeError):
                pass
        else:
            # Hitung dari CPU dan RAM jika ada
            cpu = safe_convert_to_float(
                coba_ambil_nilai(tugas, ['cpu_usage', 'CPU_Usage', 'cpu']), 0
            )
            ram = safe_convert_to_float(
                coba_ambil_nilai(tugas, ['ram_usage', 'RAM_Usage', 'ram']), 0
            )
            if cpu > 0 or ram > 0:
                kompleksitas = min(1.0, (cpu + ram/1000) / 200)
    
    # Hitung biaya efektif
    faktor_efektif = max(efisiensi_agen * kapasitas_agen, 0.1)
    biaya = (waktu_dasar * (1 + kompleksitas)) / faktor_efektif
    
    # Penalty untuk dependencies
    if isinstance(tugas, dict):
        dependensi = tugas.get('dependencies', []) or []
        biaya += len(dependensi) * 0.1
    
    return max(0.1, biaya)


def fungsi_biaya_jadwal(jadwal, durasi_total, bobot_waktu=1.0, bobot_keseimbangan_beban=1.0):
    """
    Fungsi biaya untuk mengevaluasi KESELURUHAN jadwal.
    Digunakan untuk: Evaluasi solusi di ACO dan PSO.
    
    Parameters:
    - jadwal: List of dict dengan keys 'agent_id' dan 'finish_time'
    - durasi_total: Total makespan atau durasi
    - bobot_waktu: Weight untuk durasi
    - bobot_keseimbangan_beban: Weight untuk load balance
    """
    if not jadwal:
        return float('inf')
    
    # Hitung waktu selesai per agen
    waktu_selesai = {}
    for penugasan in jadwal:
        # Support multiple key formats
        id_agen = (penugasan.get('agent_id') or 
                   penugasan.get('id_agen') or 
                   penugasan.get('Agent_ID'))
        waktu_akhir = (penugasan.get('finish_time') or 
                       penugasan.get('waktu_selesai') or 
                       penugasan.get('Finish_Time') or 0)
        
        if id_agen is not None:
            waktu_selesai[id_agen] = max(waktu_selesai.get(id_agen, 0), waktu_akhir)
    
    # Hitung load balance (coefficient of variation)
    waktu_list = list(waktu_selesai.values())
    if len(waktu_list) <= 1:
        keseimbangan = 0.0
    else:
        rata_rata = sum(waktu_list) / len(waktu_list)
        if rata_rata <= 0:
            keseimbangan = 0.0
        else:
            variansi = sum((t - rata_rata) ** 2 for t in waktu_list) / len(waktu_list)
            keseimbangan = (variansi ** 0.5) / rata_rata  # CV = std_dev / mean
    
    # Hitung biaya total
    biaya = durasi_total * (bobot_waktu + bobot_keseimbangan_beban * keseimbangan)
    return max(0.1, biaya)


def hitung_load_balance_index(waktu_selesai_agen):
    """
    Hitung indeks keseimbangan beban (coefficient of variation).
    
    Parameters:
    - waktu_selesai_agen: Dict mapping agent_id ke finish_time
    
    Returns:
    - Float: load balance index (0 = sempurna, lebih tinggi = lebih tidak seimbang)
    """
    times = list(waktu_selesai_agen.values())
    if len(times) <= 1:
        return 0.0
    waktu_rata = sum(times) / len(times)
    if waktu_rata == 0:
        return 0.0
    variance = sum((t - waktu_rata) ** 2 for t in times) / len(times)
    return (variance ** 0.5) / waktu_rata


def buat_cost_function_untuk_scheduler(bobot_waktu=1.0, bobot_keseimbangan_beban=1.0):
    """
    Factory function untuk membuat cost function yang kompatibel dengan scheduler.
    Mengembalikan fungsi yang signature-nya cocok dengan yang diharapkan scheduler.
    """
    def cost_function(jadwal, durasi_total):
        return fungsi_biaya_jadwal(jadwal, durasi_total, bobot_waktu, bobot_keseimbangan_beban)
    return cost_function


# ========== VALIDASI DEPENDENSI ==========
def ada_dependensi_sirkular(graf):
    """Deteksi circular dependency menggunakan DFS."""
    dikunjungi, stack_rekursi = set(), set()

    def dfs(node):
        if node in stack_rekursi:
            return True
        if node in dikunjungi:
            return False

        dikunjungi.add(node)
        stack_rekursi.add(node)

        for tetangga in graf.get(node, []):
            if dfs(tetangga):
                return True

        stack_rekursi.remove(node)
        return False

    return any(dfs(node) for node in graf if node not in dikunjungi)


def validasi_dependensi(daftar_tugas, task_id_col='id'):
    """
    Validasi dependencies dan deteksi circular dependencies.
    
    Returns:
    - Tuple (is_valid: bool, masalah: list)
    """
    id_tugas_set = {str(tugas.get(task_id_col, tugas.get('id', ''))) for tugas in daftar_tugas}
    masalah = []

    # Validasi existence
    for tugas in daftar_tugas:
        tid = str(tugas.get(task_id_col, tugas.get('id', '')))
        deps = tugas.get('dependencies', []) or []

        for dep in deps:
            dep_str = str(dep)
            if dep_str not in id_tugas_set:
                masalah.append(f"Task {tid} bergantung pada task tidak ada: {dep_str}")
            if dep_str == tid:
                masalah.append(f"Task {tid} memiliki self-dependency")

    # Build graph dan cek circular dependencies
    graf = {}
    for t in daftar_tugas:
        tid = str(t.get(task_id_col, t.get('id', '')))
        deps = t.get('dependencies', []) or []
        graf[tid] = [str(d) for d in deps if str(d) in id_tugas_set]

    if ada_dependensi_sirkular(graf):
        masalah.append("Circular dependency terdeteksi dalam task graph")

    return len(masalah) == 0, masalah


def filter_ghost_dependencies(daftar_tugas, task_id_col='id'):
    """
    Filter dependensi yang menunjuk ke task yang tidak ada (ghost dependencies).
    Modifikasi in-place dan return jumlah yang dihapus.
    """
    valid_ids = {str(t.get(task_id_col, t.get('id', ''))) for t in daftar_tugas}
    count_removed = 0
    total_deps_before = 0
    
    for task in daftar_tugas:
        tid = str(task.get(task_id_col, task.get('id', '')))
        original_deps = task.get('dependencies', []) or []
        total_deps_before += len(original_deps)
        
        # Filter: hanya simpan dependensi yang ID-nya ada dan bukan self-dependency
        clean_deps = [
            d for d in original_deps 
            if str(d) in valid_ids and str(d) != tid
        ]
        
        if len(clean_deps) != len(original_deps):
            count_removed += len(original_deps) - len(clean_deps)
        
        task['dependencies'] = clean_deps
    
    total_deps_after = total_deps_before - count_removed
    
    # Log lebih informatif
    if count_removed > 0:
        print(f"📊 Dependencies: {total_deps_after}/{total_deps_before} valid ({count_removed} ghost removed)")
    
    return count_removed


# Alias untuk backward compatibility
fungsi_biaya_universal = fungsi_biaya_per_tugas
