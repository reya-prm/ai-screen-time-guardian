# ====================================================
# Project: AI Screen-Time Guardian
# Stack: Python, Streamlit & Google Gemini API
# Developer: reya-prm
# Version: 1.4 (Auto Model Detection & Smart Fallback)
# ====================================================

import streamlit as st
import google.generativeai as genai

# Konfigurasi Tampilan Web
st.set_page_config(page_title="AI Screen-Time Guardian", page_icon="🛡️", layout="centered")

st.title("🛡️ AI Screen-Time Guardian")
st.caption("Aplikasi AI Pembasmi Doomscrolling & Penjaga Produktivitas")

# Sidebar untuk Input API Key
st.sidebar.header("⚙️ Pengaturan")

secrets_key = st.secrets.get("GEMINI_API_KEY", "")
api_key = secrets_key or st.sidebar.text_input("Masukkan Gemini API Key Kamu:", type="password")

# System Instruction untuk AI Guardian
SYSTEM_PROMPT = """
Bertindaklah sebagai 'AI Screen-Time Guardian', seorang mentor digital yang cerdas, memiliki selera humor tinggi, tapi tegas. Tugas utamanya adalah membantuku mengurangi kecanduan HP dan doomscrolling.

Setiap kali user memberitahumu bahwa mereka ingin membuka aplikasi hiburan (misal: TikTok, IG, Game, Youtube), kamu HARUS memberikan respon dengan struktur tegas berikut:

1. 💸 **Analisis Dampak (Finansial & Waktu):** Hitung berapa estimasi waktu yang terbuang jika diakumulasi mingguan/tahunan, dan konversikan ke dampak finansial/potensi karir yang hilang secara realistis & humoris.
2. 🧠 **Tantangan Edukasi Singkat:** Berikan 1 pertanyaan kuis pengetahuan/skill (teknologi, keuangan, atau bahasa Inggris). Jika user bisa menjawab benar, janjikan 'izin virtual' 10 menit.
3. 🏃‍♂️ **Rekomendasi Micro-Task:** Berikan 1 ide kegiatan fisik/produktif singkat selama 3 menit sebagai alternatif instan.
"""

if api_key:
    try:
        genai.configure(api_key=api_key)

        st.write("---")
        user_input = st.text_input(
            "Apa yang ingin kamu buka/lakukan sekarang?", 
            placeholder="Contoh: Mau nonton Reel Instagram 45 menit nih..."
        )

        if st.button("Minta Izin Guardian 🛡️", type="primary"):
            if user_input:
                with st.spinner("AI Guardian sedang menganalisis godaanmu..."):
                    # 1. Cari semua model yang didukung oleh API Key ini secara otomatis
                    all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    
                    # 2. Urutan prioritas model yang akan dicoba
                    priority_models = [
                        'models/gemini-2.0-flash',
                        'models/gemini-1.5-flash',
                        'models/gemini-2.0-flash-lite',
                        'models/gemini-1.5-pro'
                    ]
                    
                    target_model = None
                    for p_model in priority_models:
                        if p_model in all_models:
                            target_model = p_model
                            break
                    
                    # Jika tidak ada di daftar prioritas, pakai model pertama yang tersedia
                    if not target_model and all_models:
                        target_model = all_models[0]

                    if target_model:
                        model = genai.GenerativeModel(
                            model_name=target_model,
                            system_instruction=SYSTEM_PROMPT
                        )
                        response = model.generate_content(user_input)
                        
                        st.success(f"Analisis Guardian Selesai!")
                        st.markdown(response.text)
                    else:
                        st.error("Tidak ada model Gemini yang aktif untuk API Key ini. Silakan buat API Key baru di project baru.")
            else:
                st.warning("Tuliskan dulu godaan aplikasi apa yang mau kamu buka!")

    except Exception as e:
        st.error(f"Terjadi kesalahan pada API Key atau Layanan Gemini: {e}")
else:
    st.info("👈 Masukkan **Gemini API Key** kamu di menu Sidebar sebelah kiri untuk mengaktifkan AI Guardian!")

st.write("---")
st.caption("🚀 Built with Python & Streamlit | Powered by Google Gemini API")