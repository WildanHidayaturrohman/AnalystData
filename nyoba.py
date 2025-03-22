import pandas as pd
import gdown

# Daftar file_id dan nama file output yang sesuai
file_info = {
    "189NMMz4eEcmX_e9h9SQ5Xip_PprYTX-S": "rfm_df.csv",
    "16Y2nmqQTDWBNTt0Bz2v1f9cwBJqqvpNb": "merged_4_df.csv",
    "1flbfOdBx26n-_fWeKINthyMTOqklGhAq": "grouped_product_category_review_score.csv",
    "1M5NnrGe7IoQsdqoSgMO7yiWmb8XBB2BP": "jumlah_pesanan_terlambat_per_state_df.csv",
    "1X8vO_kSKZQ6hxC42opmS_5bPOFhgxxmy": "grouped_customer_data.csv",
    "1wFkNsEgELsWItZZyeTvv1r3J3fvvVp78": "rata_rata_waktu_pengiriman_per_state_df.csv"
}

# Mengunduh file dengan nama yang sesuai
def download_files(file_info):
    for file_id, output_name in file_info.items():
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Mengunduh {output_name} dari {url}...")
        gdown.download(url, output_name, quiet=False)

download_files(file_info)
