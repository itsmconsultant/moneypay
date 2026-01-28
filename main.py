import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login
from upload_data import show_upload_dashboard

# CSS untuk tampilan Grid Kotak Putih (Dashboard Style)
st.markdown("""
    <style>
    .main-button {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        color: black;
        font-weight: bold;
        display: block;
        margin-bottom: 20px;
        text-decoration: none;
    }
    .main-button:hover {
        background-color: #f0f2f6;
        border-color: #ff4b4b;
    }
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Konfigurasi Halaman
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

conn = st.connection("supabase", type=SupabaseConnection)

# --- LOGIKA NAVIGASI ---
if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # SATU-SATUNYA TEMPAT UNTUK SIDEBAR
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state['user_email']}")
        
        # Tombol kembali ke Menu Utama
        if st.button("Home Menu", key="home_btn"):
            st.session_state["current_page"] = "menu"
            st.rerun()
            
        # Tombol Logout
        if st.button("Logout", key="logout_btn"):
            conn.client.auth.sign_out()
            st.session_state["authenticated"] = False
            st.rerun()

    # Konten Utama
    if st.session_state["current_page"] == "menu":
        st.title("Main Menu")
        # Layout Grid (Kartu Putih)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Gunakan st.button sebagai kartu
            if st.button("📤 Upload Data", use_container_width=True, key="menu_upload"):
                st.session_state["current_page"] = "upload"
                st.rerun()
        with col2:
            st.button("📊 Report Sales", use_container_width=True, disabled=True)
        # Tambahkan col3, col4 dst jika perlu

    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
