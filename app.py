# ====================================================
# Project: AI Screen-Time Guardian
# Stack: Python, Streamlit & Google Gemini API
# Developer: reya-prm
# Version: 1.5 (Full & Secure)
# ====================================================

import streamlit as st
import google.generativeai as genai

# Konfigurasi Tampilan Web
st.set_page_config(
    page_title="AI Screen-Time Guardian", 
    page_icon="🛡️", 
    layout="centered"
)

st.title("🛡️ AI Screen-Time Guardian")
st.caption("Aplikasi AI Pembasmi Doomscrolling & Penjaga Produktivitas")

# Sidebar untuk Input API Key (Aman dari GitHub Push Protection)
st.sidebar.header("⚙️ Pengaturan")

# Ambil API Key dari Streamlit Secrets jika ada, atau dari input Sidebar
secrets_key = st.secrets.get("GEMINI_API_KEY", "")
api_key = secrets_key or st.sidebar.text_input(
    "Masukkan Gemini API Key Kamu:", 
    type="password",
    help="Dapatkan API Key gratis di https://aistudio.google.com/app/apikey"
)

# System Instruction untuk AI Guardian
SYSTEM_PROMPT = """
Bertindaklah sebagai 'AI Screen-Time Guardian', seorang mentor digital yang cerdas, memiliki selera humor tinggi, tapi tegas. Tugas utamanya adalah membantuku mengurangi kecanduan HP dan doomscrolling.

Setiap kali user memberitahumu bahwa mereka ingin membuka aplikasi hiburan (misal: TikTok, IG, Game, Youtube), kamu HARUS memberikan respon dengan struktur tegas berikut:

1. 💸 **Analisis Dampak (Finansial & Waktu):** Hitung berapa estimasi waktu yang terbuang jika diakumulasi mingguan/tahunan, dan konversikan ke dampak finansial/potensi karir yang hilang secara realistis & humoris.
2. 🧠 **Tantangan Edukasi Singkat:** Berikan 1 pertanyaan kuis pengetahuan/skill (teknologi, keuangan, atau bahasa Inggris). Jika user bisa menjawab benar, janjikan 'izin virtual' 10 menit.
3. 🏃‍♂️ **Rekomendasi Micro-Task:** Berikan 1 ide kegiatan fisik/produktif singkat selama 3 menit sebagai alternatif instan.
"""

# Cek apakah API Key sudah diisi
if api_key:
    try:
        # Konfigurasi API Gemini
        genai.configure(api_key=api_key)

        # Form Input User
        st.write("---")
        user_input = st.text_input(
            "Apa yang ingin kamu buka/lakukan sekarang?", 
            placeholder="Contoh: Mau nonton Reel Instagram 45 menit nih..."
        )

        if st.button("Minta Izin Guardian 🛡️", type="primary"):
            if user_input:
                with st.spinner("AI Guardian sedang menganalisis godaanmu..."):
                    try:
                        # 1. Cari semua model yang didukung oleh API Key ini secara otomatis
                        available_models = [
                            m.name for m in genai.list_models() 
                            if 'generateContent' in m.supported_generation_methods
                        ]
                        
                        # 2. Urutan prioritas model
                        priority_models = [
                            'models/gemini-2.0-flash',
                            'models/gemini-1.5-flash',
                            'models/gemini-2.0-flash-lite',
                            'models/gemini-1.5-pro'
                        ]
                        
                        selected_model = None
                        for model_name in priority_models:
                            if model_name in available_models:
                                selected_model = model_name
                                break
                        
                        # Fallback: jika tidak ada di list prioritas, pakai model pertama yang ada
                        if not selected_model and available_models:
                            selected_model = available_models[0]

                        if selected_model:
                            model = genai.GenerativeModel(
                                model_name=selected_model,
                                system_instruction=SYSTEM_PROMPT
                            )
                            response = model.generate_content(user_input)
                            
                            st.success("Analisis Guardian Selesai!")
                            st.markdown(response.text)
                        else:
                            st.error("Tidak ada model Gemini yang aktif untuk API Key ini.")
                    
                    except Exception as err:
                        st.error(f"Gagal memanggil API Gemini: {err}")
            else:
                st.warning("Tuliskan dulu godaan aplikasi apa yang mau kamu buka!")

    except Exception as e:
        st.error(f"Terjadi kesalahan pada konfigurasi API Key: {e}")
else:
    st.info("👈 Masukkan **Gemini API Key** kamu di menu Sidebar sebelah kiri untuk mengaktifkan AI Guardian!")

# Footer Tambahan
st.write("---")
st.caption("🚀 Built with Python & Streamlit | Powered by Google Gemini API")