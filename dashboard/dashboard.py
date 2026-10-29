import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis Kualitas Udara", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara Stasiun Aotizhongxin 🌍")

# Memuat dataset (pastikan jalur file CSV sudah sesuai)
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv") # Sesuaikan path jika diletakkan di tempat lain
    return df

df_cleaned = load_data()

# --- SIDEBAR: FITUR INTERAKTIF ---
st.sidebar.header("Filter Interaktif 🔍")

# 1. Filter Interaktif Berdasarkan Tahun (selectbox / multiselect)
years = sorted(df_cleaned['year'].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun:", options=['Semua'] + list(years))

# 2. Filter Interaktif Berdasarkan Rentang Kecepatan Angin (slider)
min_wspm = float(df_cleaned['WSPM'].min())
max_wspm = float(df_cleaned['WSPM'].max())
selected_wspm = st.sidebar.slider(
    "Rentang Kecepatan Angin (WSPM):",
    min_value=min_wspm,
    max_value=max_wspm,
    value=(min_wspm, max_wspm)
)

# Terapkan Filter ke DataFrame
filtered_df = df_cleaned[(df_cleaned['WSPM'] >= selected_wspm[0]) & (df_cleaned['WSPM'] <= selected_wspm[1])]
if selected_year != 'Semua':
    filtered_df = filtered_df[filtered_df['year'] == selected_year]


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