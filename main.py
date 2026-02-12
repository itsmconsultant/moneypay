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

# 2. KONEKSI KE SUPABASE
conn = st.connection("supabase", type=SupabaseConnection)

# 3. INISIALISASI SESSION STATE (Stateless/Tanpa Sesi Permanen)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

# --- LOGIKA NAVIGASI & PROTEKSI ---
if not st.session_state["authenticated"]:
    # Tampilkan halaman login tanpa cookie
    show_login(conn)
else:
    # --- LOGIKA AUTO-REFRESH SETELAH LOGIN (PENTING UNTUK STABILITAS WEBSOCKET) ---
    # Kode ini mencegah Error 1ST dengan menyegarkan koneksi tepat setelah login sukses
    if "has_refreshed" not in st.session_state:
        st.session_state["has_refreshed"] = False

    if not st.session_state["has_refreshed"]:
        st.session_state["has_refreshed"] = True
        st.rerun()  # Memaksa sinkronisasi ulang browser-server

    # --- SIDEBAR (Navigasi Samping) ---
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        
        if st.button("🏠 Home Menu", key="side_home", use_container_width=True):
            st.session_state["current_page"] = "menu"
            st.rerun()
            
        if st.button("🚪 Logout", key="side_logout", use_container_width=True):
            try:
                conn.client.auth.sign_out()
            except:
                pass
            
            # Reset semua status agar kembali ke login screen
            st.session_state["authenticated"] = False
            if "has_refreshed" in st.session_state:
                del st.session_state["has_refreshed"]
            st.rerun()

    # --- KONTEN UTAMA ---
    if st.session_state["current_page"] == "menu":
        st.title("Data & Report Menu")
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Upload Data", key="btn_upload", use_container_width=True):
                st.session_state["current_page"] = "upload"
                st.rerun()
            if st.button("🗑️ Delete Data", key="btn_delete", use_container_width=True):
                st.session_state["current_page"] = "delete"
                st.rerun()
        with col2:
            if st.button("⚙️ Process Data", key="card_proc", use_container_width=True):
                st.session_state["current_page"] = "procedure"
                st.rerun()
        
        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📊 Rekon Deposit", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_deposit_dan_settlement"
                st.rerun()
        with col4:
            if st.button("📊 Rekon Disbursement", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian"
                st.rerun()

    # --- ROUTING HALAMAN ---
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
