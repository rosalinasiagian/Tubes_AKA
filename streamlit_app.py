import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

# Fungsi iteratif untuk menghitung total penghasilan
@st.cache
def hitung_iteratif(data):
    total_penghasilan = 0
    for index, row in data.iterrows():
        total_penghasilan += row['Gaji_Pokok'] + row['Tunjangan'] + row['Bonus'] - row['Potongan']
    return total_penghasilan

# Fungsi rekursif untuk menghitung total penghasilan
def hitung_rekursif(data, index=0):
    if index == len(data):
        return 0
    row = data.iloc[index]
    return (row['Gaji_Pokok'] + row['Tunjangan'] + row['Bonus'] - row['Potongan']) + hitung_rekursif(data, index + 1)

# Simulasi data karyawan
def generate_data(jumlah):
    data = {
        "Karyawan_ID": [f"KRY{str(i).zfill(4)}" for i in range(1, jumlah + 1)],
        "Gaji_Pokok": [random.randint(2000000, 10000000) for _ in range(jumlah)],
        "Tunjangan": [random.randint(500000, 3000000) for _ in range(jumlah)],
        "Bonus": [random.randint(0, 2000000) for _ in range(jumlah)],
        "Potongan": [random.randint(0, 1000000) for _ in range(jumlah)],
    }
    return pd.DataFrame(data)

# Streamlit antarmuka utama
st.title("Penghitungan Penghasilan Bulanan Karyawan")

# Input jumlah karyawan
jumlah_karyawan = st.number_input("Masukkan jumlah karyawan:", min_value=10, max_value=10000, value=100)

# Inisialisasi variabel
if 'data_karyawan' not in st.session_state:
    st.session_state.data_karyawan = generate_data(jumlah_karyawan)
if 'time_iterative' not in st.session_state:
    st.session_state.time_iterative = 0
if 'time_recursive' not in st.session_state:
    st.session_state.time_recursive = 0

# Tombol untuk memulai perhitungan
if st.button("Hitung Total Penghasilan"):
    # Generate data karyawan
    st.session_state.data_karyawan = generate_data(jumlah_karyawan)

    # Perhitungan iteratif
    start_time_iterative = time.time()
    total_iterative = hitung_iteratif(st.session_state.data_karyawan)
    st.session_state.time_iterative = time.time() - start_time_iterative

    # Perhitungan rekursif
    start_time_recursive = time.time()
    total_recursive = hitung_rekursif(st.session_state.data_karyawan)
    st.session_state.time_recursive = time.time() - start_time_recursive

    # Tampilkan hasil
    st.write("### Hasil Perhitungan")
    st.write(f"Total Penghasilan (Iteratif): {total_iterative:,}")
    st.write(f"Waktu Eksekusi (Iteratif): {st.session_state.time_iterative:.6f} detik")
    st.write(f"Total Penghasilan (Rekursif): {total_recursive:,}")
    st.write(f"Waktu Eksekusi (Rekursif): {st.session_state.time_recursive:.6f} detik")

# Tampilkan tabel data
st.write("### Data Karyawan")
st.dataframe(st.session_state.data_karyawan)

# Membuat tabel perbandingan waktu eksekusi
comparison_data = {
    "Metode": ["Iteratif", "Rekursif"],
    "Waktu Eksekusi (detik)": [st.session_state.time_iterative, st.session_state.time_recursive]
}
comparison_df = pd.DataFrame(comparison_data)
st.write("### Tabel Perbandingan Waktu Eksekusi")
st.dataframe(comparison_df)

# Membuat grafik perbandingan waktu eksekusi
if st.session_state.time_iterative > 0 and st.session_state.time_recursive > 0:
    n_values = range(100, jumlah_karyawan + 1, 100)
    iterative_times = []
    recursive_times = []

    for n in n_values:
        data_sample = generate_data(n)
        
        start_time_iter = time.time()
        hitung_iteratif(data_sample)
        iterative_times.append(time.time() - start_time_iter)
        
        start_time_rec = time.time()
        hitung_rekursif(data_sample)
        recursive_times.append(time.time() - start_time_rec)
        
    # Plot grafik
    fig, ax = plt.subplots()
    ax.plot(n_values, iterative_times, marker='o', label='Iteratif', color='blue')
    ax.plot(n_values, recursive_times, marker='o', label='Rekursif', color='red')
    ax.set_xlabel("Nilai n")
    ax.set_ylabel("Waktu Eksekusi (detik)")
    ax.set_title("Perbandingan Waktu Eksekusi Iteratif vs Rekursif")
    ax.legend()
    st.pyplot(fig)
