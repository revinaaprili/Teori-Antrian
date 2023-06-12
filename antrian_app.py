import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function untuk menghitung teori antrian finite
def finite_queue(lam, mu, c, k):
    rho = lam / (c * mu)
    if rho >= 1:
        return "Rho harus lebih kecil dari 1"
    
    p0 = (1 - rho) / (1 - rho**(k+1)) # Probabilitas tidak ada pelanggan di sistem
    pk = rho**k * p0 # Probabilitas ada k pelanggan di sistem
    lq = (rho * (1 - (k+1) * rho**k + k * rho**(k+1))) / ((1 - rho) * (1 - rho**(k+1))) # Rata-rata pelanggan di antrian
    wq = lq / (lam * (1 - pk)) # Waktu tunggu rata-rata di antrian
    ws = wq + 1 / mu # Waktu tinggal rata-rata di sistem
    l = lam * ws # Rata-rata pelanggan di sistem
    w = l / lam # Waktu rata-rata di sistem
    
    return lq, wq, ws, l, w

# Function untuk menghitung teori antrian infinite (M/M/1)
def infinite_queue(lam, mu):
    rho = lam / mu
    if rho >= 1:
        return "Rho harus lebih kecil dari 1"
    
    lq = rho**2 / (1 - rho) # Rata-rata pelanggan di antrian
    wq = lq / lam # Waktu tunggu rata-rata di antrian
    ws = wq + 1 / mu # Waktu tinggal rata-rata di sistem
    l = lam * ws # Rata-rata pelanggan di sistem
    w = l / lam # Waktu rata-rata di sistem
    
    return lq, wq, ws, l, w

# Navigasi menu
def main():
    st.sidebar.title("Menu")
    options = ["Pengertian", "Teori Antrian Finite", "Teori Antrian Infinite"]
    choice = st.sidebar.radio("Pilih jenis teori antrian:", options)

    st.title("Kalkulator Teori Antrian")
    st.write("Pilih jenis teori antrian di sidebar kiri.")

    if choice == "Pengertian":
        st.header("Pengertian Teori Antrian")
        st.write("Teori Antrian adalah cabang ilmu statistik yang mempelajari perilaku antrian atau antrean dalam sistem yang melibatkan kedatangan pelanggan, proses layanan, dan keadaan antrian. Teori Antrian digunakan untuk menganalisis dan memodelkan sistem antrian guna memahami dan mengoptimalkan kinerja sistem tersebut. Beberapa istilah dalam teori antrian antara lain:")
        st.write("- Intensitas kedatangan ($\lambda$): Jumlah pelanggan yang datang dalam satuan waktu")
        st.write("- Intensitas layanan ($\mu$): Jumlah pelanggan yang dilayani dalam satuan waktu")
        st.write("- Jumlah server ($c$): Jumlah server yang tersedia untuk melayani pelanggan")
        st.write("- Kapasitas antrian ($k$): Jumlah maksimum pelanggan yang dapat mengantri sebelum ditolak")
        st.write("- Rho ($\rho$): Rasio antara intensitas kedatangan dan intensitas layanan ($\rho = \lambda / (c \cdot \mu)$)")
        
    elif choice == "Teori Antrian Finite":
        st.header("Teori Antrian Finite (M/M/c/k)")
        st.markdown("Rumus-rumus pada Teori Antrian Finite:")
        st.latex(r'''
        \begin{align*}
        \text{Probabilitas tidak ada pelanggan di sistem (}p_0\text{)} &= \frac{1 - \rho}{1 - \rho^{k+1}} \\
        \text{Probabilitas ada k pelanggan di sistem (}p_k\text{)} &= \rho^k \cdot p_0 \\
        \text{Rata-rata pelanggan di antrian (}L_q\text{)} &= \frac{\rho \cdot (1 - (k+1) \cdot \rho^k + k \cdot \rho^{k+1})}{(1 - \rho) \cdot (1 - \rho^{k+1})} \\
        \text{Waktu tunggu rata-rata di antrian (}W_q\text{)} &= \frac{L_q}{\lambda \cdot (1 - p_k)} \\
        \text{Waktu tinggal rata-rata di sistem (}W_s\text{)} &= W_q + \frac{1}{\mu} \\
        \text{Rata-rata pelanggan di sistem (}L\text{)} &= \lambda \cdot W_s \\
        \text{Waktu rata-rata di sistem (}W\text{)} &= \frac{L}{\lambda}
        \end{align*}
        ''')

        lam = st.number_input("Intensitas kedatangan ($\lambda$):", value=1.0)
        mu = st.number_input("Intensitas layanan ($\mu$):", value=1.0)
        c = st.number_input("Jumlah server ($c$):", value=1)
        k = st.number_input("Kapasitas antrian ($k$):", value=1)

        if st.button("Hitung"):
            lq, wq, ws, l, w = finite_queue(lam, mu, c, k)
            st.subheader("Hasil Perhitungan:")
            st.write(f"Rata-rata pelanggan di antrian ($L_q$): {lq}")
            st.write(f"Waktu tunggu rata-rata di antrian ($W_q$): {wq}")
            st.write(f"Waktu tinggal rata-rata di sistem ($W_s$): {ws}")
            st.write(f"Rata-rata pelanggan di sistem ($L$): {l}")
            st.write(f"Waktu rata-rata di sistem ($W$): {w}")

    elif choice == "Teori Antrian Infinite":
        st.header("Teori Antrian Infinite (M/M/1)")
        st.markdown("Rumus-rumus pada Teori Antrian Infinite:")
        st.latex(r'''
        \begin{align*}
        \text{Rata-rata pelanggan di antrian (}L_q\text{)} &= \frac{\rho^2}{1 - \rho} \\
        \text{Waktu tunggu rata-rata di antrian (}W_q\text{)} &= \frac{L_q}{\lambda} \\
        \text{Waktu tinggal rata-rata di sistem (}W_s\text{)} &= W_q + \frac{1}{\mu} \\
        \text{Rata-rata pelanggan di sistem (}L\text{)} &= \lambda \cdot W_s \\
        \text{Waktu rata-rata di sistem (}W\text{)} &= \frac{L}{\lambda}
        \end{align*}
        ''')

        lam = st.number_input("Intensitas kedatangan ($\lambda$):", value=1.0)
        mu = st.number_input("Intensitas layanan ($\mu$):", value=1.0)

        if st.button("Hitung"):
            lq, wq, ws, l, w = infinite_queue(lam, mu)
            st.subheader("Hasil Perhitungan:")
            st.write(f"Rata-rata pelanggan di antrian ($L_q$): {lq}")
            st.write(f"Waktu tunggu rata-rata di antrian ($W_q$): {wq}")
            st.write(f"Waktu tinggal rata-rata di sistem ($W_s$): {ws}")
            st.write(f"Rata-rata pelanggan di sistem ($L$): {l}")
            st.write(f"Waktu rata-rata di sistem ($W$): {w}")

if __name__ == '__main__':
    main()
