import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Upload Data", layout="wide")

st.title("📤 Upload Data")

# 1. Inisialisasi Koneksi
target_schema = st.secrets.get("SUPABASE_SCHEMA", "project1") # Default ke project1
conn = st.connection("supabase", type=SupabaseConnection, schema=target_schema)

# 2. Ambil Daftar Tabel dari View 'v_table_list'
try:
    allowed_tables = ["disbursement","deposit","saldo_durian","settlement"]
    # Memastikan schema project1 terpanggil eksplisit
    view_data = conn.client.schema("project1").table("v_table_list").select("*").in_("table_name", allowed_tables).execute()
    
    list_tabel = [row['table_name'] for row in view_data.data]
    
    if not list_tabel:
        st.warning("View 'v_table_list' ditemukan tetapi tidak ada data tabel.")
        list_tabel = ["No Tables Found"]
except Exception as e:
    st.error(f"Gagal mengambil daftar tabel dari view: {e}")
    list_tabel = ["Error Loading View"]

# 3. Dropdown Dinamis
target_table = st.selectbox(
    "Pilih Tabel Tujuan:",
    list_tabel
)

# --- Proses Upload File ---
uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])

if uploaded_file and target_table not in ["Error Loading View", "No Tables Found"]:
    try:
        # Membaca data dari Excel
        df = pd.read_excel(uploaded_file)
        
        # --- NORMALISASI NAMA KOLOM ---
        # 1. str(col).strip(): Menghapus spasi di awal/akhir nama kolom
        # 2. .lower(): Mengubah ke huruf kecil
        # 3. .replace(' ', '_'): Mengganti spasi di tengah dengan underscore
        df.columns = [str(col).strip().lower().replace(' ', '_').replace("'","_") for col in df.columns]
        # ------------------------------

        st.subheader(f"Total: {len(df)} baris")
        # Menampilkan preview dengan nama kolom yang sudah dinormalisasi
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("Proses Upload"):
            import numpy as np
            
            # 1. Konversi dataframe ke list of records
            data_dict = df.to_dict(orient='records')
            
            # 2. Fungsi pembersihan rekursif (NaN, Inf, dan Timestamp)
            def clean_json_data(obj):
                if isinstance(obj, list):
                    return [clean_json_data(item) for item in obj]
                elif isinstance(obj, dict):
                    return {k: clean_json_data(v) for k, v in obj.items()}
                elif isinstance(obj, float):
                    if np.isnan(obj) or np.isinf(obj):
                        return None
                # --- TAMBAHAN UNTUK TIMESTAMP ---
                elif hasattr(obj, 'isoformat'): # Mengecek apakah objek adalah date/timestamp
                    return obj.isoformat()
                # --------------------------------
                return obj

            # Jalankan pembersihan
            cleaned_data = clean_json_data(data_dict)
            
            with st.spinner(f'Mengunggah {len(cleaned_data)} baris...'):
                try:
                    response = conn.client.schema("project1").table(target_table).insert(cleaned_data).execute()
                    if response:
                        st.success("Berhasil diunggah!")
                        st.balloons()
                except Exception as e:
                    st.error(f"Detail Error: {e}")
                    
    except Exception as e:
        st.error(f"File tidak terbaca: {e}")











