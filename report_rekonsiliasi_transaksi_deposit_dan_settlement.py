import streamlit as st
import pandas as pd
import datetime

def show_report_deposit_settlement(conn):
    st.title("📊 Rekonsiliasi Transaksi Deposit dan Settlement")
    st.write("Menampilkan data langsung dari database Supabase.")
    st.divider()

    # 1. Input Parameter Tanggal
    col1, col2 = st.columns([1, 2])
    with col1:
        # Default ke tanggal hari ini jika belum ada di session state
        default_date = st.session_state.get('last_date', datetime.date.today())
        selected_date = st.date_input("Pilih Tanggal:", default_date)
    
    st.session_state['last_date'] = selected_date

    # 2. Tombol Cari
    if st.button("Tampilkan Data", use_container_width=True):
        tanggal_str = selected_date.strftime("%Y-%m-%d")
        
        with st.spinner(f"Mengambil data untuk tanggal {tanggal_str}..."):
            try:
                # 3. Menggunakan API Select Supabase (Tanpa SQLAlchemy)
                # .table() merujuk ke nama tabel, .select("*") mengambil semua kolom
                response = conn.client.schema("project1").table("summary_deposit") \
                    .select("*") \
                    .eq("tanggal_proses", tanggal_str) \
                    .order("urutan", desc=False) \
                    .execute()

                # 4. Menampilkan Hasil
                if response.data:
                    df = pd.DataFrame(response.data)
                    st.success(f"Berhasil menemukan {len(df)} data.")
                    
                    # Tombol Download
                    st.download_button(
                        label="📥 Download CSV",
                        data=df.to_csv(index=False),
                        file_name=f"report_{tanggal_str}.csv",
                        mime="text/csv"
                    )
                    
                    # Tampilkan Tabel
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"Tidak ada data ditemukan untuk tanggal {tanggal_str}.")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

    # Sidebar Kembali
    if st.sidebar.button("🏠 Kembali ke Menu Utama"):
        st.session_state["current_page"] = "menu"
        st.rerun()
