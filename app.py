import streamlit as st
import joblib
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Osteoporosis",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    /* Background gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Container utama */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Card style */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #666;
        font-size: 1.2rem;
    }
    
    /* Input section styling */
    .stSelectbox, .stNumberInput {
        background: white;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Result box styling */
    .result-box {
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .result-positive {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .result-negative {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    /* Factor list styling */
    .factor-item {
        background: rgba(255,255,255,0.2);
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid white;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load model dan scaler
try:
    model = joblib.load("model_dt.pkl")
    scaler = joblib.load("scaler.pkl")
except:
    st.error("⚠️ Model atau scaler tidak ditemukan. Pastikan file model_dt.pkl dan scaler.pkl ada di direktori yang sama.")
    st.stop()

# Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🦴 Prediksi Osteoporosis</div>
    <div class="subtitle">Sistem Prediksi Berbasis Decision Tree</div>
</div>
""", unsafe_allow_html=True)

# Info Box
st.markdown("""
<div class="info-box">
    <h3 style="margin-top:0; color:#333;">ℹ️ Tentang Osteoporosis</h3>
    <p style="margin-bottom:0; color:#555;">
    Osteoporosis adalah kondisi pengeroposan tulang yang membuat tulang menjadi rapuh dan mudah patah. 
    Deteksi dini sangat penting untuk pencegahan dan penanganan yang tepat.
    </p>
</div>
""", unsafe_allow_html=True)

# Layout dengan 2 kolom
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Data Demografis</div>', unsafe_allow_html=True)
    
    age = st.number_input("🎂 Usia", min_value=18, max_value=100, value=30, help="Masukkan usia Anda")
    gender = st.selectbox("👤 Jenis Kelamin", ["Perempuan", "Laki-laki"])
    race = st.selectbox("🌍 Ras/Etnis", ["Afrika-Amerika", "Asia", "Kaukasia"])
    weight = st.selectbox("⚖️ Berat Badan", ["Normal", "Kurus"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💊 Kondisi Medis</div>', unsafe_allow_html=True)
    
    hormonal = st.selectbox("🔬 Perubahan Hormon", ["Normal", "Pasca menopause"])
    family = st.selectbox("👨‍👩‍👧 Riwayat Keluarga", ["Tidak", "Ya"])
    medical = st.selectbox("🏥 Kondisi Medis", ["Tidak ada", "Gangguan tiroid", "Radang sendi"])
    meds = st.selectbox("💉 Obat-obatan", ["Tidak ada", "Kortikosteroid"])
    fracture = st.selectbox("🩹 Riwayat Patah Tulang", ["Tidak", "Ya"])
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🥗 Nutrisi</div>', unsafe_allow_html=True)
    
    calcium = st.selectbox("🥛 Asupan Kalsium", ["Cukup", "Rendah"])
    vitd = st.selectbox("☀️ Asupan Vitamin D", ["Cukup", "Tidak cukup"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🏃 Gaya Hidup</div>', unsafe_allow_html=True)
    
    activity = st.selectbox("⚽ Aktivitas Fisik", ["Aktif", "Kurang aktif"])
    smoke = st.selectbox("🚬 Merokok", ["Tidak", "Ya"])
    alkohol = st.selectbox("🍷 Konsumsi Alkohol", ["Tidak", "Sedang"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# Mapping
map_gender = {"Perempuan":0, "Laki-laki":1}
map_hormonal = {"Normal":0, "Pasca menopause":1}
map_family = {"Tidak":0, "Ya":1}
map_race = {"Afrika-Amerika":0, "Asia":1, "Kaukasia":2}
map_weight = {"Normal":0, "Kurus":1}
map_calcium = {"Cukup":0, "Rendah":1}
map_vitd = {"Tidak cukup":0, "Cukup":1}
map_activity = {"Aktif":0, "Kurang aktif":1}
map_smoke = {"Tidak":0, "Ya":1}
map_alkohol = {"Tidak":0, "Sedang":1}
map_medical = {"Gangguan tiroid":0, "Tidak ada":1, "Radang sendi":2}
map_meds = {"Kortikosteroid":0, "Tidak ada":1}
map_fracture = {"Tidak":0, "Ya":1}

# Prepare data
data = np.array([[
    age,
    map_gender[gender],
    map_hormonal[hormonal],
    map_family[family],
    map_race[race],
    map_weight[weight],
    map_calcium[calcium],
    map_vitd[vitd],
    map_activity[activity],
    map_smoke[smoke],
    map_alkohol[alkohol],
    map_medical[medical],
    map_meds[meds],
    map_fracture[fracture]
]])

data_scaled = scaler.transform(data)

# Tombol prediksi dengan spacing
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("🔍 ANALISIS SEKARANG")

# Prediksi
if predict_button:
    with st.spinner('🔄 Menganalisis data...'):
        hasil = model.predict(data_scaled)[0]
        
        if hasil == 1:
            st.markdown("""
            <div class="result-box result-positive">
                <h2 style="margin-top:0;">⚠️ HASIL PREDIKSI: BERISIKO OSTEOPOROSIS</h2>
                <p style="font-size:1.1rem;">Berdasarkan data yang Anda masukkan, sistem mendeteksi risiko osteoporosis.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Faktor Risiko yang Teridentifikasi:")
            
            factors = []
            if age > 50: factors.append("Usia di atas 50 tahun")
            if family == "Ya": factors.append("Ada riwayat keluarga osteoporosis")
            if hormonal == "Pasca menopause": factors.append("Kondisi pasca menopause")
            if weight == "Kurus": factors.append("Berat badan di bawah normal")
            if calcium == "Rendah": factors.append("Asupan kalsium rendah")
            if vitd == "Tidak cukup": factors.append("Asupan vitamin D tidak mencukupi")
            if activity == "Kurang aktif": factors.append("Aktivitas fisik kurang")
            if smoke == "Ya": factors.append("Kebiasaan merokok")
            if alkohol == "Sedang": factors.append("Konsumsi alkohol")
            if fracture == "Ya": factors.append("Riwayat patah tulang")
            
            if factors:
                for factor in factors:
                    st.markdown(f'<div class="factor-item">• {factor}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <h4 style="margin-top:0; color:#d63031;">💡 Rekomendasi:</h4>
                <ul style="color:#555; margin-bottom:0;">
                    <li>Konsultasikan dengan dokter untuk pemeriksaan lebih lanjut</li>
                    <li>Pertimbangkan untuk melakukan tes kepadatan tulang (DEXA scan)</li>
                    <li>Tingkatkan asupan kalsium dan vitamin D</li>
                    <li>Rutin berolahraga untuk memperkuat tulang</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="result-box result-negative">
                <h2 style="margin-top:0;">✅ HASIL PREDIKSI: RISIKO RENDAH</h2>
                <p style="font-size:1.1rem;">Berdasarkan data yang Anda masukkan, risiko osteoporosis tergolong rendah.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ✨ Faktor Protektif yang Teridentifikasi:")
            
            positive_factors = []
            if age <= 50: positive_factors.append("Usia masih relatif muda")
            if family == "Tidak": positive_factors.append("Tidak ada riwayat keluarga osteoporosis")
            if hormonal == "Normal": positive_factors.append("Kondisi hormonal normal")
            if weight == "Normal": positive_factors.append("Berat badan normal")
            if calcium == "Cukup": positive_factors.append("Asupan kalsium mencukupi")
            if vitd == "Cukup": positive_factors.append("Asupan vitamin D mencukupi")
            if activity == "Aktif": positive_factors.append("Aktivitas fisik teratur")
            if smoke == "Tidak": positive_factors.append("Tidak merokok")
            if alkohol == "Tidak": positive_factors.append("Tidak mengonsumsi alkohol")
            if fracture == "Tidak": positive_factors.append("Tidak ada riwayat patah tulang")
            
            if positive_factors:
                for factor in positive_factors:
                    st.markdown(f'<div class="factor-item">• {factor}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <h4 style="margin-top:0; color:#00b894;">💡 Saran untuk Menjaga Kesehatan Tulang:</h4>
                <ul style="color:#555; margin-bottom:0;">
                    <li>Pertahankan gaya hidup sehat yang sudah baik</li>
                    <li>Tetap konsumsi kalsium dan vitamin D yang cukup</li>
                    <li>Lanjutkan aktivitas fisik secara teratur</li>
                    <li>Lakukan pemeriksaan kesehatan rutin</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:white; padding:2rem;">
    <p style="margin:0; font-size:0.9rem;">⚕️ <strong>Disclaimer:</strong> Hasil prediksi ini bersifat informatif dan tidak menggantikan diagnosis medis profesional.</p>
    <p style="margin:0.5rem 0 0 0; font-size:0.8rem;">© 2025 Sistem Prediksi Osteoporosis | Powered by Decision Tree Algorithm</p>
</div>
""", unsafe_allow_html=True)
