import streamlit as st
import pandas as pd
from sqlalchemy import text
import datetime # Import datetime secara utuh lebih aman

def show_report_rekonsiliasi_transaksi_deposit_dan_settlement():
    st.title("📊 Rekonsiliasi Transaksi Deposit dan Settlement")
    st.divider()

    # 1. Input Parameter Tanggal
    col1, col2 = st.columns([1, 2])
    with col1:
        # Gunakan datetime.date.today() agar lebih eksplisit dan menghindari NameError
        default_date = st.session_state.get('last_date', datetime.date.today())
        selected_date = st.date_input("Pilih Tanggal:", default_date)
    
    # Simpan tanggal terakhir ke session state agar tidak reset
    st.session_state['last_date'] = selected_date

    # 2. Tombol Cari
    if st.button("Tampilkan Data", use_container_width=True):
        db_sql = st.connection("postgresql", type="sql")
        tanggal_str = selected_date.strftime("%Y-%m-%d")
        
        with st.spinner(f"Mengambil data untuk tanggal {tanggal_str}..."):
            try:
                query = text("""
                    SELECT merchant, tanggal_proses, keterangan, jumlah_transaksi, 
                           jumlah_transaksi_sesuai_rate, penambahan_rupiah, 
                           pengurangan_rupiah, rekonsiliasi_jumlah_transaksi, 
                           rekonsiliasi_rupiah, rekonsiliasi_tambah_kurang, 
                           saldo_rekonsiliasi_rupiah
                    FROM project1.summary_deposit
                    WHERE tanggal_proses::date = :tgl
                    ORDER BY urutan ASC
                """)
                
                df = db_sql.query(query, params={"tgl": tanggal_str})

                if not df.empty:
                    st.success(f"Ditemukan {len(df)} baris data.")
                    
                    # Tampilkan Tombol Download
                    st.download_button(
                        label="📥 Download CSV",
                        data=df.to_csv(index=False),
                        file_name=f"report_{tanggal_str}.csv",
                        mime="text/csv"
                    )
                    
                    # Tampilkan Tabel
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning("Tidak ada data ditemukan untuk tanggal tersebut.")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat mengambil data: {e}")

    # Tombol Kembali di Sidebar
    if st.sidebar.button("⬅️ Kembali ke Menu Utama"):
        st.session_state["current_page"] = "menu"
        st.rerun()
