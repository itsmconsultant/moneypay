import streamlit as st
import pandas as pd
import numpy as np

def show_upload_dashboard(conn):
    st.title("📤 Upload Data")
    st.write("Pilih tabel tujuan untuk penyimpanan data dan excel sebagai sumber data.")
    st.divider()

    # 1. Ambil daftar tabel dan kolom tanggal dari mapping table
    try:
        # Mapping table di schema moneypay dengan nama 'mapping_kolom_delete'
        mapping_data = conn.client.schema("moneypay").table("mapping_kolom_delete").select("*").execute()
        mapping_df = pd.DataFrame(mapping_data.data)
        list_tabel = mapping_df['table_name'].tolist()
    except Exception as e:
        st.error(f"Gagal memuat mapping tabel: {e}")
        list_tabel = []

    target_table = st.selectbox("Pilih Tabel Tujuan:", list_tabel)
    uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])

    if uploaded_file and target_table:
        try:
            df = pd.read_excel(uploaded_file)
            # Normalisasi kolom excel
            df.columns = [str(col).strip().lower().replace(' ', '_').replace("'", "_").replace("+", "_") for col in df.columns]
            
            # Ambil nama kolom tanggal target dari mapping
            date_col_target = mapping_df[mapping_df['table_name'] == target_table]['column_name'].values[0]
            
            if date_col_target not in df.columns:
                st.error(f"Kolom '{date_col_target}' tidak ditemukan di file Excel Anda.")
                return

            st.subheader(f"Total : {len(df)} baris")
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("Unggah Data"):
                # --- LOGIKA TANGGAL (FIX: DATE ONLY) ---
                # Mengonversi kolom ke datetime lalu ambil hanya porsi date (YYYY-MM-DD)
                df[date_col_target] = pd.to_datetime(df[date_col_target]).dt.date
                
                # Mengambil tanggal unik dan mengonversinya ke string ISO format
                distinct_dates = [d.isoformat() for d in df[date_col_target].unique()]

                with st.spinner('Proses pengunggahan...'):
                    try:
                        # STEP 3: Delete data berdasarkan list tanggal unik (YYYY-MM-DD)
                        conn.client.schema("moneypay").table(target_table).delete().in_(date_col_target, distinct_dates).execute()
                        
                        # STEP 4: Insert data baru dengan Chunking
                        def clean_json_data(obj):
                            if isinstance(obj, list): return [clean_json_data(item) for item in obj]
                            elif isinstance(obj, dict): return {k: clean_json_data(v) for k, v in obj.items()}
                            elif isinstance(obj, float):
                                if np.isnan(obj) or np.isinf(obj): return None
                            elif hasattr(obj, 'isoformat'): return obj.isoformat()
                            return obj

                        cleaned_data = clean_json_data(df.to_dict(orient='records'))
                        
                        CHUNK_SIZE = 1000
                        total_rows = len(cleaned_data)
                        success_count = 0
                        
                        # Progress visual
                        pbar = st.progress(0)
                        
                        for i in range(0, total_rows, CHUNK_SIZE):
                            chunk = cleaned_data[i:i + CHUNK_SIZE]
                            conn.client.schema("moneypay").table(target_table).insert(chunk).execute()
                            success_count += len(chunk)
                            pbar.progress(success_count / total_rows)
                        
                        st.success(f"Berhasil! Data pada tanggal {', '.join(distinct_dates)} telah diupload.")
                        st.balloons()

                    except Exception as e:
                        st.error(f"Proses gagal di database: {e}")
                        
        except Exception as e:
            st.error(f"Error pembacaan file: {e}")
