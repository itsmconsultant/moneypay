import streamlit as st
import pandas as pd
import numpy as np

def show_upload_dashboard(conn):

    st.title("📤 Upload Data")
    st.write("Pilih tabel tujuan untuk penyimpanan data dan excel sebagai sumber data.")
    st.divider()

    # Ambil daftar tabel
    try:
        allowed_tables = ["disbursement", "deposit", "saldo_durian", "settlement"]
        view_data = conn.client.schema("moneypay").table("v_table_list").select("*").in_("table_name", allowed_tables).execute()
        list_tabel = [row['table_name'] for row in view_data.data]
    except Exception as e:
        st.error(f"Gagal memuat tabel: {e}")
        list_tabel = []

    target_table = st.selectbox("Pilih Tabel Tujuan:", list_tabel)
    uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])

    if uploaded_file and target_table:
        try:
            df = pd.read_excel(uploaded_file)
            # Normalisasi kolom
            df.columns = [str(col).strip().lower().replace(' ', '_').replace("'", "_").replace("+", "_") for col in df.columns]
            
            st.subheader(f"Total: {len(df)} baris")
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("Proses Upload"):
                def clean_json_data(obj):
                    if isinstance(obj, list): return [clean_json_data(item) for item in obj]
                    elif isinstance(obj, dict): return {k: clean_json_data(v) for k, v in obj.items()}
                    elif isinstance(obj, float):
                        if np.isnan(obj) or np.isinf(obj): return None
                    elif hasattr(obj, 'isoformat'): return obj.isoformat()
                    return obj

                # Konversi ke dict
                raw_data = df.to_dict(orient='records')
                cleaned_data = clean_json_data(raw_data)
                
                # --- LOGIKA CHUNKING (PERBAIKAN) ---
                chunk_size = 1000  # Kirim per 500 baris agar tidak timeout
                total_chunks = (len(cleaned_data) // chunk_size) + (1 if len(cleaned_data) % chunk_size > 0 else 0)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                success_count = 0
                error_occurred = False

                with st.spinner('Sedang mengunggah data...'):
                    for i in range(0, len(cleaned_data), chunk_size):
                        chunk = cleaned_data[i:i + chunk_size]
                        current_chunk_num = (i // chunk_size) + 1
                        
                        try:
                            # Kirim potongan data
                            conn.client.schema("moneypay").table(target_table).insert(chunk).execute()
                            success_count += len(chunk)
                            
                            # Update progress bar
                            progress = current_chunk_num / total_chunks
                            progress_bar.progress(progress)
                            status_text.text(f"Mengunggah: {success_count} / {len(cleaned_data)} baris...")
                            
                        except Exception as e:
                            st.error(f"Gagal mengunggah potongan ke-{current_chunk_num}: {e}")
                            error_occurred = True
                            break # Hentikan jika ada error di tengah jalan
                
                if not error_occurred:
                    st.success(f"Berhasil! {success_count} baris data telah diunggah ke tabel '{target_table}'.")
                    st.balloons()
                # ----------------------------------
                
        except Exception as e:
            st.error(f"File rusak atau tidak terbaca: {e}")
