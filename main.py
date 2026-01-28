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
    
    /* 1. Paksa Grid Kolom agar menggunakan seluruh lebar yang ada */
    [data-testid="stHorizontalBlock"] {
        width: 100%;
        gap: 2rem;
    }

    /* 2. STYLE CARD UTAMA */
    [data-testid="stMain"] div.stButton > button {
        /* Reset & Base Style */
        background-color: #ffffff !important;
        color: #31333F !important;
        border: 1px solid #e6e9ef !important;
        border-radius: 15px !important;
        
        /* Ukuran Card */
        width: 250px !important;      /* Paksa lebar 100% dari kolom */
        min-width: 100% !important;  /* Tambahan penguat lebar */
        min-height: 250px !important; /* Tinggi kotak */
        padding: 20px !important;
        
        /* Layout isi di dalam tombol */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        
        /* Efek Shadow */
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        transition: all 0.3s ease-in-out !important;
        white-space: pre-wrap !important; /* Agar \n terbaca untuk pindah baris */
    }
    
    /* Efek Hover Card */
    [data-testid="stMain"] div.stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 20px rgba(0,0,0,0.15) !important;
    }

    /* 3. RESET SIDEBAR (Kembali ke tombol standar) */
    [data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        min-height: unset !important;
        min-width: unset !important;
        padding: 5px 10px !important;
        border-radius: 5px !important;
        font-size: 14px !important;
        background-color: transparent !important;
        box-shadow: none !important;
        border: 1px solid rgba(49, 51, 63, 0.2) !important;
        transform: none !important;
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
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤\n\nUpload Data", key="card_upload"):
                st.session_state["current_page"] = "upload"
                st.rerun()
        with col2:
            st.button("📊\n\nReport Sales", key="card_rep", disabled=True)


    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
