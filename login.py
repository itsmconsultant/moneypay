import streamlit as st
from st_supabase_connection import SupabaseConnection

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Login - Excel Uploader", layout="centered")

# 3. Inisialisasi Koneksi ke Supabase
# Pastikan SUPABASE_URL dan SUPABASE_KEY sudah ada di Secrets
conn = st.connection("supabase", type=SupabaseConnection)

# 4. Fungsi Utama Login
def login_page():
    st.title("🔐 Login ke Sistem")
    st.write("Silakan masukkan email dan password Anda.")

    # Menggunakan form agar input diproses sekaligus saat tombol diklik
    with st.form("login_form"):
        email = st.text_input("Alamat Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Masuk")

        if submit_button:
            if email and password:
                try:
                    # Proses autentikasi menggunakan library Supabase
                    response = conn.client.auth.sign_in_with_password({
                        "email": email, 
                        "password": password
                    })
                    
                    # Jika berhasil, simpan status login ke Session State
                    if response.user:
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = response.user.email
                        st.success("Login Berhasil! Mengalihkan...")
                        st.rerun()
                        
                except Exception as e:
                    # Jika login gagal (email/password salah)
                    st.error(f"Gagal Login: Pastikan email dan password benar.")
            else:
                st.warning("Mohon isi email dan password.")

# 5. Logika Navigasi
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Tampilan berdasarkan status login
if not st.session_state["authenticated"]:
    login_page()
else:
    # --- HALAMAN SETELAH LOGIN BERHASIL ---
    st.sidebar.title("Informasi Akun")
    st.sidebar.write(f"Email: {st.session_state['user_email']}")
    
    if st.sidebar.button("Keluar (Logout)"):
        conn.client.auth.sign_out()
        st.session_state["authenticated"] = False
        st.rerun()

    st.success(f"Selamat datang, {st.session_state['user_email']}!")
    st.write("Anda sekarang berada di dalam sistem yang aman.")
    
    # Di sini Anda bisa memanggil fungsi dashboard upload Anda yang sebelumnya
    # Contoh: display_upload_dashboard()
