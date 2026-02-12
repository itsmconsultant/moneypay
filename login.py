import streamlit as st

def show_login(conn):
    # Menampilkan judul di tengah halaman login
    st.title("🔐 Login")
    
    # Membuat form login agar input email dan password dikirim bersamaan
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk", use_container_width=True)
        
        if submit:
            try:
                # Melakukan autentikasi menggunakan Supabase Auth
                res = conn.client.auth.sign_in_with_password({
                    "email": email, 
                    "password": password
                })
                
                # Jika user ditemukan, tandai session sebagai terautentikasi
                if res.user:
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = res.user.email
                    st.success("Login Berhasil! Mengalihkan ke Dashboard...")
                    
                    # Refresh halaman untuk memicu navigasi ke Menu Utama
                    st.rerun()
                else:
                    st.error("Login Gagal: User tidak ditemukan.")
                    
            except Exception as e:
                # Memberikan pesan error yang jelas jika terjadi kegagalan koneksi atau kredensial salah
                st.error("Login Gagal: Pastikan email dan password benar.")
