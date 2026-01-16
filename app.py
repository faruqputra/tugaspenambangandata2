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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background */
    .main {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Container utama */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 3rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        position: relative;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        font-weight: 300;
        position: relative;
    }
    
    /* Card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }
    
    /* Section headers */
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
    }
    
    /* Input styling */
    .stSelectbox label, .stNumberInput label {
        font-weight: 600;
        color: #4a5568;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div, .stNumberInput > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover, .stNumberInput > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        padding: 1.2rem 3rem;
        border: none;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Info banner */
    .info-banner {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-left: 5px solid #f5576c;
    }
    
    .info-banner h3 {
        color: #2d3748;
        margin-top: 0;
        font-weight: 700;
        font-size: 1.4rem;
    }
    
    .info-banner p {
        color: #4a5568;
        margin-bottom: 0;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    /* Result boxes */
    .result-container {
        margin-top: 3rem;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-header {
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .result-positive {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .result-negative {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    .result-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .result-description {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.95);
        font-weight: 300;
    }
    
    /* Factor items */
    .factor-list {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .factor-list h3 {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .factor-item {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        font-weight: 500;
        color: #2d3748;
        transition: all 0.3s ease;
    }
    
    .factor-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .recommendation-box h4 {
        color: #2d3748;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    .recommendation-box ul {
        color: #2d3748;
        line-height: 2;
        font-size: 1.05rem;
    }
    
    .recommendation-box li {
        margin-bottom: 0.5rem;
    }
    
    /* Stats card */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #718096;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.8);
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer-text {
        font-size: 0.95rem;
        line-height: 1.8;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load model dan scaler
try:
    model = joblib.load("model_dt.pkl")
    scaler = joblib.load("scaler.pkl")
except:
    st.error("Model atau scaler tidak ditemukan. Pastikan file model_dt.pkl dan scaler.pkl ada di direktori yang sama.")
    st.stop()

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Sistem Prediksi Osteoporosis</div>
    <div class="hero-subtitle">Analisis risiko berbasis Machine Learning dengan Decision Tree Algorithm</div>
</div>
""", unsafe_allow_html=True)

# Info Banner
st.markdown("""
<div class="info-banner">
    <h3>Tentang Osteoporosis</h3>
    <p>
    Osteoporosis adalah kondisi medis yang ditandai dengan penurunan kepadatan tulang, 
    menyebabkan tulang menjadi rapuh dan rentan patah. Deteksi dini sangat penting untuk 
    pencegahan dan penanganan yang efektif. Sistem ini menggunakan algoritma Decision Tree 
    untuk menganalisis berbagai faktor risiko dan memberikan prediksi awal.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Input Section
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Data Demografis & Antropometri</div>', unsafe_allow_html=True)
    
    age = st.number_input("Usia (tahun)", min_value=18, max_value=100, value=30, help="Masukkan usia dalam tahun")
    gender = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    race = st.selectbox("Apa ras atau etnis anda?", ["Afrika-Amerika", "Asia", "Kaukasia"])
    weight = st.selectbox("Bagaimana status berat badan anda?", ["Normal", "Kurus"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Riwayat Medis</div>', unsafe_allow_html=True)
    
    hormonal = st.selectbox("Apakah anda mengalami perubahan hormonal yang signifikan (misalnya menopause)?", ["Normal", "Pasca menopause"])
    family = st.selectbox("Apakah ada riwayat keluarga osteoporosis atau patah tulang?", ["Tidak", "Ya"])
    medical = st.selectbox("Apakah anda memiliki kondisi medis tertentu?", ["Tidak ada", "Gangguan tiroid", "Radang sendi"])
    meds = st.selectbox("Apakah anda mengkonsumsi obat-obatan tertentu?", ["Tidak ada", "Kortikosteroid"])
    fracture = st.selectbox("Apakah anda mengalami patah tulang sebelumnya?", ["Tidak", "Ya"])
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Asupan Nutrisi</div>', unsafe_allow_html=True)
    
    calcium = st.selectbox("Bagaimana tingkat asupan kalsium harian anda ( misalnya dari susu, keju, atau suplemen)?", ["Cukup", "Rendah"])
    vitd = st.selectbox("Bagaimana tingkat asupan Vitamin D anda ( dari makanan, suplemen, atau sinar matahari )?", ["Cukup", "Tidak cukup"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Gaya Hidup & Kebiasaan</div>', unsafe_allow_html=True)
    
    activity = st.selectbox("Seberapa aktif anda dalam melakukan aktifitas fisik atau olahraga? ", ["Aktif", "Kurang aktif"])
    smoke = st.selectbox("Apakah anda seorang perokok? ", ["Tidak", "Ya"])
    alkohol = st.selectbox("Bagaimana kebiasaan konsumsi alkohol anda?", ["Tidak", "Sedang"])
    
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

# Tombol prediksi
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("Analisis Risiko Sekarang")

# Prediksi
if predict_button:
    with st.spinner('Memproses data dan menganalisis risiko...'):
        hasil = model.predict(data_scaled)[0]
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        if hasil == 1:
            st.markdown("""
            <div class="result-header result-positive">
                <div class="result-title">RISIKO TINGGI OSTEOPOROSIS</div>
                <div class="result-description">Hasil analisis menunjukkan adanya indikasi risiko osteoporosis berdasarkan data yang diberikan</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="factor-list">', unsafe_allow_html=True)
            st.markdown("<h3>Faktor Risiko Teridentifikasi</h3>", unsafe_allow_html=True)
            
            factors = []
            if age > 50: factors.append("Usia lebih dari 50 tahun meningkatkan risiko pengeroposan tulang")
            if family == "Ya": factors.append("Riwayat keluarga dengan osteoporosis menunjukkan faktor genetik")
            if hormonal == "Pasca menopause": factors.append("Kondisi pasca menopause mempengaruhi kepadatan tulang")
            if weight == "Kurus": factors.append("Berat badan di bawah normal mengurangi densitas tulang")
            if calcium == "Rendah": factors.append("Asupan kalsium yang rendah mempengaruhi kesehatan tulang")
            if vitd == "Tidak cukup": factors.append("Kekurangan vitamin D menghambat penyerapan kalsium")
            if activity == "Kurang aktif": factors.append("Aktivitas fisik minimal mengurangi kekuatan tulang")
            if smoke == "Ya": factors.append("Kebiasaan merokok mempercepat kehilangan massa tulang")
            if alkohol == "Sedang": factors.append("Konsumsi alkohol dapat mengganggu pembentukan tulang")
            if fracture == "Ya": factors.append("Riwayat fraktur sebelumnya meningkatkan risiko patah tulang berulang")
            
            if factors:
                for factor in factors:
                    st.markdown(f'<div class="factor-item">{factor}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="factor-item">Sistem mendeteksi pola risiko dari kombinasi faktor yang ada</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
                <h4>Rekomendasi Tindak Lanjut</h4>
                <ul>
                    <li>Segera konsultasikan dengan dokter spesialis ortopedi atau rheumatologi</li>
                    <li>Pertimbangkan untuk melakukan tes densitas tulang (DEXA Scan)</li>
                    <li>Tingkatkan asupan kalsium hingga 1000-1200 mg per hari</li>
                    <li>Konsumsi suplemen vitamin D sesuai anjuran medis</li>
                    <li>Mulai program latihan weight-bearing secara teratur</li>
                    <li>Evaluasi dan modifikasi gaya hidup yang berisiko</li>
                    <li>Pertimbangkan terapi medis preventif jika diperlukan</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="result-header result-negative">
                <div class="result-title">RISIKO RENDAH OSTEOPOROSIS</div>
                <div class="result-description">Hasil analisis menunjukkan risiko osteoporosis dalam kategori rendah berdasarkan data yang diberikan</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="factor-list">', unsafe_allow_html=True)
            st.markdown("<h3>Faktor Protektif Teridentifikasi</h3>", unsafe_allow_html=True)
            
            positive_factors = []
            if age <= 50: positive_factors.append("Usia masih dalam kategori optimal untuk kesehatan tulang")
            if family == "Tidak": positive_factors.append("Tidak ada riwayat keluarga mengurangi predisposisi genetik")
            if hormonal == "Normal": positive_factors.append("Status hormonal normal mendukung homeostasis tulang")
            if weight == "Normal": positive_factors.append("Berat badan ideal mempertahankan densitas tulang optimal")
            if calcium == "Cukup": positive_factors.append("Asupan kalsium adekuat mendukung kesehatan tulang")
            if vitd == "Cukup": positive_factors.append("Level vitamin D memadai untuk penyerapan kalsium")
            if activity == "Aktif": positive_factors.append("Aktivitas fisik teratur memperkuat struktur tulang")
            if smoke == "Tidak": positive_factors.append("Bebas rokok melindungi dari kehilangan massa tulang")
            if alkohol == "Tidak": positive_factors.append("Tidak mengonsumsi alkohol menjaga metabolisme tulang")
            if fracture == "Tidak": positive_factors.append("Tidak ada riwayat fraktur menunjukkan tulang yang kuat")
            
            if positive_factors:
                for factor in positive_factors:
                    st.markdown(f'<div class="factor-item">{factor}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="factor-item">Profil risiko Anda menunjukkan kondisi yang baik</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
                <h4>Saran Pemeliharaan Kesehatan Tulang</h4>
                <ul>
                    <li>Pertahankan pola hidup sehat yang sudah dijalankan</li>
                    <li>Jaga asupan kalsium dan vitamin D tetap adekuat</li>
                    <li>Lanjutkan rutinitas aktivitas fisik minimal 150 menit per minggu</li>
                    <li>Konsumsi makanan kaya nutrisi untuk tulang (susu, ikan, sayuran hijau)</li>
                    <li>Hindari kebiasaan yang dapat merusak kesehatan tulang</li>
                    <li>Lakukan pemeriksaan kesehatan rutin setiap tahun</li>
                    <li>Monitor kesehatan tulang seiring bertambahnya usia</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div class="footer-text">
        <strong>Disclaimer Medis</strong><br>
        Hasil prediksi ini bersifat informatif dan tidak dapat menggantikan diagnosis medis profesional.
        Selalu konsultasikan dengan tenaga kesehatan yang berkualifikasi untuk evaluasi dan penanganan yang tepat.
    </div>
    <div class="divider"></div>
    <div class="footer-text">
        Sistem Prediksi Osteoporosis | Decision Tree Machine Learning Algorithm<br>
        Dikembangkan untuk tujuan edukasi dan skrining awal
    </div>
</div>
""", unsafe_allow_html=True)
