import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Kebutuhan Belajar Fisika",
    page_icon="📊",
    layout="wide"
)

# Judul Dashboard
st.title("📊 DASHBOARD ANALISIS KEBUTUHAN BELAJAR PESERTA DIDIK")
st.subheader("Pembelajaran Fisika - SMA Negeri 4 Palembang")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("ANGKET ANALISIS KEBUTUHAN PESERTA DIDIK.csv", skiprows=1)
    return df

try:
    df = load_data()
    
    # Sidebar untuk filter
    st.sidebar.header("🔍 Filter Data")
    
    # Filter Kelas
    kelas_list = df['Kelas'].unique().tolist()
    selected_kelas = st.sidebar.multiselect("Pilih Kelas:", kelas_list, default=kelas_list)
    
    # Filter data berdasarkan kelas
    if selected_kelas:
        df_filtered = df[df['Kelas'].isin(selected_kelas)]
    else:
        df_filtered = df
    
    # Informasi responden
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Informasi Responden")
    st.sidebar.write(f"**Total Responden:** {len(df_filtered)} siswa")
    st.sidebar.write(f"**Tanggal Survey:** 10 Maret 2026")
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ===== BAGIAN 1: PROFIL RESPONDEN =====
st.header("1️⃣ PROFIL RESPONDEN")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Responden", f"{len(df_filtered)} Siswa")
    
with col2:
    jumlah_kelas = df_filtered['Kelas'].nunique()
    st.metric("Jumlah Kelas", f"{jumlah_kelas} Kelas")
    
with col3:
    st.metric("Jumlah Pertanyaan", "19 Butir")

st.markdown("---")

# ===== BAGIAN 2: DISTRIBUSI JAWABAN PER INDIKATOR =====
st.header("2️⃣ DISTRIBUSI JAWABAN PER INDIKATOR")

# Definisi kolom untuk setiap indikator
indikator_map = {
    "Minat dan Sikap": [
        "Saya tertarik mempelajari Fisika.",
        "Fisika merupakan pelajaran yang penting untuk kehidupan sehari-hari.",
        "Saya merasa senang saat mengikuti pembelajaran Fisika.",
        "Fisika adalah pelajaran yang sulit.",
        "Saya percaya diri saat mengerjakan soal Fisika."
    ],
    "Kesulitan Belajar": [
        "Saya kesulitan memahami konsep-konsep dalam Fisika.",
        "Saya kesulitan dalam perhitungan atau penggunaan rumus.",
        "Saya kesulitan memahami soal cerita dalam Fisika.",
        "Saya kesulitan menghubungkan Fisika dengan kehidupan sehari-hari."
    ],
    "Preferensi Pembelajaran": [
        "Penjelasan yang diberikan oleh guru sudah mudah untuk saya pahami.",
        "Saya lebih mudah memahami Fisika jika menggunakan video atau animasi.",
        "Saya lebih mudah memahami Fisika melalui praktikum atau percobaan.",
        "Saya lebih suka pembelajaran dengan diskusi kelompok."
    ],
    "Kebutuhan Belajar": [
        "Saya membutuhkan lebih banyak latihan soal.",
        "Saya membutuhkan contoh soal yang dibahas secara bertahap.",
        "Saya membutuhkan media pembelajaran yang lebih menarik.",
        "Saya belajar kembali materi Fisika di rumah.",
        "Saya mencari sumber belajar lain selain dari guru (internet/buku lain).",
        "Saya bertanya kepada guru jika tidak memahami materi."
    ]
}

# Pilihan indikator
selected_indikator = st.selectbox(
    "Pilih Indikator:",
    list(indikator_map.keys())
)

# Tampilkan hasil untuk indikator yang dipilih
st.subheader(f"📈 {selected_indikator}")

# Hitung mean untuk setiap pertanyaan dalam indikator
pertanyaan_list = indikator_map[selected_indikator]
data_visual = []

for pertanyaan in pertanyaan_list:
    if pertanyaan in df_filtered.columns:
        mean_score = df_filtered[pertanyaan].mean()
        
        # Kategorisasi
        if mean_score >= 3.26:
            kategori = "Tinggi"
            warna = "green"
        elif mean_score >= 2.51:
            kategori = "Sedang"
            warna = "orange"
        elif mean_score >= 1.76:
            kategori = "Rendah"
            warna = "red"
        else:
            kategori = "Sangat Rendah"
            warna = "darkred"
        
        data_visual.append({
            "Pertanyaan": pertanyaan[:80] + "..." if len(pertanyaan) > 80 else pertanyaan,
            "Mean": round(mean_score, 2),
            "Kategori": kategori,
            "Warna": warna
        })

df_visual = pd.DataFrame(data_visual)

# Tampilkan tabel
st.dataframe(
    df_visual,
    use_container_width=True,
    hide_index=True
)

# ===== BAGIAN 3: VISUALISASI INTERAKTIF =====
st.header("3️⃣ VISUALISASI DATA")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribusi Jawaban", "📈 Mean Score", "🎯 Kategori", "💡 Insights"])

with tab1:
    st.subheader("Distribusi Frekuensi Jawaban")
    
    # Pilih pertanyaan untuk ditampilkan
    selected_pertanyaan = st.selectbox(
        "Pilih Pernyataan:",
        pertanyaan_list
    )
    
    if selected_pertanyaan in df_filtered.columns:
        # Hitung frekuensi
        freq = df_filtered[selected_pertanyaan].value_counts().sort_index()
        
        # Mapping nilai
        nilai_map = {1: "STS", 2: "TS", 3: "S", 4: "SS"}
        
        fig = px.bar(
            x=[nilai_map[i] for i in freq.index],
            y=freq.values,
            labels={"x": "Kategori Jawaban", "y": "Frekuensi"},
            title=f"Distribusi Jawaban: {selected_pertanyaan[:100]}",
            color=[nilai_map[i] for i in freq.index],
            color_discrete_map={"STS": "#e74c3c", "TS": "#e67e22", "S": "#3498db", "SS": "#2ecc71"}
        )
        
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Grafik Mean Score per Pernyataan")
    
    # Bar chart mean score
    fig = px.bar(
        df_visual,
        x="Pertanyaan",
        y="Mean",
        color="Kategori",
        color_discrete_map={"Tinggi": "#2ecc71", "Sedang": "#f39c12", "Rendah": "#e74c3c"},
        title="Mean Score untuk Setiap Pernyataan",
        labels={"Pertanyaan": "Pernyataan", "Mean": "Nilai Rata-rata"}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Persentase Kategori")
    
    # Hitung persentase kategori
    kategori_count = df_visual['Kategori'].value_counts()
    
    # Pie chart
    fig = px.pie(
        values=kategori_count.values,
        names=kategori_count.index,
        title="Distribusi Kategori Pernyataan",
        color=kategori_count.index,
        color_discrete_map={"Tinggi": "#2ecc71", "Sedang": "#f39c12", "Rendah": "#e74c3c"}
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("💡 Insights dan Temuan Penting")
    
    # Temuan berdasarkan data
    st.markdown("### 📌 Temuan Utama:")
    
    # Pernyataan dengan mean tertinggi
    tertinggi = df_visual.loc[df_visual['Mean'].idxmax()]
    st.success(f"**Pernyataan dengan skor tertinggi:** {tertinggi['Pertanyaan']} (Mean: {tertinggi['Mean']})")
    
    # Pernyataan dengan mean terendah
    terendah = df_visual.loc[df_visual['Mean'].idxmin()]
    st.warning(f"**Pernyataan dengan skor terendah:** {terendah['Pertanyaan']} (Mean: {terendah['Mean']})")
    
    # Jumlah kategori
    st.info(f"**Distribusi Kategori:** {df_visual['Kategori'].value_counts().to_dict()}")

# ===== BAGIAN 4: ANALISIS KOMPREHENSIF =====
st.header("4️⃣ ANALISIS KOMPREHENSIF")

# Hitung overall mean per indikator
st.subheader("Rata-rata per Indikator")

indikator_means = {}

for indikator, pertanyaan_list in indikator_map.items():
    scores = []
    for pertanyaan in pertanyaan_list:
        if pertanyaan in df_filtered.columns:
            scores.append(df_filtered[pertanyaan].mean())
    
    if scores:
        indikator_means[indikator] = round(np.mean(scores), 2)

# Tampilkan dalam bentuk metric columns
cols = st.columns(len(indikator_means))

for idx, (indikator, mean_score) in enumerate(indikator_means.items()):
    with cols[idx]:
        if mean_score >= 3.26:
            st.metric(indikator, f"{mean_score}", "Tinggi 📈")
        elif mean_score >= 2.51:
            st.metric(indikator, f"{mean_score}", "Sedang ➡️")
        else:
            st.metric(indikator, f"{mean_score}", "Rendah 📉")

# Grafik radar untuk semua indikator
st.subheader("Visualisasi Radar Chart")

radar_data = pd.DataFrame({
    'Indikator': list(indikator_means.keys()),
    'Mean': list(indikator_means.values())
})

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=radar_data['Mean'],
    theta=radar_data['Indikator'],
    fill='toself',
    name='Mean Score',
    line_color='#3498db'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[1, 4]
        )),
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ===== BAGIAN 5: REKOMENDASI =====
st.header("5️⃣ REKOMENDASI BERDASARKAN DATA")

st.markdown("""
### Berdasarkan hasil analisis angket, berikut rekomendasi pembelajaran:

**🎯 Metode Pembelajaran:**
- **Prioritas Utama:** Tingkatkan frekuensi praktikum (95.2% siswa lebih mudah paham melalui praktikum)
- **Media Visual:** Gunakan video/animasi untuk konsep abstrak (85.7% siswa terbantu)
- **Pendekatan Bertahap:** Berikan contoh soal dengan penyelesaian bertahap (90.5% siswa membutuhkan)

**📚 Kebutuhan Belajar:**
- Sediakan lebih banyak latihan soal dengan pembahasan detail
- Gunakan media pembelajaran interaktif (PhET, Kahoot, games)
- Berikan penjelasan dengan bahasa yang mudah dipahami

**🔧 Strategi Pembelajaran:**
- Kombinasikan praktikum dengan penjelasan konsep oleh guru
- Fokus pada pemahaman konsep sebelum penggunaan rumus
- Ciptakan pembelajaran yang menyenangkan dan interaktif
""")

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Dashboard Analisis Kebutuhan Belajar Fisika</strong></p>
    <p>SMA Negeri 4 Palembang | Maret 2026</p>
    <p>Dibuat untuk Mata Kuliah Perencanaan Pembelajaran Fisika</p>
</div>
""", unsafe_allow_html=True)