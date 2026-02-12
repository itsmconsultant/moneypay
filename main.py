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
conn = st.connection(
    "supabase",
    type=SupabaseConnection
)

# 3. LOGIKA PROTEKSI SESI (AUTO-LOGOUT PADA TAB BARU)
# st.session_state['init_check'] hanya ada selama tab aktif. 
# Jika tab ditutup dan dibuka lagi, variable ini hilang, memicu sign_out global.
if "init_check" not in st.session_state:
    try:
        # Hapus semua sesi di database & lokal agar tidak "langsung login"
        conn.client.auth.sign_out(scope="global")
    except:
        pass
    
    # Reset semua status login
    st.session_state["authenticated"] = False
    st.session_state["init_check"] = True # Tandai bahwa pengecekan awal selesai
    st.rerun()

# 4. PENGECEKAN AUTHENTICATION NORMAL
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    show_login(conn)
else:
    # --- LOGIKA AUTO-REFRESH SETELAH LOGIN ---
    if "has_refreshed" not in st.session_state:
        st.session_state["has_refreshed"] = False

    if not st.session_state["has_refreshed"]:
        st.session_state["has_refreshed"] = True
        st.rerun() 

    # Ambil email user untuk tampilan UI
    if "user_email" not in st.session_state:
        try:
            session = conn.client.auth.get_session()
            if session:
                st.session_state["user_email"] = session.user.email
        except:
            st.session_state["user_email"] = "User"

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "menu"

    # --- SIDEBAR (Navigasi Samping) ---
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        if st.button("🏠 Home Menu", key="side_home", use_container_width=True):
            st.session_state["current_page"] = "menu"
            st.rerun()
            
        # Logout Global melalui Tombol
        if st.button("🚪 Logout", key="side_logout", use_container_width=True):
            try:
                # 1. Sign out dari Supabase terlebih dahulu
                conn.client.auth.sign_out(scope="global")
            except Exception as e:
                # Jika gagal (misal koneksi terputus), kita abaikan agar tetap bisa clear state lokal
                pass
            
            # 2. Bersihkan semua session state secara manual
            st.session_state["authenticated"] = False
            
            # Hapus flag-flag kontrol agar aplikasi benar-benar reset
            keys_to_clear = ["has_refreshed", "init_check", "user_email", "current_page"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            # 3. Paksa kembali ke halaman login
            st.rerun()

    # --- KONTEN UTAMA ---
    if st.session_state["current_page"] == "menu":
        st.title("Data")
        st.write("Harap upload dan proses data terlebih dahulu sebelum menarik report!")
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤\n\n\n\nUpload Data", key="btn_upload", use_container_width=True):
                st.session_state["current_page"] = "upload"
                st.rerun()
        with col2:
            if st.button("⚙️\n\n\n\nProcess Data", key="card_proc", use_container_width=True):
                st.session_state["current_page"] = "procedure"
                st.rerun()
        with col1:
            if st.button("🗑️\n\n\n\nDelete Data", key="btn_delete", use_container_width=True):
                st.session_state["current_page"] = "delete"
                st.rerun()
        
        st.title("Report")
        st.write("Silakan pilih report yang ingin Anda akses:")
        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📊\n\n\n\nReport Rekonsiliasi Transaksi Deposit dan Settlement", key="r1", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_deposit_dan_settlement"
                st.rerun()
        with col4:
            if st.button("📊\n\n\n\nRekonsiliasi Transaksi Disbursement dan Saldo Durian", key="r2", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_disbursement_dan_saldo_durian"
                st.rerun()
        with col3:
            if st.button("📊\n\n\n\nReport Detail Reversal", key="r3", use_container_width=True):
                st.session_state["current_page"] = "report_detail_reversal"
                st.rerun()
        with col4:
            if st.button("📊\n\n\n\nReport Balance Flow", key="r4", use_container_width=True):
                st.session_state["current_page"] = "report_balance_flow"
                st.rerun()

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
