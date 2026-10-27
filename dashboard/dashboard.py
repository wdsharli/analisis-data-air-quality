import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Analisis Kualitas Udara Aotizhongxin", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis Kualitas Udara Stasiun Aotizhongxin 🌍")

# Memuat data bersih
@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data.csv")

df = load_data()

# --- Pertanyaan 1: Tren Rata-rata PM2.5 dari Tahun ke Tahun ---
st.subheader("Tren Rata-rata Konsentrasi PM2.5 dari Tahun ke Tahun")
pm25_yearly = df.groupby('year')['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pm25_yearly['year'], pm25_yearly['PM2.5'], marker='o', color='b', linewidth=2)
ax.set_title("Rata-rata PM2.5 per Tahun", fontsize=14)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel(r"PM2.5 ($\mu g/m^3$)", fontsize=12)
ax.grid(True)
st.pyplot(fig)

# --- Pertanyaan 2: Hubungan Kecepatan Angin (WSPM) terhadap PM10 ---
st.subheader("Hubungan Kecepatan Angin (WSPM) terhadap Rata-rata PM10")
wspm_pm10 = df.groupby('WSPM')['PM10'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.scatterplot(data=wspm_pm10, x='WSPM', y='PM10', color='r', alpha=0.7, ax=ax2)
ax2.set_title("Scatter Plot WSPM vs PM10", fontsize=14)
ax2.set_xlabel("Kecepatan Angin (WSPM - m/s)", fontsize=12)
ax2.set_ylabel(r"Rata-rata PM10 ($\mu g/m^3$)", fontsize=12)
ax2.grid(True)
st.pyplot(fig2)

st.caption("Proyek Analisis Data - Dicoding")