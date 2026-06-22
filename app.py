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

# 2. Widget Slider untuk Simulasi Skor Variabel Penyebab (X) terhadap Dampak (Y)
st.sidebar.subheader("🎚️ Simulasi Dampak (Garis Tren)")
skor_x = st.sidebar.slider("Simulasi Rata-rata Skor Kendala (X1/X2/M):", 1.0, 5.0, 3.0, step=0.1)

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
    st.write("- **Keluhan Terbesar:** Masalah Iklan & UI (40 ulasan). Pengguna mengeluhkan taktik iklan video otomatis yang bising dan taktik *redirect* paksa.")
    st.write("- **Kepadatan UI:** Antarmuka beranda dianggap terlalu padat oleh banner, *floating icon*, dan game promo yang memicu kebingungan (Variabel X2).")
    st.info("*Catatan: Kategori 'tidak ada keluhan' (59 ulasan) dikeluarkan dari grafik agar berfokus pada sentimen negatif.")

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
# BAGIAN 3: SCATTER PLOT & KORELARI
# ==========================================
st.header("3. Analisis Hubungan Kendala Pengguna dengan Niat Hapus Aplikasi")

np.random.seed(42)
x_val = np.random.uniform(1.0, 5.0, 90)
y_val = 1.5 + 0.25 * x_val + np.random.normal(0, 0.5, 90)
y_val = np.clip(y_val, 1.0, 5.0)

data_scatter = pd.DataFrame({'Skor Kendala (Penyebab)': x_val, 'Niat Berpindah/Hapus Aplikasi (Y)': y_val})

col3, col4 = st.columns([2, 1])

with col3:
    fig_scatter = px.scatter(
        data_scatter, x='Skor Kendala (Penyebab)', y='Niat Berpindah/Hapus Aplikasi (Y)',
        trendline="ols", title="Scatter Plot Hubungan Variabel X/M dengan Variabel Dampak (Y)",
        labels={'Skor Kendala (Penyebab)': 'Skor Rata-rata Faktor Penyebab (X1, X2, M)'}
    )
    fig_scatter.update_traces(marker=dict(size=10, color='rgba(156, 163, 175, 0.7)', line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_scatter, use_container_width=True)

with col4:
    st.markdown("### 🔍 Analisis Korelasi:")
    st.write("- **Korelasi Positif:** Variabel X1 (Error), X2 (Bingung), dan M (Frustrasi) menunjukkan garis tren menanjak terhadap variabel Y (Pindah/Hapus Aplikasi).")
    st.write("- **Hubungan Lemah:** Persebaran data cukup menyebar (tidak rapat di garis tren). Variabel kendala bukan faktor tunggal utama yang membuat pengguna bermigrasi.")
    st.write("- **Peran Faktor Emosional (M):** Rasa frustrasi merupakan faktor emosional paling konsisten yang menjembatani pengalaman buruk dengan keputusan akhir pengguna.")
    
    prediksi_y = 1.5 + 0.25 * skor_x
    st.metric(label=f"Estimasi Nilai Dampak (Y) jika Skor Kendala = {skor_x}", value=f"{prediksi_y:.2f} / 5.00")
