import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit agar lebar
st.set_page_config(page_title="Dashboard Analisis Kualitas Udara Aotizhongxin", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara Stasiun Aotizhongxin 🌍")
st.markdown("---")

# Memuat data bersih
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    # Pastikan kolom tanggal diubah ke datetime jika ingin menggunakan date_input
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    return df

df = load_data()

# --- SIDEBAR: KOMPONEN INTERAKTIF SESUAI PERMINTAAN REVIEWER ---
st.sidebar.header("Filter Interaktif Dashboard 🔍")

# 1. st.date_input() untuk menyaring data berdasarkan rentang tanggal
min_date = df['datetime'].min().date()
max_date = df['datetime'].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Pilih Periode Waktu:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 2. st.selectbox() untuk memilih tahun tertentu
years = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun Pengamatan:", options=['Semua Tahun'] + list(years))

# 3. st.slider() untuk rentang kecepatan angin (WSPM)
min_wspm = float(df['WSPM'].min())
max_wspm = float(df['WSPM'].max())
selected_wspm = st.sidebar.slider(
    "Rentang Kecepatan Angin (WSPM):",
    min_value=min_wspm,
    max_value=max_wspm,
    value=(min_wspm, max_wspm)
)

# --- PENERAPAN FILTER KE DATAFRAME ---
filtered_df = df[
    (df['datetime'].dt.date >= start_date) & 
    (df['datetime'].dt.date <= end_date) & 
    (df['WSPM'] >= selected_wspm[0]) & 
    (df['WSPM'] <= selected_wspm[1])
]

if selected_year != 'Semua Tahun':
    filtered_df = filtered_df[filtered_df['year'] == selected_year]


# --- KOTAK METRIK UTAMA (KPI) ---
col1, col2, col3 = st.columns(3)
with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25:.2f} µg/m³" if not pd.isna(avg_pm25) else "0")
with col2:
    avg_pm10 = filtered_df['PM10'].mean()
    st.metric("Rata-rata PM10", value=f"{avg_pm10:.2f} µg/m³" if not pd.isna(avg_pm10) else "0")
with col3:
    avg_wspm = filtered_df['WSPM'].mean()
    st.metric("Rata-rata Kecepatan Angin", value=f"{avg_wspm:.2f} m/s" if not pd.isna(avg_wspm) else "0")

st.markdown("---")


# --- VISUALISASI 1: Tren Rata-rata PM2.5 per Tahun ---
st.subheader("1. Tren Rata-rata Konsentrasi PM2.5 dari Tahun ke Tahun")
pm25_yearly = df.groupby('year')['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pm25_yearly['year'], pm25_yearly['PM2.5'], marker='o', color='b', linewidth=2, linestyle='-')
ax.set_title("Rata-rata PM2.5 per Tahun (2013-2017)")
ax.set_xlabel("Tahun")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.grid(True)
st.pyplot(fig)


# --- VISUALISASI 2: Hubungan Kecepatan Angin (WSPM) dan PM10 (Dinamis) ---
st.subheader("2. Hubungan Kecepatan Angin (WSPM) dan Konsentrasi PM10")
st.write(f"Menampilkan data tersaring (Periode: {start_date} s.d. {end_date} | Tahun: {selected_year})")

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='WSPM', y='PM10', data=filtered_df, alpha=0.4, color='purple', ax=ax)
ax.set_title("Scatter Plot WSPM vs PM10 Berdasarkan Filter")
ax.set_xlabel("Kecepatan Angin (WSPM)")
ax.set_ylabel("Konsentrasi PM10")
st.pyplot(fig)