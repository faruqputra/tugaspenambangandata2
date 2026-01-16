import streamlit as st
import joblib
import numpy as np

# ================= TAMPILAN =================
st.set_page_config(
    page_title="Prediksi Osteoporosis",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CSS MODERN & RESPONSIF =================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Background Modern */
div[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #0f172a, #1e293b, #334155);
    font-family: 'Poppins', sans-serif;
}

/* Container utama */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    padding: 3rem 2rem;
    border-radius: 24px;
    margin-bottom: 2.5rem;
    text-align: center;
    box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
}

.main-header h1 {
    color: white !important;
    font-size: 3.5rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.main-header p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.2rem !important;
    margin-top: 0.5rem !important;
    font-weight: 400 !important;
}

/* Card Modern */
.modern-card {
    background: rgba(255, 255, 255, 0.98);
    padding: 2.5rem;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    height: 100%;
}

/* Section Title */
.section-title {
    color: #1e293b !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin-bottom: 2rem !important;
    padding-bottom: 1rem !important;
    border-bottom: 3px solid #3b82f6 !important;
}

/* Input Styling */
.stSelectbox label, .stNumberInput label {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
}

.stSelectbox > div > div, .stNumberInput > div > div {
    border-radius: 14px !important;
    border: 2px solid #e2e8f0 !important;
    background: #f8fafc !important;
    transition: all 0.3s ease !important;
    font-size: 1rem !important;
}

.stSelectbox > div > div:hover, .stNumberInput > div > div:hover {
    border-color: #3b82f6 !important;
    background: white !important;
}

.stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
    border-color: #3b82f6 !important;
    background: white !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
}

/* Button Premium */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 1.2rem 3rem !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    margin-top: 2rem !important;
    letter-spacing: 0.5px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 35px rgba(59, 130, 246, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(1.01) !important;
}

/* Result Box */
.result-box {
    padding: 2rem;
    border-radius: 20px;
    margin: 1.5rem 0;
    border-left: 6px solid;
    font-size: 1.1rem;
    font-weight: 600;
}

.result-positive {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-left-color: #ef4444;
    color: #991b1b;
}

.result-negative {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-left-color: #10b981;
    color: #065f46;
}

.result-waiting {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border-left-color: #3b82f6;
    color: #1e40af;
}

/* Factor List */
.factor-title {
    color: #1e293b;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 2rem 0 1.5rem 0;
    padding-top: 1.5rem;
    border-top: 2px solid #e2e8f0;
}

.factor-item {
    background: #f8fafc;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
    border-radius: 12px;
    border-left: 4px solid #3b82f6;
    color: #334155;
    font-size: 1.05rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.factor-item:hover {
    background: #f1f5f9;
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.risk-factor {
    border-left-color: #ef4444;
}

.protective-factor {
    border-left-color: #10b981;
}

/* Summary Box */
.summary-box {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 16px;
    margin-top: 2rem;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

.recommendation-box {
    background: #fef3c7;
    color: #92400e;
    padding: 1.5rem;
    border-radius: 16px;
    margin-top: 1.5rem;
    font-size: 1.05rem;
    font-weight: 600;
    border-left: 5px solid #f59e0b;
}

/* Responsif */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2.2rem !important;
    }
    
    .main-header p {
        font-size: 1rem !important;
    }
    
    .modern-card {
        padding: 1.5rem !important;
    }
    
    .section-title {
        font-size: 1.4rem !important;
    }
}

/* Animasi */
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

.modern-card {
    animation: slideIn 0.6s ease-out;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= MODEL =================
model = joblib.load("model_dt.pkl")
scaler = joblib.load("scaler.pkl")

# ================= HEADER =================
st.markdown("""
<div class='main-header'>
    <h1>Prediksi Osteoporosis</h1>
    <p>Sistem Deteksi Dini Berbasis Decision Tree</p>
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT DUA KOLOM =================
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Data Pasien</h2>", unsafe_allow_html=True)

    age = st.number_input("Usia (tahun)", 18, 100, 30)
    gender = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    hormonal = st.selectbox("Perubahan Hormon", ["Normal", "Pasca menopause"])
    family = st.selectbox("Riwayat Keluarga", ["Tidak", "Ya"])
    race = st.selectbox("Ras/Etnis", ["Afrika-Amerika", "Asia", "Kaukasia"])
    weight = st.selectbox("Status Berat Badan", ["Normal", "Kurus"])
    calcium = st.selectbox("Asupan Kalsium", ["Cukup", "Rendah"])
    vitd = st.selectbox("Asupan Vitamin D", ["Cukup", "Tidak cukup"])
    activity = st.selectbox("Aktivitas Fisik", ["Aktif", "Kurang aktif"])
    smoke = st.selectbox("Merokok", ["Tidak", "Ya"])
    alkohol = st.selectbox("Konsumsi Alkohol", ["Tidak", "Sedang"])
    medical = st.selectbox("Kondisi Medis", ["Gangguan tiroid", "Tidak ada", "Radang sendi"])
    meds = st.selectbox("Obat-obatan", ["Kortikosteroid", "Tidak ada"])
    fracture = st.selectbox("Riwayat Patah Tulang", ["Tidak", "Ya"])

    st.markdown("</div>", unsafe_allow_html=True)

# ================= MAPPING =================
map_gender = {"Perempuan": 0, "Laki-laki": 1}
map_hormonal = {"Normal": 0, "Pasca menopause": 1}
map_family = {"Tidak": 0, "Ya": 1}
map_race = {"Afrika-Amerika": 0, "Asia": 1, "Kaukasia": 2}
map_weight = {"Normal": 0, "Kurus": 1}
map_calcium = {"Cukup": 0, "Rendah": 1}
map_vitd = {"Tidak cukup": 0, "Cukup": 1}
map_activity = {"Aktif": 0, "Kurang aktif": 1}
map_smoke = {"Tidak": 0, "Ya": 1}
map_alkohol = {"Tidak": 0, "Sedang": 1}
map_medical = {"Gangguan tiroid": 0, "Tidak ada": 1, "Radang sendi": 2}
map_meds = {"Kortikosteroid": 0, "Tidak ada": 1}
map_fracture = {"Tidak": 0, "Ya": 1}

data = np.array([[age,
    map_gender[gender], map_hormonal[hormonal], map_family[family],
    map_race[race], map_weight[weight], map_calcium[calcium], map_vitd[vitd],
    map_activity[activity], map_smoke[smoke], map_alkohol[alkohol],
    map_medical[medical], map_meds[meds], map_fracture[fracture]
]])
data_scaled = scaler.transform(data)

# ================= HASIL PREDIKSI =================
with col2:
    st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Hasil Analisis</h2>", unsafe_allow_html=True)
    
    if st.button("PREDIKSI SEKARANG"):
        with st.spinner('Menganalisis data...'):
            hasil = model.predict(data_scaled)[0]

            if hasil == 1:
                st.markdown("<div class='result-box result-positive'>TERDETEKSI OSTEOPOROSIS</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='factor-title'>Faktor Risiko Teridentifikasi</div>", unsafe_allow_html=True)
                
                faktor_count = 0
                if age > 50: 
                    st.markdown("<div class='factor-item risk-factor'>Usia di atas 50 tahun</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if family == "Ya": 
                    st.markdown("<div class='factor-item risk-factor'>Ada riwayat keluarga osteoporosis</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if hormonal == "Pasca menopause": 
                    st.markdown("<div class='factor-item risk-factor'>Status pasca menopause</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if weight == "Kurus": 
                    st.markdown("<div class='factor-item risk-factor'>Berat badan kurang</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if calcium == "Rendah": 
                    st.markdown("<div class='factor-item risk-factor'>Asupan kalsium rendah</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if vitd == "Tidak cukup": 
                    st.markdown("<div class='factor-item risk-factor'>Kekurangan vitamin D</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if activity == "Kurang aktif": 
                    st.markdown("<div class='factor-item risk-factor'>Aktivitas fisik kurang</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if smoke == "Ya": 
                    st.markdown("<div class='factor-item risk-factor'>Kebiasaan merokok</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if alkohol == "Sedang": 
                    st.markdown("<div class='factor-item risk-factor'>Konsumsi alkohol</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if fracture == "Ya": 
                    st.markdown("<div class='factor-item risk-factor'>Riwayat patah tulang</div>", unsafe_allow_html=True)
                    faktor_count += 1
                
                st.markdown(f"<div class='summary-box'>Total {faktor_count} Faktor Risiko Ditemukan</div>", unsafe_allow_html=True)
                st.markdown("<div class='recommendation-box'>Segera konsultasi dengan dokter untuk pemeriksaan lebih lanjut</div>", unsafe_allow_html=True)
                
            else:
                st.markdown("<div class='result-box result-negative'>TIDAK TERDETEKSI OSTEOPOROSIS</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='factor-title'>Faktor Protektif</div>", unsafe_allow_html=True)
                
                faktor_count = 0
                if age <= 50: 
                    st.markdown("<div class='factor-item protective-factor'>Usia masih optimal</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if family == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak ada riwayat keluarga</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if hormonal == "Normal": 
                    st.markdown("<div class='factor-item protective-factor'>Hormon normal</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if weight == "Normal": 
                    st.markdown("<div class='factor-item protective-factor'>Berat badan ideal</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if calcium == "Cukup": 
                    st.markdown("<div class='factor-item protective-factor'>Asupan kalsium cukup</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if vitd == "Cukup": 
                    st.markdown("<div class='factor-item protective-factor'>Vitamin D tercukupi</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if activity == "Aktif": 
                    st.markdown("<div class='factor-item protective-factor'>Aktivitas fisik baik</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if smoke == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak merokok</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if alkohol == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak konsumsi alkohol</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if fracture == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak ada riwayat fraktur</div>", unsafe_allow_html=True)
                    faktor_count += 1
                
                st.markdown(f"<div class='summary-box'>Total {faktor_count} Faktor Protektif Ditemukan</div>", unsafe_allow_html=True)
                st.markdown("<div class='recommendation-box'>Pertahankan pola hidup sehat dan lakukan pemeriksaan rutin</div>", unsafe_allow_html=True)

    else:
        st.markdown("<div class='result-box result-waiting'>Klik tombol di bawah untuk memulai prediksi</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 1.2rem 3rem !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    margin-top: 2rem !important;
    letter-spacing: 0.5px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 35px rgba(59, 130, 246, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(1.01) !important;
}

/* Result Box */
.result-box {
    padding: 2rem;
    border-radius: 20px;
    margin: 1.5rem 0;
    border-left: 6px solid;
    font-size: 1.1rem;
    font-weight: 600;
}

.result-positive {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-left-color: #ef4444;
    color: #991b1b;
}

.result-negative {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-left-color: #10b981;
    color: #065f46;
}

.result-waiting {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border-left-color: #3b82f6;
    color: #1e40af;
}

/* Factor List */
.factor-title {
    color: #1e293b;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 2rem 0 1.5rem 0;
    padding-top: 1.5rem;
    border-top: 2px solid #e2e8f0;
}

.factor-item {
    background: #f8fafc;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
    border-radius: 12px;
    border-left: 4px solid #3b82f6;
    color: #334155;
    font-size: 1.05rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.factor-item:hover {
    background: #f1f5f9;
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.risk-factor {
    border-left-color: #ef4444;
}

.protective-factor {
    border-left-color: #10b981;
}

/* Summary Box */
.summary-box {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 16px;
    margin-top: 2rem;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

.recommendation-box {
    background: #fef3c7;
    color: #92400e;
    padding: 1.5rem;
    border-radius: 16px;
    margin-top: 1.5rem;
    font-size: 1.05rem;
    font-weight: 600;
    border-left: 5px solid #f59e0b;
}

/* Responsif */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2.2rem !important;
    }
    
    .main-header p {
        font-size: 1rem !important;
    }
    
    .modern-card {
        padding: 1.5rem !important;
    }
    
    .section-title {
        font-size: 1.4rem !important;
    }
}

/* Animasi */
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

.modern-card {
    animation: slideIn 0.6s ease-out;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= MODEL =================
model = joblib.load("model_dt.pkl")
scaler = joblib.load("scaler.pkl")

# ================= HEADER =================
st.markdown("""
<div class='main-header'>
    <h1>Prediksi Osteoporosis</h1>
    <p>Sistem Deteksi Dini Berbasis Decision Tree</p>
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT DUA KOLOM =================
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Data Pasien</h2>", unsafe_allow_html=True)

    age = st.number_input("Usia (tahun)", 18, 100, 30)
    gender = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    hormonal = st.selectbox("Perubahan Hormon", ["Normal", "Pasca menopause"])
    family = st.selectbox("Riwayat Keluarga", ["Tidak", "Ya"])
    race = st.selectbox("Ras/Etnis", ["Afrika-Amerika", "Asia", "Kaukasia"])
    weight = st.selectbox("Status Berat Badan", ["Normal", "Kurus"])
    calcium = st.selectbox("Asupan Kalsium", ["Cukup", "Rendah"])
    vitd = st.selectbox("Asupan Vitamin D", ["Cukup", "Tidak cukup"])
    activity = st.selectbox("Aktivitas Fisik", ["Aktif", "Kurang aktif"])
    smoke = st.selectbox("Merokok", ["Tidak", "Ya"])
    alkohol = st.selectbox("Konsumsi Alkohol", ["Tidak", "Sedang"])
    medical = st.selectbox("Kondisi Medis", ["Gangguan tiroid", "Tidak ada", "Radang sendi"])
    meds = st.selectbox("Obat-obatan", ["Kortikosteroid", "Tidak ada"])
    fracture = st.selectbox("Riwayat Patah Tulang", ["Tidak", "Ya"])

    st.markdown("</div>", unsafe_allow_html=True)

# ================= MAPPING =================
map_gender = {"Perempuan": 0, "Laki-laki": 1}
map_hormonal = {"Normal": 0, "Pasca menopause": 1}
map_family = {"Tidak": 0, "Ya": 1}
map_race = {"Afrika-Amerika": 0, "Asia": 1, "Kaukasia": 2}
map_weight = {"Normal": 0, "Kurus": 1}
map_calcium = {"Cukup": 0, "Rendah": 1}
map_vitd = {"Tidak cukup": 0, "Cukup": 1}
map_activity = {"Aktif": 0, "Kurang aktif": 1}
map_smoke = {"Tidak": 0, "Ya": 1}
map_alkohol = {"Tidak": 0, "Sedang": 1}
map_medical = {"Gangguan tiroid": 0, "Tidak ada": 1, "Radang sendi": 2}
map_meds = {"Kortikosteroid": 0, "Tidak ada": 1}
map_fracture = {"Tidak": 0, "Ya": 1}

data = np.array([[age,
    map_gender[gender], map_hormonal[hormonal], map_family[family],
    map_race[race], map_weight[weight], map_calcium[calcium], map_vitd[vitd],
    map_activity[activity], map_smoke[smoke], map_alkohol[alkohol],
    map_medical[medical], map_meds[meds], map_fracture[fracture]
]])
data_scaled = scaler.transform(data)

# ================= HASIL PREDIKSI =================
with col2:
    st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Hasil Analisis</h2>", unsafe_allow_html=True)
    
    if st.button("PREDIKSI SEKARANG"):
        with st.spinner('Menganalisis data...'):
            hasil = model.predict(data_scaled)[0]

            if hasil == 1:
                st.markdown("<div class='result-box result-positive'>TERDETEKSI OSTEOPOROSIS</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='factor-title'>Faktor Risiko Teridentifikasi</div>", unsafe_allow_html=True)
                
                faktor_count = 0
                if age > 50: 
                    st.markdown("<div class='factor-item risk-factor'>Usia di atas 50 tahun</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if family == "Ya": 
                    st.markdown("<div class='factor-item risk-factor'>Ada riwayat keluarga osteoporosis</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if hormonal == "Pasca menopause": 
                    st.markdown("<div class='factor-item risk-factor'>Status pasca menopause</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if weight == "Kurus": 
                    st.markdown("<div class='factor-item risk-factor'>Berat badan kurang</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if calcium == "Rendah": 
                    st.markdown("<div class='factor-item risk-factor'>Asupan kalsium rendah</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if vitd == "Tidak cukup": 
                    st.markdown("<div class='factor-item risk-factor'>Kekurangan vitamin D</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if activity == "Kurang aktif": 
                    st.markdown("<div class='factor-item risk-factor'>Aktivitas fisik kurang</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if smoke == "Ya": 
                    st.markdown("<div class='factor-item risk-factor'>Kebiasaan merokok</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if alkohol == "Sedang": 
                    st.markdown("<div class='factor-item risk-factor'>Konsumsi alkohol</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if fracture == "Ya": 
                    st.markdown("<div class='factor-item risk-factor'>Riwayat patah tulang</div>", unsafe_allow_html=True)
                    faktor_count += 1
                
                st.markdown(f"<div class='summary-box'>Total {faktor_count} Faktor Risiko Ditemukan</div>", unsafe_allow_html=True)
                st.markdown("<div class='recommendation-box'>Segera konsultasi dengan dokter untuk pemeriksaan lebih lanjut</div>", unsafe_allow_html=True)
                
            else:
                st.markdown("<div class='result-box result-negative'>TIDAK TERDETEKSI OSTEOPOROSIS</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='factor-title'>Faktor Protektif</div>", unsafe_allow_html=True)
                
                faktor_count = 0
                if age <= 50: 
                    st.markdown("<div class='factor-item protective-factor'>Usia masih optimal</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if family == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak ada riwayat keluarga</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if hormonal == "Normal": 
                    st.markdown("<div class='factor-item protective-factor'>Hormon normal</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if weight == "Normal": 
                    st.markdown("<div class='factor-item protective-factor'>Berat badan ideal</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if calcium == "Cukup": 
                    st.markdown("<div class='factor-item protective-factor'>Asupan kalsium cukup</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if vitd == "Cukup": 
                    st.markdown("<div class='factor-item protective-factor'>Vitamin D tercukupi</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if activity == "Aktif": 
                    st.markdown("<div class='factor-item protective-factor'>Aktivitas fisik baik</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if smoke == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak merokok</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if alkohol == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak konsumsi alkohol</div>", unsafe_allow_html=True)
                    faktor_count += 1
                if fracture == "Tidak": 
                    st.markdown("<div class='factor-item protective-factor'>Tidak ada riwayat fraktur</div>", unsafe_allow_html=True)
                    faktor_count += 1
                
                st.markdown(f"<div class='summary-box'>Total {faktor_count} Faktor Protektif Ditemukan</div>", unsafe_allow_html=True)
                st.markdown("<div class='recommendation-box'>Pertahankan pola hidup sehat dan lakukan pemeriksaan rutin</div>", unsafe_allow_html=True)

    else:
        st.markdown("<div class='result-box result-waiting'>Klik tombol di bawah untuk memulai prediksi</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
