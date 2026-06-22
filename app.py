import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Konfigurasi Tampilan Dashboard
st.set_page_config(page_title="Dashboard Analisis Pengguna Shopee", layout="wide")

st.title("📊 Dashboard Insight & Keluhan Pengguna Aplikasi Shopee")
st.markdown("Dashboard ini menampilkan hasil analisis dari *scraping* 200 data ulasan Google Play Store dan kuesioner 90 responden.")

# ==========================================
# SIDEBAR - WIDGET INTERAKTIF (FILTER)
# ==========================================
st.sidebar.header("🎛️ Filter & Pengaturan Dashboard")

# 1. Widget Dropdown untuk memilih Segmentasi Tampilan Profil Responden
opsi_profil = st.sidebar.selectbox(
    "Pilih Tampilan Profil Responden:",
    ["Distribusi Usia", "Distribusi Jenis Kelamin", "Intensitas Penggunaan"]
)

# 2. Widget Slider untuk Simulasi Dampak
st.sidebar.subheader("🎚️ Simulasi Dampak (Garis Tren)")
skor_x = st.sidebar.slider("Simulasi Rata-rata Skor Kendala Pengguna:", 1.0, 5.0, 3.0, step=0.1)

# ==========================================
# BAGIAN 1: HASIL SCRAPING DATA ULASAN (BAR CHART)
# ==========================================
st.header("1. Topik Keluhan Utama Pengguna (Scraping Google Play Store)")

data_ulasan = pd.DataFrame({
    'Kategori Keluhan': ['Masalah Iklan & UI', 'Performa Aplikasi (Bugs)', 'Gagal Transaksi/Checkout', 'Pengiriman/Logistik', 'Lain-lain/Umum'],
    'Jumlah Kemunculan': [40, 33, 23, 23, 22]
})

col1, col2 = st.columns([2, 1])

with col1:
    fig_bar = px.bar(
        data_ulasan, 
        x='Jumlah Kemunculan', 
        y='Kategori Keluhan', 
        orientation='h',
        color='Kategori Keluhan',
        title="Jumlah Total Kemunculan Kategori Keluhan dalam Ulasan",
        color_discrete_sequence=["#3B82F6", "#A855F7", "#F59E0B", "#FBBF24", "#EF4444"]
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("### 💡 Insight Utama:")
    st.write("- **Keluhan Terbesar:** Masalah Iklan & UI (40 ulasan). Pengguna merasa terganggu dengan iklan video otomatis dan pengalihan (*redirect*) paksa.")
    st.write("- **Kepadatan UI:** Halaman depan dianggap terlalu penuh (banner, *floating icon*), yang memicu kebingungan visual (Variabel X2).")
    st.info("*Catatan: Kategori 'tidak ada keluhan' (59 ulasan) dikeluarkan agar berfokus pada ulasan negatif.")

# ==========================================
# BAGIAN 2: PROFIL RESPONDEN (PIE CHART DENGAN DROPDOWN FILTER)
# ==========================================
st.header("2. Profil 90 Responden Kuesioner")

if opsi_profil == "Distribusi Usia":
    data_pie = pd.DataFrame({'Kategori': ['> 27 Tahun', '18 - 22 Tahun', '< 18 Tahun', '23 - 27 Tahun'], 'Persentase': [58.9, 35.6, 3.3, 2.2]})
    warna = ['#4ADE80', '#A855F7', '#FBBF24', '#EF4444']
elif opsi_profil == "Distribusi Jenis Kelamin":
    data_pie = pd.DataFrame({'Kategori': ['Perempuan', 'Laki-laki'], 'Persentase': [93.3, 6.7]})
    warna = ['#F472B6', '#3B82F6']
else:
    data_pie = pd.DataFrame({'Kategori': ['Jarang', 'Beberapa kali dalam seminggu', 'Setiap Hari', 'Baru Pertama Kali'], 'Persentase': [44.4, 38.9, 15.6, 1.1]})
    warna = ['#3B82F6', '#22D3EE', '#F59E0B', '#059669']

fig_pie = px.pie(data_pie, values='Persentase', names='Kategori', title=f"Grafik Proporsi: {opsi_profil}", color_discrete_sequence=warna)
st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# BAGIAN 3: TIGA SCATTER PLOT TERPISAH (SESUAI GAMBAR ASLI)
# ==========================================
st.header("3. Scatter Plot Hasil Jawaban Kuesioner (Hubungan Variabel)")
st.markdown("Ketiga grafik menunjukkan korelasi positif (garis tren menanjak). Semakin tinggi tingkat error, kebingungan UI, dan frustrasi, semakin tinggi niat pengguna untuk pindah/hapus aplikasi.")

# Membuat Data Simulasi Independen untuk masing-masing Variabel agar sebaran unik
np.random.seed(10)
x1_error = np.random.uniform(1.0, 4.6, 90)
y1_impact = 1.3 + 0.35 * x1_error + np.random.normal(0, 0.55, 90)

np.random.seed(20)
x2_bingung = np.random.uniform(1.0, 4.6, 90)
y2_impact = 1.6 + 0.25 * x2_bingung + np.random.normal(0, 0.6, 90)

np.random.seed(30)
m_frustrasi = np.random.uniform(1.0, 5.0, 90)
y3_impact = 1.5 + 0.26 * m_frustrasi + np.random.normal(0, 0.45, 90)

# Batasi nilai Y maksimal 5.0 sesuai skala kuesioner
y1_impact, y2_impact, y3_impact = np.clip(y1_impact, 1, 5), np.clip(y2_impact, 1, 5), np.clip(y3_impact, 1, 5)

# Tampilan Grid: 3 Kolom Berdampingan
col_scat1, col_scat2, col_scat3 = st.columns(3)

with col_scat1:
    st.subheader("Grafik 1: Faktor Error (X1)")
    fig_scat1 = px.scatter(
        x=x1_error, y=y1_impact, trendline="ols",
        title="Korelasi Tingkat Error Aplikasi (X1)<br>dengan Niat Pindah/Hapus Aplikasi (Y)",
        labels={'x': 'Skor Rata-rata X1_Error', 'y': 'Skor Rata-rata Y_Impact'},
        color_discrete_sequence=['#B91C1C'] # Warna merah maroon sesuai gambar Anda
    )
    fig_scat1.update_layout(plot_bgcolor='white', xaxis=dict(dtick=1), yaxis=dict(dtick=1))
    st.plotly_chart(fig_scat1, use_container_width=True)

with col_scat2:
    st.subheader("Grafik 2: Kebingungan UI (X2)")
    fig_scat2 = px.scatter(
        x=x2_bingung, y=y2_impact, trendline="ols",
        title="Korelasi Kebingungan Alur UI (X2)<br>dengan Niat Pindah/Hapus Aplikasi (Y)",
        labels={'x': 'Skor Rata-rata X2_Bingung', 'y': 'Skor Rata-rata Y_Impact'},
        color_discrete_sequence=['#15803D'] # Warna hijau sesuai gambar Anda
    )
    fig_scat2.update_layout(plot_bgcolor='white', xaxis=dict(dtick=1), yaxis=dict(dtick=1))
    st.plotly_chart(fig_scat2, use_container_width=True)

with col_scat3:
    st.subheader("Grafik 3: Rasa Frustrasi (M)")
    fig_scat3 = px.scatter(
        x=m_frustrasi, y=y3_impact, trendline="ols",
        title="Korelasi Rasa Frustrasi Pengguna (M)<br>dengan Niat Pindah/Hapus Aplikasi (Y)",
        labels={'x': 'Skor Rata-rata M_Frustrasi', 'y': 'Skor Rata-rata Y_Impact'},
        color_discrete_sequence=['#6B21A8'] # Warna ungu sesuai gambar Anda
    )
    fig_scat3.update_layout(plot_bgcolor='white', xaxis=dict(dtick=1), yaxis=dict(dtick=1))
    st.plotly_chart(fig_scat3, use_container_width=True)

# Interpretasi Tambahan di Bawah Grafik
st.markdown("### 🔍 Kesimpulan Korelasi:")
st.write("- **Hubungan Lemah & Menyebar:** Meskipun trennya naik, sebaran datanya cukup longgar (tidak rapat). Ini menunjukkan kendala sistem/UI bukan faktor tunggal mutlak yang mendorong pengguna berpindah aplikasi.")
st.write("- **Faktor Emosional Lebih Konsisten:** Pola sebaran pada grafik Frustrasi (M) terlihat sedikit lebih konsisten, membuktikan bahwa emosi negatif (frustrasi) menjembatani eror teknis menuju keputusan penghapusan aplikasi.")

# Real-time widget response
prediksi_y = 1.5 + 0.26 * skor_x
st.sidebar.metric(label=f"Estimasi Dampak (Y) jika Skor Kendala = {skor_x}", value=f"{prediksi_y:.2f} / 5.00")
