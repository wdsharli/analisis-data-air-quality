import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis Kualitas Udara", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara Stasiun Aotizhongxin 🌍")

# Memuat data bersih
@st.cache_data
def load_data():
    # Mendapatkan direktori tempat file dashboard.py ini berada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Menggabungkan direktori tersebut dengan nama file CSV
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path)
    return df

df_cleaned = load_data()

# --- SIDEBAR: FITUR INTERAKTIF ---
st.sidebar.header("Filter Interaktif 🔍")

# 1. st.date_input() untuk menyaring data berdasarkan rentang tanggal
min_date = df_cleaned['datetime'].min().date()
max_date = df_cleaned['datetime'].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Pilih Periode Waktu:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 2. Filter Interaktif Berdasarkan Tahun (selectbox / multiselect)
years = sorted(df_cleaned['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun:", options=['Semua'] + list(years))

# 3. Filter Interaktif Berdasarkan Rentang Kecepatan Angin (slider)
min_wspm = float(df_cleaned['WSPM'].min())
max_wspm = float(df_cleaned['WSPM'].max())
selected_wspm = st.sidebar.slider(
    "Rentang Kecepatan Angin (WSPM):",
    min_value=min_wspm,
    max_value=max_wspm,
    value=(min_wspm, max_wspm)
)

# Terapkan Filter ke DataFrame
filtered_df = df_cleaned[
    (df_cleaned['datetime'].dt.date >= start_date) & 
    (df_cleaned['datetime'].dt.date <= end_date) & 
    (df_cleaned['WSPM'] >= selected_wspm[0]) & 
    (df_cleaned['WSPM'] <= selected_wspm[1])
]

if selected_year != 'Semua':
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

# --- VISUALISASI 1: Tren Rata-rata Konsentrasi PM2.5 per Tahun ---
st.subheader("1. Tren Rata-rata Konsentrasi PM2.5 dari Tahun ke Tahun")
pm25_yearly = df_cleaned.groupby('year')['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pm25_yearly['year'], pm25_yearly['PM2.5'], marker='o', color='b', linestyle='-')
ax.set_title("Rata-rata PM2.5 per Tahun")
ax.set_xlabel("Tahun")
ax.set_ylabel("PM2.5 ($\mu g/m^3$)")
ax.grid(True)
st.pyplot(fig)


# --- VISUALISASI 2: Hubungan Kecepatan Angin (WSPM) dan PM10 (Dinamis dengan Filter) ---
st.subheader("2. Hubungan Kecepatan Angin (WSPM) dan Konsentrasi PM10")

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='WSPM', y='PM10', data=filtered_df, alpha=0.4, color='purple', ax=ax)
ax.set_title(f"Scatter Plot WSPM vs PM10 (Filter Tahun: {selected_year})")
ax.set_xlabel("Kecepatan Angin (WSPM)")
ax.set_ylabel("Konsentrasi PM10")
st.pyplot(fig)