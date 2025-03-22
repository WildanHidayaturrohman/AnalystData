import pandas as pd
import gdown

# Daftar file_id dan nama file output yang sesuai
file_info = {
    "189NMMz4eEcmX_e9h9SQ5Xip_PprYTX-S": "rfm_df.csv",
    "16Y2nmqQTDWBNTt0Bz2v1f9cwBJqqvpNb": "merged_4_df.csv",
    "1oImyQqC7mdkhHk7tvkcR7rsSIUchAZBN": "kategori_produk_terurut_english.csv",
    "1MbWlpyS1F0LNjbt0Ow051jipA6z5ckkK": "jumlah_pesanan_terlambat_per_state.csv",
    "144uxyKd_TkjVSIwi2PccAsOvMY0qR0UA": "customer_kategori_sorted.csv",
    "1JfFEIflZuLk8YpVYtSZWIQSiaqTfJvtO": "rata_rata_waktu_pengiriman_per_state.csv"
}

# Mengunduh file dengan nama yang sesuai
def download_files(file_info):
    for file_id, output_name in file_info.items():
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Mengunduh {output_name} dari {url}...")
        gdown.download(url, output_name, quiet=False)

download_files(file_info)
