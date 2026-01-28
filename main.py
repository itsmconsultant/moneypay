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

# 2. CSS KUSTOM (Target spesifik area Main Menu)
st.markdown("""
    <style>
    
    /* Maksa kontainer kolom agar lebih rapat dan lebar */
    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    /* Style CARD hanya untuk Main Content */
    [data-testid="stMain"] div.stButton > button {
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid #e6e9ef;
        border-radius: 12px;
        padding: 50px 10px; 
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
        
        /* Kunci agar Card Lebar */
        width: 100% !important;
        min-height: 180px;
        
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    [data-testid="stMain"] div.stButton > button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: #fcfcfc;
        transform: scale(1.02);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }

    /* Kembalikan Sidebar ke tombol Standar Streamlit */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        padding: 5px 15px !important;
        min-height: unset !important;
        width: 100% !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        font-weight: normal !important;
        box-shadow: none !important;
        transform: none !important;
        border: 1px solid rgba(49, 51, 63, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. KONEKSI & NAVIGASI
conn = st.connection("supabase", type=SupabaseConnection)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # SIDEBAR
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
        st.write("Pilih layanan di bawah ini:")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # GUNAKAN 3 ATAU 4 KOLOM (Semakin sedikit kolom, Card semakin lebar)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📤\n\nUpload Data", key="card_upload"):
                st.session_state["current_page"] = "upload"
                st.rerun()
        with col2:
            st.button("📊\n\nReport Sales", key="card_rep", disabled=True)
        with col3:
            st.button("📦\n\nInventory", key="card_inv", disabled=True)
        with col4:
            st.button("💰\n\nSettlement", key="card_set", disabled=True)

    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
