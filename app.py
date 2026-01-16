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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Background dengan gradient */
div[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', sans-serif;
}

div[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    pointer-events: none;
    z-index: 0;
}

/* Container utama */
.block-container {
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* Header Card */
.header-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 2.5rem;
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    margin-bottom: 2rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Card dengan glassmorphism */
.glass-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* Judul */
h1 {
    color: #1a1a2e;
    font-size: 3rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    color: #64748b;
    font-size: 1.1rem;
    font-weight: 400;
    margin-bottom: 0;
}

/* Sub-headers */
h2, h3 {
    color: #1e293b !important;
    font-weight: 600 !important;
}

.stSubheader {
    color: #1e293b !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 1.5rem !important;
}

/* Input fields styling */
.stSelectbox label, .stNumberInput label {
    color: #334155 !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}

.stSelectbox > div > div, .stNumberInput > div > div {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    background: white !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div:hover, .stNumberInput > div > div:hover {
    border-color: #667eea !important;
}

.stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Tombol prediksi */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    margin-top: 1rem !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Alert boxes */
.element-container div[data-testid="stMarkdownContainer"] > div[data-testid="stAlert"] {
    border-radius: 12px !important;
    padding: 1.25rem !important;
    margin: 1rem 0 !important;
    border-left: 4px solid !important;
    font-weight: 500 !important;
}

div[data-baseweb="notification"][kind="error"] {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
    border-left-color: #ef4444 !important;
}

div[data-baseweb="notification"][kind="success"] {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
    border-left-color: #10b981 !important;
}

/* List styling */
.stMarkdown ul {
    list-style: none !important;
    padding-left: 0 !important;
}

.stMarkdown li {
    padding: 0.5rem 0 !important;
    color: #475569 !important;
    font-size: 0.95rem !important;
    display: flex !important;
    align-items: center !important;
}

.stMarkdown li::before {
    content: "→" !important;
    margin-right: 0.75rem !important;
    color: #667eea !important;
    font-weight: bold !important;
    font-size: 1.2rem !important;
}

/* Section headers dalam hasil */
.stMarkdown strong {
    color: #1e293b !important;
    font-size: 1.1rem !important;
    display: block !important;
    margin: 1rem 0 0.5rem 0 !important;
}

/* Responsif untuk mobile */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }
    
    .header-card {
        padding: 1.5rem !important;
    }
    
    .glass-card {
        padding: 1.5rem !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
    }
}

/* Animasi loading */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.glass-card {
    animation: fadeIn 0.5s ease-out;
}

/* Icon emoji styling */
.header-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    display: block;
}

/* Spacing adjustments */
.element-container {
    margin-bottom: 0.5rem !important;
}

/* Divider */
hr {
    margin: 2rem 0 !important;
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
}
</style>
""", unsafe_allow_html=True)

# ================= MODEL =================
model = joblib.load("model_dt.pkl")
scaler = joblib.load("scaler.pkl")

# ================= HEADER =================
st.markdown("""
<div class='header-card'>
    <span class='header-icon'>🦴</span>
    <h1>Prediksi Osteoporosis</h1>
    <p class='subtitle'>Aplikasi Prediksi Berbasis Decision Tree untuk Deteksi Dini Osteoporosis</p>
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT DUA KOLOM =================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📝 Data Pasien")
    st.markdown("---")

    age = st.number_input("Usia (tahun)", 18, 100, 30, help="Masukkan usia pasien")
    gender = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    hormonal = st.selectbox("Perubahan Hormon", ["Normal", "Pasca menopause"])
    family = st.selectbox("Riwayat Keluarga Osteoporosis", ["Tidak", "Ya"])
    race = st.selectbox("Ras/Etnis", ["Afrika-Amerika", "Asia", "Kaukasia"])
    weight = st.selectbox("Status Berat Badan", ["Normal", "Kurus"])
    calcium = st.selectbox("Asupan Kalsium", ["Cukup", "Rendah"])
    vitd = st.selectbox("Asupan Vitamin D", ["Cukup", "Tidak cukup"])
    activity = st.selectbox("Aktivitas Fisik", ["Aktif", "Kurang aktif"])
    smoke = st.selectbox("Status Merokok", ["Tidak", "Ya"])
    alkohol = st.selectbox("Konsumsi Alkohol", ["Tidak", "Sedang"])
    medical = st.selectbox("Kondisi Medis", ["Gangguan tiroid", "Tidak ada", "Radang sendi"])
    meds = st.selectbox("Penggunaan Obat-obatan", ["Kortikosteroid", "Tidak ada"])
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
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Prediksi")
    st.markdown("---")
    
    if st.button("🔍 Mulai Prediksi"):
        with st.spinner('Menganalisis data...'):
            hasil = model.predict(data_scaled)[0]

            if hasil == 1:
                st.error("⚠️ **Terdeteksi Osteoporosis**")
                st.markdown("**Faktor Risiko yang Teridentifikasi:**")
                
                faktor_count = 0
                if age > 50: 
                    st.write("- Usia di atas 50 tahun")
                    faktor_count += 1
                if family == "Ya": 
                    st.write("- Riwayat keluarga dengan osteoporosis")
                    faktor_count += 1
                if hormonal == "Pasca menopause": 
                    st.write("- Status pasca menopause")
                    faktor_count += 1
                if weight == "Kurus": 
                    st.write("- Berat badan di bawah normal")
                    faktor_count += 1
                if calcium == "Rendah": 
                    st.write("- Asupan kalsium tidak mencukupi")
                    faktor_count += 1
                if vitd == "Tidak cukup": 
                    st.write("- Asupan vitamin D kurang")
                    faktor_count += 1
                if activity == "Kurang aktif": 
                    st.write("- Aktivitas fisik rendah")
                    faktor_count += 1
                if smoke == "Ya": 
                    st.write("- Kebiasaan merokok aktif")
                    faktor_count += 1
                if alkohol == "Sedang": 
                    st.write("- Konsumsi alkohol reguler")
                    faktor_count += 1
                if fracture == "Ya": 
                    st.write("- Riwayat patah tulang sebelumnya")
                    faktor_count += 1
                
                st.markdown("---")
                st.info(f"📌 **Total Faktor Risiko:** {faktor_count} faktor teridentifikasi")
                st.warning("💡 **Rekomendasi:** Segera konsultasikan dengan dokter untuk pemeriksaan lebih lanjut.")
                
            else:
                st.success("✅ **Tidak Terdeteksi Osteoporosis**")
                st.markdown("**Faktor Protektif yang Mendukung:**")
                
                faktor_count = 0
                if age <= 50: 
                    st.write("- Usia masih dalam rentang optimal")
                    faktor_count += 1
                if family == "Tidak": 
                    st.write("- Tidak ada riwayat keluarga")
                    faktor_count += 1
                if hormonal == "Normal": 
                    st.write("- Status hormonal normal")
                    faktor_count += 1
                if weight == "Normal": 
                    st.write("- Berat badan ideal")
                    faktor_count += 1
                if calcium == "Cukup": 
                    st.write("- Asupan kalsium mencukupi")
                    faktor_count += 1
                if vitd == "Cukup": 
                    st.write("- Asupan vitamin D optimal")
                    faktor_count += 1
                if activity == "Aktif": 
                    st.write("- Aktivitas fisik teratur")
                    faktor_count += 1
                if smoke == "Tidak": 
                    st.write("- Tidak merokok")
                    faktor_count += 1
                if alkohol == "Tidak": 
                    st.write("- Tidak konsumsi alkohol")
                    faktor_count += 1
                if fracture == "Tidak": 
                    st.write("- Tidak ada riwayat patah tulang")
                    faktor_count += 1
                
                st.markdown("---")
                st.info(f"📌 **Total Faktor Protektif:** {faktor_count} faktor mendukung")
                st.success("💡 **Saran:** Pertahankan gaya hidup sehat dan lakukan pemeriksaan rutin.")

    else:
        st.info("👆 Klik tombol **Mulai Prediksi** untuk melihat hasil analisis")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class='glass-card' style='text-align: center; padding: 1.5rem;'>
    <p style='color: #64748b; margin: 0; font-size: 0.9rem;'>
        ⚕️ <strong>Disclaimer:</strong> Hasil prediksi ini hanya sebagai alat bantu skrining awal. 
        Konsultasikan dengan tenaga medis profesional untuk diagnosis yang akurat.
    </p>
</div>
""", unsafe_allow_html=True)
