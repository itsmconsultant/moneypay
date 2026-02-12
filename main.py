import streamlit as st
from st_supabase_connection import SupabaseConnection
import extra_streamlit_components as stx  # Import library cookie
from login import show_login
from upload_data import show_upload_dashboard
from process_data import show_run_procedure
from report_rekonsiliasi_transaksi_deposit_dan_settlement import show_report_deposit_settlement
from report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian import show_report_disbursement_durian
from report_detail_reversal import show_report_detail_reversal
from report_balance_flow import show_report_balance_flow
from delete_data import show_delete_data
from datetime import datetime, timedelta

# 1. SET WIDE MODE
st.set_page_config(page_title="Portal System", layout="wide", initial_sidebar_state="expanded")

# 2. INISIALISASI COOKIE MANAGER
cookie_manager = stx.CookieManager()

# 3. KONEKSI SUPABASE
conn = st.connection("supabase", type=SupabaseConnection)

# 4. LOGIKA CEK LOGIN VIA COOKIE
# Kita ambil flag 'is_logged_in' dari cookie browser
is_logged_in_cookie = cookie_manager.get(cookie="is_logged_in")

if "authenticated" not in st.session_state:
    if is_logged_in_cookie == "true":
        st.session_state["authenticated"] = True
        # Ambil email dari cookie jika ada
        st.session_state["user_email"] = cookie_manager.get(cookie="user_email")
    else:
        st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

# --- LOGIKA NAVIGASI ---
if not st.session_state.get("authenticated"):
    # Tampilkan halaman login
    # Catatan: Di dalam login.py, setelah login sukses, 
    # Anda harus menambahkan: cookie_manager.set("is_logged_in", "true")
    show_login(conn, cookie_manager)
    
    # Cek lagi setelah login sukses di login.py
    if st.session_state.get("authenticated"):
        cookie_manager.set("is_logged_in", "true", expires_at=datetime.now() + timedelta(days=1))
        cookie_manager.set("user_email", st.session_state.get("user_email"), expires_at=datetime.now() + timedelta(days=1))
        st.rerun()
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
        
        if st.button("🏠 Home Menu", use_container_width=True):
            st.session_state["current_page"] = "menu"
            st.rerun()
            
        # Logout melalui Tombol
        if st.button("🚪 Logout", key="side_logout", use_container_width=True):
            try:
                # 1. Sign out dari Supabase
                conn.client.auth.sign_out()
            except:
                pass
            
            # 2. HAPUS COOKIE DENGAN PENGECEKAN (Safety Check)
            # Menggunakan loop untuk memastikan kita hanya menghapus kunci yang benar-benar ada
            current_cookies = cookie_manager.get_all()
            if current_cookies:
                if "is_logged_in" in current_cookies:
                    cookie_manager.delete("is_logged_in")
                if "user_email" in current_cookies:
                    cookie_manager.delete("user_email")
            
            # 3. Bersihkan session state secara menyeluruh
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # 4. Berikan pesan sukses sejenak lalu paksa rerun
            st.success("Logout berhasil...")
            st.rerun()

    # --- KONTEN UTAMA (Sama seperti sebelumnya) ---
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
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📊 Rekon Deposit", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_deposit_dan_settlement"; st.rerun()
        with col4:
            if st.button("📊 Rekon Disbursement", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian"; st.rerun()

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
