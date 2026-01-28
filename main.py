import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login
from upload_data import show_upload_dashboard
from process_data import show_run_procedure

# 1. SET WIDE MODE DEFAULT
st.set_page_config(
    page_title="Portal System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 3. KONEKSI & INISIALISASI SESSION
conn = st.connection("supabase", type=SupabaseConnection)

if "authenticated" not in st.session_state:
    try:
        # Mencoba mengambil sesi yang tersimpan di browser
        session = conn.client.auth.get_session()
        if session:
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = session.user.email
        else:
            st.session_state["authenticated"] = False
    except:
        st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

# --- LOGIKA NAVIGASI ---
if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # SIDEBAR (Navigasi Samping)
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        if st.button("🏠 Home Menu", key="side_home", use_container_width=True):
            st.session_state["current_page"] = "menu"
            st.rerun()
        if st.button("🚪 Logout", key="side_logout", use_container_width=True):
            conn.client.auth.sign_out()
            st.session_state["authenticated"] = False
            st.rerun()

    # KONTEN UTAMA
    if st.session_state["current_page"] == "menu":
        st.title("Main Menu")
        st.write("Silakan pilih modul yang ingin Anda akses:")
        st.divider()
        
        # Grid Menu menggunakan tombol standar Streamlit
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📤\n\nUpload Data", key="btn_upload", use_container_width=True):
                st.session_state["current_page"] = "upload"
                st.rerun()
        
        with col2: # Misalnya kotak kedua
            if st.button("⚙️\n\nRun Procedure", key="card_proc", use_container_width=True):
                st.session_state["current_page"] = "procedure"
                st.rerun()
            
        with col3:
            st.button("📦 Inventory", key="btn_inv", use_container_width=True, disabled=True)
            
        with col4:
            st.button("💰 Settlement", key="btn_settle", use_container_width=True, disabled=True)

    elif st.session_state["current_page"] == "upload":
        # Menampilkan halaman upload dari file upload_data.py
        show_upload_dashboard(conn)
        
    elif st.session_state["current_page"] == "procedure":
        show_run_procedure(conn)
