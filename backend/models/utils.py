"""
Utility functions untuk Multi-Agent Task Scheduling.
Berisi fungsi helper untuk parsing, validasi, dan kalkulasi biaya.
"""

import pandas as pd
import random
import numpy as np


# ========== FUNGSI PARSING & CONVERSION ==========
def safe_convert_to_float(value, default=0.0):
    """
    Mengkonversi nilai ke float dengan penanganan error yang aman.
    
    Args:
        value (any): Nilai input.
        default (float, optional): Nilai default jika konversi gagal. Defaults to 0.0.
        
    Returns:
        float: Hasil konversi atau nilai default.
    """
    if value is None or value == '':
        return default
    if isinstance(value, str) and value.lower() in ['null', 'nan', 'none']:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def normalize_id(val):
    """
    Menormalisasi nilai ID menjadi string yang konsisten.
    
    Mengubah float 1.0 menjadi "1" untuk menghindari ketidakkonsistenan ID
    antara integer dan float.
    
    Args:
        val (any): Nilai ID input.
        
    Returns:
        str | None: String ID yang ternormalisasi atau None jika input None.
    """
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


def parse_dependensi(string_dep):
    """
    Memparse string yang berisi daftar dependensi menjadi list of strings.
    
    Mendukung pemisah koma (,) atau titik koma (;).
    
    Args:
        string_dep (str | any): String input representasi dependensi.
        
    Returns:
        list[str]: List ID dependensi yang valid.
    """
    if not string_dep:
        return []
    
    # Handle NaN/None directly
    if isinstance(string_dep, float) and pd.isna(string_dep):
        return []

    # If already list/tuple
    if isinstance(string_dep, (list, tuple)):
        return [str(item).strip() for item in string_dep if item is not None and str(item).strip() != '']

    s = str(string_dep)
    if s.lower() in ['nan', 'none', 'null', '']:
        return []
        
    parts = s.replace(';', ',').split(',')
    
    hasil = []
    for p in parts:
        p = p.strip()
        if p and p.lower() not in ['nan', 'none', 'null']:
            # Normalisasi ID jika bisa convert ke int
            try:
                val = float(p)
                if val.is_integer():
                    hasil.append(str(int(val)))
                else:
                    hasil.append(p)
            except ValueError:
                hasil.append(p)
    return hasil




# ========== GENERATE AGEN ==========
def generate_agen_default(jumlah_agen, agent_id_col='id'):
    """
    Membuat daftar agen default dengan karakteristik seragam (Homogen).
    
    Args:
        jumlah_agen (int): Jumlah agen yang ingin dibuat.
        agent_id_col (str, optional): Key untuk menyimpan ID agen. Defaults to 'id'.
        
    Returns:
        list[dict]: List dictionary yang merepresentasikan agen-agen.
    """
    if jumlah_agen <= 0:
        return []
    
    # Gunakan MODULO agar agen selalu identik di setiap run (deterministik)
    return [{
        agent_id_col: f'Agent-{i+1}',
        'type': 'Standard',
        'capacity': 1.0,
        'efficiency': 1.0
    } for i in range(jumlah_agen)]


# ========== COST & VALIDATION FUNCTIONS ==========
def hitung_load_balance_index(waktu_selesai_agen):
    """
    Menghitung indeks keseimbangan beban kerja antar agen.
    
    Menggunakan Coefficient of Variation (CV) dari waktu penyelesaian agen.
    
    Args:
        waktu_selesai_agen (dict): Mapping ID agen ke waktu selesai tugas terakhirnya.
        
    Returns:
        float: Indeks ketidakseimbangan (0.0 = seimbang sempurna).
    """
    if not waktu_selesai_agen:
        return 0.0
    times = list(waktu_selesai_agen.values())
    if len(times) <= 1:
        return 0.0
        
    mean_time = sum(times) / len(times)
    if mean_time == 0:
        return 0.0
        
    variance = sum((t - mean_time) ** 2 for t in times) / len(times)
    std_dev = variance ** 0.5
    return std_dev / mean_time


def fungsi_biaya_jadwal(jadwal, durasi_total, bobot_waktu=1.0, bobot_keseimbangan_beban=1.0):
    """
    Mengevaluasi kualitas keseluruhan jadwal (schedule) yang dihasilkan.
    
    Fungsi objektif ini menggabungkan total waktu penyelesaian (makespan)
    dan keseimbangan beban kerja antar agen.
    
    Args:
        jadwal (list[dict]): List penugasan yang berisi 'agent_id' dan 'finish_time'.
        durasi_total (float): Total waktu penyelesaian jadwal (makespan).
        bobot_waktu (float, optional): Bobot kepentingan waktu penyelesaian. Defaults to 1.0.
        bobot_keseimbangan_beban (float, optional): Bobot kepentingan keseimbangan beban. Defaults to 1.0.
        
    Returns:
        float: Nilai fitness/biaya jadwal (semakin kecil semakin baik).
    """
    if not jadwal:
        return float('inf')
    
    # Hitung waktu selesai per agen
    waktu_selesai = {}
    for penugasan in jadwal:
        id_agen = (penugasan.get('agent_id') or 
                   penugasan.get('id_agen') or 
                   penugasan.get('Agent_ID'))
        waktu_akhir = (penugasan.get('finish_time') or 
                       penugasan.get('waktu_selesai') or 
                       penugasan.get('Finish_Time') or 0)
        
        if id_agen is not None:
            waktu_selesai[id_agen] = max(waktu_selesai.get(id_agen, 0), waktu_akhir)
            
    # Hitung load balance
    keseimbangan = hitung_load_balance_index(waktu_selesai)
    
    # Hitung biaya total
    biaya = durasi_total * (bobot_waktu + bobot_keseimbangan_beban * keseimbangan)
    return max(0.1, biaya)


def buat_cost_function_untuk_scheduler(bobot_waktu=1.0, bobot_keseimbangan_beban=1.0):
    """
    Factory pattern untuk membuat fungsi biaya yang dikustomisasi dengan bobot tertentu.
    
    Args:
        bobot_waktu (float, optional): Bobot untuk makespan. Defaults to 1.0.
        bobot_keseimbangan_beban (float, optional): Bobot untuk load balance. Defaults to 1.0.
        
    Returns:
        callable: Fungsi cost yang menerima (jadwal, durasi_total).
    """
    def cost_function(jadwal, durasi_total):
        return fungsi_biaya_jadwal(jadwal, durasi_total, bobot_waktu, bobot_keseimbangan_beban)
    return cost_function


def ada_dependensi_sirkular(graf):
    """
    Mendeteksi apakah terdapat siklus (circular dependency) dalam graf tugas.
    
    Menggunakan algoritma DFS (Depth First Search) untuk melacak siklus.
    
    Args:
        graf (dict): Representasi graf adjacency list {node: [neighbors]}.
        
    Returns:
        bool: True jika ada siklus, False jika aman (DAG).
    """
    visited = set()
    recursion_stack = set()
    
    # Helper recursive
    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)
        
        if node in graf:
            for neighbor in graf[node]:
                if neighbor not in visited:
                    if dfs(neighbor): return True
                elif neighbor in recursion_stack:
                    return True
                    
        recursion_stack.remove(node)
        return False
        
    for node in graf:
        if node not in visited:
            if dfs(node): return True
    return False


def validasi_dependensi(daftar_tugas, task_id_col='id'):
    """
    Memvalidasi konsistensi dependensi antar tugas.
    
    Pemeriksaan meliputi:
    1. Dependensi ke tugas yang tidak ada (missing tasks).
    2. Self-dependency (tugas bergantung pada dirinya sendiri).
    3. Circular dependency (siklus A -> B -> A).
    
    Args:
        daftar_tugas (list[dict]): List data tugas.
        task_id_col (str, optional): Key untuk ID tugas. Defaults to 'id'.
        
    Returns:
        tuple[bool, list[str]]: (isValid, daftar_masalah).
    """
    id_tugas_set = {str(tugas.get(task_id_col, tugas.get('id', ''))) for tugas in daftar_tugas}
    masalah = []

    # Validasi existence & self-dep
    for tugas in daftar_tugas:
        tid = str(tugas.get(task_id_col, tugas.get('id', '')))
        deps = tugas.get('dependencies', []) or []
        if isinstance(deps, str): deps = [deps] # Safety

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
        # Hanya simpan dependensi yang ID-nya ada dalam graf
        graf[tid] = [str(d) for d in deps if str(d) in id_tugas_set and str(d) != tid]

    if ada_dependensi_sirkular(graf):
        masalah.append("Circular dependency detected")

    return len(masalah) == 0, masalah


def filter_ghost_dependencies(daftar_tugas, task_id_col='id'):
    """
    Membersihkan dependensi yang tidak valid (ghost dependencies) dari daftar tugas.
    
    Menghapus dependensi yang menunjuk ke ID yang tidak ada dalam daftar tugas,
    serta menghapus self-dependencies. Modifikasi dilakukan secara in-place.
    
    Args:
        daftar_tugas (list[dict]): List data tugas yang akan dibersihkan.
        task_id_col (str, optional): Key untuk ID tugas. Defaults to 'id'.
        
    Returns:
        int: Jumlah dependensi invalid yang dihapus.
    """
    valid_ids = {str(t.get(task_id_col, t.get('id', ''))) for t in daftar_tugas}
    count_removed = 0
    total_deps_before = 0
    
    for task in daftar_tugas:
        tid = str(task.get(task_id_col, task.get('id', '')))
        original_deps = task.get('dependencies', []) or []
        total_deps_before += len(original_deps)
        
        clean_deps = [
            d for d in original_deps 
            if str(d) in valid_ids and str(d) != tid
        ]
        
        if len(clean_deps) != len(original_deps):
            count_removed += len(original_deps) - len(clean_deps)
        
        task['dependencies'] = clean_deps
        
    return count_removed
