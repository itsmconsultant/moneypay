import streamlit as st
from st_supabase_connection import SupabaseConnection
# Import fungsi dari file lain
from login import show_login
from upload_data import show_upload_dashboard

# Konfigurasi Halaman (Hanya boleh ada satu di file utama)
st.set_page_config(page_title="Sistem Upload Data", layout="wide")

# Inisialisasi Koneksi
conn = st.connection("supabase", type=SupabaseConnection)

# Cek Status Login di Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Logika Navigasi
if not st.session_state["authenticated"]:
    show_login(conn)
else:
    show_upload_dashboard(conn)
