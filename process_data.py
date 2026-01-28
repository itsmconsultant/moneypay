import streamlit as st
from datetime import date

def show_run_procedure(conn):
    st.title("⚙️ Jalankan Store Procedure")
    st.write("Gunakan halaman ini untuk menjalankan prosedur `run_all_procedure` berdasarkan tanggal tertentu.")
    st.divider()

    # 1. Input Tanggal
    selected_date = st.date_input("Pilih Tanggal Parameter:", date.today())
    
    # Tombol eksekusi
    if st.button("Jalankan Prosedur", use_container_width=True):
        # Konversi tanggal ke string format ISO (YYYY-MM-DD) agar sesuai dengan PostgreSQL
        tanggal_str = selected_date.strftime("%Y-%m-%d")
        
        with st.spinner(f"Sedang menjalankan prosedur untuk tanggal {tanggal_str}..."):
            try:
                # Gunakan query manual dengan perintah CALL untuk Procedure
                # Kita menggunakan f-string untuk memasukkan parameter ke dalam string SQL
                query = f"CALL project1.run_all_procedure('{tanggal_str}')"
                
                # Eksekusi melalui conn.query (pastikan library mendukung atau gunakan client.postgrest)
                response = conn.client.postgrest.query(query).execute()
                
                st.success(f"Stored Procedure berhasil dipanggil untuk tanggal: {tanggal_str}")
                
            except Exception as e:
                st.error(f"Gagal menjalankan prosedur: {e}")

    # Tombol Kembali (Opsional jika tidak lewat sidebar)
    if st.button("Kembali ke Menu Utama"):
        st.session_state["current_page"] = "menu"
        st.rerun()
