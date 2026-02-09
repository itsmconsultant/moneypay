import streamlit as st
from sqlalchemy import text

# Gunakan decorator @st.dialog untuk membuat pop-up konfirmasi
@st.dialog("Konfirmasi Penghapusan")
def confirm_delete_dialog(selected_date):
    st.warning(f"Apakah Anda yakin ingin menghapus SEMUA data pada tanggal {selected_date}?")
    st.write("Tindakan ini tidak dapat dibatalkan.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ya, Hapus Sekarang", type="primary", use_container_width=True):
            # Jalankan logika penghapusan di sini
            execute_delete(selected_date)
            st.rerun()
    with col2:
        if st.button("Batal", use_container_width=True):
            st.rerun()

def execute_delete(selected_date):
    db_sql = st.connection("postgresql", type="sql")
    tanggal_str = selected_date.strftime("%Y-%m-%d")
    
    with st.spinner(f"Menghapus data tanggal {tanggal_str}..."):
        try:
            with db_sql.session as session:
                # Disarankan memisahkan query agar lebih bersih atau gunakan BEGIN/COMMIT block
                sql_query = text("""
                    DELETE FROM moneypay.deposit WHERE payment_at::date = :tgl;
                    DELETE FROM moneypay.disbursement WHERE payment_at::date = :tgl;
                    DELETE FROM moneypay.saldo_durian WHERE transaction_time::date = :tgl;
                    DELETE FROM moneypay.settlement WHERE payment_date::date = :tgl;
                """)
                
                session.execute(sql_query, {"tgl": tanggal_str})
                session.commit()
                st.success(f"Data tanggal {tanggal_str} berhasil dihapus!")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

def show_delete_data(conn):
    st.title("🗑️ Hapus Data")
    st.write("Fitur ini hanya digunakan jika ada perbaikan / revisi data.")
    st.divider()
    
    selected_date = st.date_input("Pilih Tanggal Data yang akan dihapus :")
    
    # Tombol awal hanya memicu kemunculan pop-up
    if st.button("Hapus Data", type="secondary"):
        confirm_delete_dialog(selected_date)
