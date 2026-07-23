# ====================================================
# Project: AI Screen-Time Guardian
# Stack: Python, Streamlit & Google Gemini API
# Developer: reya-prm
# Version: 1.3 (Fixed Model Routing & Fallback)
# ====================================================

import streamlit as st
import google.generativeai as genai

# Konfigurasi Tampilan Web
st.set_page_config(page_title="AI Screen-Time Guardian", page_icon="🛡️", layout="centered")

st.title("🛡️ AI Screen-Time Guardian")
st.caption("Aplikasi AI Pembasmi Doomscrolling & Penjaga Produktivitas")

# Sidebar untuk Input API Key
st.sidebar.header("⚙️ Pengaturan")

# Ambil API Key dari Streamlit Secrets jika ada, atau dari input Sidebar
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

# Cek API Key
if api_key:
    try:
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
                    # Coba panggil model gemini-2.0-flash yang aktif dan stabil
                    try:
                        model = genai.GenerativeModel(
                            model_name='gemini-2.0-flash',
                            system_instruction=SYSTEM_PROMPT
                        )
                        response = model.generate_content(user_input)
                    except Exception:
                        # Fallback ke gemini-2.0-flash-lite jika ada kendala
                        model = genai.GenerativeModel(
                            model_name='gemini-2.0-flash-lite',
                            system_instruction=SYSTEM_PROMPT
                        )
                        response = model.generate_content(user_input)

                    st.success("Analisis Guardian Selesai!")
                    st.markdown(response.text)
            else:
                st.warning("Tuliskan dulu godaan aplikasi apa yang mau kamu buka!")

    except Exception as e:
        st.error(f"Terjadi kesalahan pada API Key atau Layanan Gemini: {e}")
else:
    st.info("👈 Masukkan **Gemini API Key** kamu di menu Sidebar sebelah kiri untuk mengaktifkan AI Guardian!")

# Footer Tambahan
st.write("---")
st.caption("🚀 Built with Python & Streamlit | Powered by Google Gemini API")