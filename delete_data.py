import streamlit as st
from sqlalchemy import text
import time

# Gunakan decorator @st.dialog untuk membuat pop-up konfirmasi
@st.dialog("Konfirmasi Penghapusan")
def confirm_delete_dialog(selected_date):
    st.warning(f"Apakah Anda yakin ingin menghapus SEMUA data pada tanggal {selected_date}?")
    st.write("Tindakan ini tidak dapat dibatalkan.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ya, Hapus Sekarang", type="primary", use_container_width=True):
            # 1. Jalankan proses hapus
            success = execute_delete(selected_date)
            
            # 2. Jika sukses, tampilkan pesan di dalam dialog, tunggu sebentar, lalu rerun
            if success:
                st.success(f"Data berhasil dihapus!")
                time.sleep(2) # Memberi waktu pengguna membaca pesan sukses (2 detik)
                st.rerun()
    with col2:
        if st.button("Batal", use_container_width=True):
            st.rerun()

def execute_delete(selected_date):
    db_sql = st.connection("postgresql", type="sql")
    tanggal_str = selected_date.strftime("%Y-%m-%d")
    
    # Gunakan container kosong untuk spinner agar tidak merusak layout dialog
    with st.spinner(f"Menghapus data..."):
        try:
            with db_sql.session as session:
                sql_query = text("""
                    DELETE FROM moneypay.deposit WHERE payment_at::date = :tgl;
                    DELETE FROM moneypay.disbursement WHERE payment_at::date = :tgl;
                    DELETE FROM moneypay.saldo_durian WHERE transaction_time::date = :tgl;
                    DELETE FROM moneypay.settlement WHERE payment_date::date = :tgl;
                """)
                session.execute(sql_query, {"tgl": tanggal_str})
                session.commit()
                return True # Kembalikan True jika berhasil
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            return False

def show_delete_data(conn):
    st.title("🗑️ Hapus Data")
    st.write("Fitur ini hanya digunakan jika ada perbaikan / revisi data.")
    st.divider()
    
    selected_date = st.date_input("Pilih Tanggal Data yang akan dihapus :")
    
    # Tombol awal hanya memicu kemunculan pop-up
    if st.button("Hapus Data", type="secondary"):
        confirm_delete_dialog(selected_date)
