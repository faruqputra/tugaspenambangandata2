import streamlit as st
import joblib
import numpy as np

# ================= TAMPILAN =================
st.set_page_config(
    page_title="Prediksi Osteoporosis",
    page_icon="🦴",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
/* Background utama */
div[data-testid="stAppViewContainer"] {
    background-color: #f9fafb;
    color: #111827;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* Card sederhana */
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* Judul */
h1 {
    color: #1f2937;
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 0.2rem;
}

/* Subjudul */
h2, h3 {
    color: #374151;
}

/* Tombol minimalis */
.stButton>button {
    background: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
    width: 100%;
    transition: background 0.2s ease;
}
.stButton>button:hover {
    background: #2563eb;
}

/* Input spacing */
.css-1d391kg {margin-bottom: 12px;} 
</style>
""", unsafe_allow_html=True)

# ================= MODEL =================
model = joblib.load("model_dt.pkl")
scaler = joblib.load("scaler.pkl")

# ================= HEADER =================
st.markdown("<h1>🦴 Prediksi Osteoporosis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#6b7280;font-size:14px;'>Aplikasi Berbasis Decision Tree</p>", unsafe_allow_html=True)

# ================= LAYOUT DUA KOLOM =================
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Data Pasien")

    age = st.number_input("Usia", 18, 100, 30)
    gender = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    hormonal = st.selectbox("Perubahan Hormon", ["Normal", "Pasca menopause"])
    family = st.selectbox("Riwayat Keluarga", ["Tidak", "Ya"])
    race = st.selectbox("Ras/Etnis", ["Afrika-Amerika", "Asia", "Kaukasia"])
    weight = st.selectbox("Berat Badan", ["Normal", "Kurus"])
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

data = np.array([[age,
    map_gender[gender], map_hormonal[hormonal], map_family[family],
    map_race[race], map_weight[weight], map_calcium[calcium], map_vitd[vitd],
    map_activity[activity], map_smoke[smoke], map_alkohol[alkohol],
    map_medical[medical], map_meds[meds], map_fracture[fracture]
]])
data_scaled = scaler.transform(data)

# ================= HASIL PREDIKSI =================
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Prediksi")
    
    if st.button("Prediksi"):
        hasil = model.predict(data_scaled)[0]

        if hasil == 1:
            st.error("Mengalami Osteoporosis")
            st.markdown("**Faktor yang Memengaruhi:**")
            if age > 50: st.write("- Usia di atas 50 tahun")
            if family == "Ya": st.write("- Ada riwayat keluarga")
            if hormonal == "Pasca menopause": st.write("- Pasca menopause")
            if weight == "Kurus": st.write("- Berat badan kurus")
            if calcium == "Rendah": st.write("- Asupan kalsium rendah")
            if vitd == "Tidak cukup": st.write("- Vitamin D tidak cukup")
            if activity == "Kurang aktif": st.write("- Aktivitas fisik rendah")
            if smoke == "Ya": st.write("- Merokok")
            if alkohol == "Sedang": st.write("- Konsumsi alkohol")
            if fracture == "Ya": st.write("- Pernah patah tulang")
        else:
            st.success("Tidak Mengalami Osteoporosis")
            st.markdown("**Kondisi Relatif Aman:**")
            if age <= 50: st.write("- Usia masih relatif muda")
            if family == "Tidak": st.write("- Tidak ada riwayat keluarga")
            if hormonal == "Normal": st.write("- Hormon normal")
            if weight == "Normal": st.write("- Berat badan normal")
            if calcium == "Cukup": st.write("- Kalsium cukup")
            if vitd == "Cukup": st.write("- Vitamin D cukup")
            if activity == "Aktif": st.write("- Aktivitas fisik baik")
            if smoke == "Tidak": st.write("- Tidak merokok")
            if alkohol == "Tidak": st.write("- Tidak konsumsi alkohol")
            if fracture == "Tidak": st.write("- Tidak pernah patah tulang")

    st.markdown("</div>", unsafe_allow_html=True)
