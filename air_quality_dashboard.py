import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul dan deskripsi dashboard
st.title("Dashboard Analisis Kualitas Udara 🌍")
st.write("Selamat datang di dashboard analisis kualitas udara. Selamat mengeksplorasi!")

# Memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("air_quality_final.csv")
    return df

df = load_data()

# Sidebar untuk navigasi
st.sidebar.header("Menu Interaktif 🛠️")

# Sidebar untuk Pertanyaan Bisnis 1
st.sidebar.subheader("Business Problem 1")
feature1 = st.sidebar.selectbox('Pilih Indikator Kualitas Udara untuk semua Station:', sorted(df.columns[5:]), index=df.columns.get_loc('PM2.5') - 5)

# Sidebar untuk Pertanyaan Bisnis 2
st.sidebar.subheader("Business Problem 2")
feature_x = st.sidebar.selectbox('Pilih Fitur untuk Sumbu X:', sorted(df.columns[5:]), index=df.columns.get_loc('TEMP') - 5)
feature_y = st.sidebar.selectbox('Pilih Fitur untuk Sumbu Y:', sorted(df.columns[5:]), index=df.columns.get_loc('O3') - 5)

# Slider untuk rentang tahun
year_range = st.sidebar.slider("Pilih Rentang Tahun:", min(df['year']), max(df['year']), (2016, 2017))

# Filtrasi Data Berdasarkan Tahun
df_filtered = df[df['year'].between(year_range[0], year_range[1])]

# Pertanyaan Bisnis 1
st.header(f"Business Problem 1: Rata-Rata Konsentrasi {feature1} berdasarkan Lokasi/Stasiun")

# Menampilkan statistik deskriptif
st.subheader("Statistik Deskriptif")
feature1_summary = df_filtered.groupby('station')[feature1].describe()
st.dataframe(feature1_summary)

# Visualisasi Data
st.subheader("Visualisasi Data")
fig1, ax1 = plt.subplots(figsize=(16, 8))
sns.barplot(x='station', y=feature1, data=df_filtered, estimator=np.mean, errorbar=None, palette="coolwarm", ax=ax1)  # Menggunakan errorbar=None menggantikan ci=None

# Menambahkan label angka pada setiap bar
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

ax1.set_title(f'Rata-Rata Konsentrasi {feature1} per Stasiun untuk Tahun {year_range[0]}-{year_range[1]}')
ax1.set_xlabel('Stasiun')
ax1.set_ylabel(f'Rata-Rata Konsentrasi {feature1}')
plt.xticks(rotation=45)
st.pyplot(fig1)

# Pertanyaan Bisnis 2
st.header(f"Business Problem 2: Korelasi antara {feature_x} dan {feature_y}")

# Menampilkan statistik deskriptif untuk Pertanyaan Bisnis 2
st.subheader("Statistik Deskriptif")
correlation = df_filtered[feature_x].corr(df_filtered[feature_y])
st.write(f"Korelasi antara {feature_x} dan {feature_y}: {correlation:.2f}")

# Visualisasi Data
st.subheader("Visualisasi Data")
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.scatterplot(x=feature_x, y=feature_y, data=df_filtered, hue='station', ax=ax2, alpha=0.5, s=20)  # Mengurangi ukuran titik untuk meningkatkan kecepatan
sns.regplot(x=feature_x, y=feature_y, data=df_filtered, scatter=False, color='red', ax=ax2)

# Menambahkan grid dan korelasi
ax2.grid(True, linestyle='--')
ax2.text(min(df_filtered[feature_x]) + 1, max(df_filtered[feature_y]) - 10, f'Korelasi: {correlation:.2f}', fontsize=12, color='red', bbox=dict(facecolor='white', alpha=0.5))

ax2.set_title(f'Scatter Plot antara {feature_x} vs {feature_y}')
ax2.set_xlabel(f'{feature_x}')
ax2.set_ylabel(f'{feature_y}')
st.pyplot(fig2)
