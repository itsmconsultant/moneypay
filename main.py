import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login
from upload_data import show_upload_dashboard

# 1. SET WIDE MODE DEFAULT
st.set_page_config(
    page_title="Portal System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS KUSTOM (Target spesifik hanya untuk Card di Main Menu)
st.markdown("""
    <style>
    /* Style khusus untuk Container Card di Main Menu */
    /* Kita gunakan selector khusus agar tidak merusak Sidebar */
    [data-testid="stMain"] div.stButton > button {
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid #e6e9ef;
        border-radius: 15px;
        padding: 80px 20px; /* Padding atas-bawah diperbesar untuk kesan Card */
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%; /* Memaksa lebar mengikuti kolom */
        min-height: 200px; /* Memastikan tinggi minimum agar berbentuk kotak */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    [data-testid="stMain"] div.stButton > button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        background-color: #ffffff;
    }

    /* Memastikan tombol Sidebar tetap standar (Tidak terpengaruh CSS Card) */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent;
        padding: 0.25rem 0.75rem;
        min-height: 0px;
        border-radius: 4px;
        font-size: 14px;
        font-weight: normal;
        box-shadow: none;
        width: auto;
    }
    </style>
""", unsafe_allow_html=True)

# 3. INISIALISASI KONEKSI & SESSION
conn = st.connection("supabase", type=SupabaseConnection)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

# --- LOGIKA NAVIGASI ---
if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # SIDEBAR (Tombol standar)
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        if st.button("Home Menu", key="side_home"):
            st.session_state["current_page"] = "menu"
            st.rerun()
        if st.button("Logout", key="side_logout"):
            conn.client.auth.sign_out()
            st.session_state["authenticated"] = False
            st.rerun()

    # KONTEN UTAMA
    if st.session_state["current_page"] == "menu":
        st.title("Main Menu")
        st.write("Silakan pilih modul yang ingin Anda akses:")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # GRID LAYOUT (4 Kolom untuk Card yang lebih lebar)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Gunakan \n yang cukup untuk memisahkan Icon dan Teks
            if st.button("📤\n\nUpload Data", key="card_upload"):
                st.session_state["current_page"] = "upload"
                st.rerun()
        
        with col2:
            st.button("📊\n\nReport Sales", key="card_report", disabled=True)
            
        with col3:
            st.button("📦\n\nInventory", key="card_inv", disabled=True)
            
        with col4:
            st.button("💰\n\nSettlement", key="card_settle", disabled=True)

    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
