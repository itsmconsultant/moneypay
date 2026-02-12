import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login
from upload_data import show_upload_dashboard
from process_data import show_run_procedure
from report_rekonsiliasi_transaksi_deposit_dan_settlement import show_report_deposit_settlement
from report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian import show_report_disbursement_durian
from report_detail_reversal import show_report_detail_reversal
from report_balance_flow import show_report_balance_flow
from delete_data import show_delete_data

# 1. SET WIDE MODE DEFAULT
st.set_page_config(
    page_title="Portal System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. KONEKSI KE SUPABASE DENGAN CONFIG STORAGE KHUSUS
# Menggunakan 'sessionStorage' adalah cara terbaik untuk memastikan:
# - Refresh/Tab Baru: Tetap Login (karena dalam satu session browser)
# - Perangkat Lain: Harus Login (karena sessionStorage tidak disinkronkan antar perangkat)
conn = st.connection(
    "supabase",
    type=SupabaseConnection,
    config={
        "auth": {
            "storage_key": "portal-auth-cookie",
            "storage": "sessionStorage", 
            "persist_session": True
        }
    }
)

# 3. LOGIKA AUTENTIKASI
if "authenticated" not in st.session_state:
    try:
        # Cek sesi aktif di browser saat ini
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
if not st.session_state.get("authenticated"):
    show_login(conn)
else:
    # --- LOGIKA AUTO-REFRESH SETELAH LOGIN ---
    if "has_refreshed" not in st.session_state:
        st.session_state["has_refreshed"] = False

    if not st.session_state["has_refreshed"]:
        st.session_state["has_refreshed"] = True
        st.rerun() 

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        
        if st.button("🏠 Home Menu", key="side_home", use_container_width=True):
            st.session_state["current_page"] = "menu"
            st.rerun()
            
        if st.button("🚪 Logout", key="side_logout", use_container_width=True):
            try:
                # Gunakan pemanggilan tanpa parameter 'scope' jika terjadi TypeError
                conn.client.auth.sign_out()
            except Exception:
                # Abaikan error jika sesi sudah tidak ada di server
                pass
            
            # Bersihkan semua session state secara menyeluruh agar aplikasi reset
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Paksa kembali ke halaman login
            st.rerun()

    # --- KONTEN UTAMA ---
    # (Pilih halaman berdasarkan st.session_state["current_page"])
    if st.session_state["current_page"] == "menu":
        st.title("Data & Report Menu")
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Upload Data", key="btn_upload", use_container_width=True):
                st.session_state["current_page"] = "upload"; st.rerun()
            if st.button("🗑️ Delete Data", key="btn_delete", use_container_width=True):
                st.session_state["current_page"] = "delete"; st.rerun()
        with col2:
            if st.button("⚙️ Process Data", key="card_proc", use_container_width=True):
                st.session_state["current_page"] = "procedure"; st.rerun()
        
        st.divider()
        # Menu Report
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📊 Rekon Deposit", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_deposit_dan_settlement"; st.rerun()
            if st.button("📊 Detail Reversal", use_container_width=True):
                st.session_state["current_page"] = "report_detail_reversal"; st.rerun()
        with col4:
            if st.button("📊 Rekon Disbursement", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian"; st.rerun()
            if st.button("📊 Balance Flow", use_container_width=True):
                st.session_state["current_page"] = "report_balance_flow"; st.rerun()

    # --- ROUTING ---
    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
    elif st.session_state["current_page"] == "procedure":
        show_run_procedure(conn)
    elif st.session_state["current_page"] == "report_rekonsiliasi_transaksi_deposit_dan_settlement":
        show_report_deposit_settlement(conn)
    elif st.session_state["current_page"] == "report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian":
        show_report_disbursement_durian(conn)
    elif st.session_state["current_page"] == "report_detail_reversal":
        show_report_detail_reversal(conn)
    elif st.session_state["current_page"] == "report_balance_flow":
        show_report_balance_flow(conn)
    elif st.session_state["current_page"] == "delete":
        show_delete_data(conn)
