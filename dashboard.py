# Membaca file CSV ke dalam dataframe
seller_df = pd.read_csv("output1.csv")
product_df = pd.read_csv("output2.csv")
translate_df = pd.read_csv("output3.csv")
orders_df = pd.read_csv("output4.csv")
review_df = pd.read_csv("output5.csv")
payment_df = pd.read_csv("output6.csv")
item_df = pd.read_csv("output7.csv")
geolocation_df = pd.read_csv("output8.csv")
customers_df = pd.read_csv("output9.csv")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# ~~~~~~~~~~~~~~~~~ Awal cleaning Data ~~~~~~~~~~~~~~
datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]

for column in datetime_columns:
  orders_df[column] = pd.to_datetime(orders_df[column])

# mean untuk setiap selisih waktu
mean_to_approved_at = (orders_df['order_approved_at'] - orders_df['order_purchase_timestamp']).dt.total_seconds().mean()
mean_to_carrier_date = (orders_df['order_delivered_carrier_date'] - orders_df['order_approved_at']).dt.total_seconds().mean()
mean_to_delivered_customer_date = (orders_df['order_delivered_customer_date'] - orders_df['order_estimated_delivery_date']).dt.total_seconds().mean()

# Mengisi nilai yang kosong menggunakan fillna()
orders_df['order_approved_at'] = orders_df['order_approved_at'].fillna(orders_df['order_purchase_timestamp'] + pd.Timedelta(seconds=mean_to_approved_at))
orders_df['order_delivered_carrier_date'] = orders_df['order_delivered_carrier_date'].fillna(orders_df['order_approved_at'] + pd.Timedelta(seconds=mean_to_carrier_date))
orders_df['order_delivered_customer_date'] = orders_df['order_delivered_customer_date'].fillna(orders_df['order_estimated_delivery_date'] + pd.Timedelta(seconds=mean_to_delivered_customer_date))

kondisi_1 = payment_df['payment_installments'] == 0
kondisi_2 = payment_df['payment_value'] == 0

payment_df.drop(payment_df[kondisi_1].index, inplace=True)
payment_df.drop(payment_df[kondisi_2].index, inplace=True)

item_df['shipping_limit_date'] = pd.to_datetime(item_df['shipping_limit_date'])

# ~~~~~~~~~~~~~~~~~ Akhir cleaning Data ~~~~~~~~~~~~~~



# ~~~~~~~~~~~~~~~~~ Awal helper function yang dibutuhkan untuk menyiapkan berbagai dataframe ~~~~~~~~~~~~~~
# Tentukan batas bawah (1 tahun sebelum 2018-10-17 17:30:18)
batas_bawah = pd.Timestamp('2018-10-17 17:30:18') - pd.DateOffset(years=1)

# Filter data dalam setahun terakhir
orders_setahun_terakhir = orders_df[orders_df['order_purchase_timestamp'] >= batas_bawah]

# Hitung jumlah order per customer
jumlah_order_per_customer = orders_setahun_terakhir.groupby('customer_id')['order_id'].count()

# Buat DataFrame kategori pelanggan
customer_kategori = pd.DataFrame({'Jumlah Order': jumlah_order_per_customer})

# Kategorikan customer berdasarkan jumlah order
customer_kategori['Kategori Pelanggan'] = np.where(customer_kategori['Jumlah Order'] == 1, 'Customer Baru', 'Customer Kembali')

# Hitung jumlah pelanggan berdasarkan kategori
kategori_customer_setahunTerakhir = customer_kategori.groupby('Kategori Pelanggan').size().reset_index(name='Jumlah Pelanggan')

# Filter data dalam 1 tahun terakhir
batas_bawah_1tahun = pd.Timestamp('2018-10-17 17:30:18') - pd.DateOffset(years=1)
orders_1tahun_terakhir = orders_df[orders_df['order_purchase_timestamp'] >= batas_bawah_1tahun]

# Gabungkan data orders dan customer
merged_df = pd.merge(orders_1tahun_terakhir,
                     customers_df,
                     on='customer_id',
                     how='left')
merged_df['customer_zip_code_prefix'] = merged_df['customer_zip_code_prefix'].astype(int)
geolocation_df['geolocation_zip_code_prefix'] = geolocation_df['geolocation_zip_code_prefix'].astype(int)

# Gabungkan DataFrame
merged_df = pd.merge(merged_df,
                     geolocation_df,
                     left_on='customer_zip_code_prefix',
                     right_on='geolocation_zip_code_prefix',
                     how='left')
# Hitung selisih waktu pengiriman
merged_df['waktu_pengiriman'] = (merged_df['order_delivered_customer_date'] - merged_df['order_purchase_timestamp']).dt.days

# Hitung rata-rata waktu pengiriman
rata_rata_waktu_pengiriman = merged_df['waktu_pengiriman'].mean()

# Analisis keterlambatan berdasarkan lokasi geografis
merged_df['terlambat'] = merged_df['order_delivered_customer_date'] > merged_df['order_estimated_delivery_date']

# Rata-rata waktu pengiriman per state
rata_rata_waktu_pengiriman_per_state = merged_df.groupby('geolocation_state')['waktu_pengiriman'].mean()
# Jumlah pesanan yang terlambat per state
jumlah_pesanan_terlambat_per_state = merged_df.groupby('geolocation_state')['terlambat'].sum()

# Gabungkan DataFrame yang dibutuhkan untuk menjawab pertanyaan 3
merged_2_df = pd.merge(item_df,
                      product_df,
                      on='product_id',
                      how='left')
merged_2_df = pd.merge(merged_2_df,
                      review_df,
                      on='order_id',
                      how='left')

# Filter data dalam 1 tahun terakhir
batas_bawah = pd.Timestamp('2018-10-17 17:30:18') - pd.DateOffset(years=1)
merged_2_df_setahun_terakhir = merged_2_df[merged_2_df['shipping_limit_date'] >= batas_bawah]

# Hitung rata-rata rating ulasan per kategori produk
rata_rata_rating_per_kategori = merged_2_df_setahun_terakhir.groupby('product_category_name')['review_score'].mean()

# Urutkan kategori produk berdasarkan rata-rata rating ulasan dari tertinggi ke terendah
kategori_produk_terurut = rata_rata_rating_per_kategori.sort_values(ascending=False)

# Gabungkan merged_2_df_setahun_terakhir dengan translate_df
merged_3_df = pd.merge(merged_2_df_setahun_terakhir,
                      translate_df,
                      on='product_category_name',
                      how='left')

# Hitung rata-rata rating ulasan per kategori produk (menggunakan product_category_name_english)
rata_rata_rating_per_kategori_english = merged_3_df.groupby('product_category_name_english')['review_score'].mean()

# Urutkan kategori produk berdasarkan rata-rata rating ulasan dari tertinggi ke terendah
kategori_produk_terurut_english = rata_rata_rating_per_kategori_english.sort_values(ascending=False)

# Gabungkan DataFrame yang dibutuhkan
merged_4_df = pd.merge(orders_df,
                       review_df,
                       on='order_id',
                       how='left')

# Hitung selisih waktu pengiriman
merged_4_df['waktu_pengiriman'] = (merged_4_df['order_delivered_customer_date'] - merged_4_df['order_purchase_timestamp']).dt.days

# Analisis korelasi antara waktu pengiriman dan kepuasan pelanggan
correlation = merged_4_df['waktu_pengiriman'].corr(merged_4_df['review_score'])

# Menggabungkan data orders dan payment untuk mendapatkan total revenue per customer
rfm_df = pd.merge(orders_df, payment_df, on='order_id', how='inner')

# Mengambil tanggal terbaru dalam dataset
latest_date = rfm_df['order_purchase_timestamp'].max()

# Menghitung Recency (selisih hari dari transaksi terakhir)
rfm_df['Recency'] = (latest_date - rfm_df['order_purchase_timestamp']).dt.days

# Menghitung Frequency (jumlah transaksi per customer)
frequency_df = rfm_df.groupby('customer_id')['order_id'].nunique().reset_index(name='Frequency')

# Menghitung Monetary (total revenue per customer)
monetary_df = rfm_df.groupby('customer_id')['payment_value'].sum().reset_index(name='Monetary')

# Mencari Recency terkecil per customer (hari sejak transaksi terakhir)
recency_df = rfm_df.groupby('customer_id')['Recency'].min().reset_index(name='Recency')

# Menggabungkan Recency, Frequency, dan Monetary
rfm_df = pd.merge(recency_df, frequency_df, on='customer_id', how='inner')
rfm_df = pd.merge(rfm_df, monetary_df, on='customer_id', how='inner')

# Menghapus duplikasi
rfm_df = rfm_df.drop_duplicates(subset=['customer_id'])

# ~~~~~~~~~~~~~~~~~ Akhir helper function yang dibutuhkan untuk menyiapkan berbagai dataframe ~~~~~~~~~~~~~~

# URL Google Drive untuk langsung mendownload
image_url = "https://drive.google.com/uc?id=1sJ3cLxlY0ZXcx9cbKyoFx0WTrxV8NgMr"
st.image(image_url)


# plot pertanyaan 1
st.header('E-Commerce Collection Dashboard')
st.subheader('Kategori Pelanggan dalam Setahun Terakhir')

plt.figure(figsize=(8, 6))
sns.barplot(x='Kategori Pelanggan', y='Jumlah Pelanggan', data=kategori_customer_setahunTerakhir)
plt.title('Kategori Pelanggan dalam Setahun Terakhir')
plt.xlabel('Kategori Pelanggan')
plt.ylabel('Jumlah Pelanggan')

st.pyplot(plt)


# plot pertanyaan 2
st.subheader("Rata-rata Waktu Pengiriman")

# Menentukan warna berdasarkan nilai rata-rata waktu pengiriman
colors = ['chartreuse' if val == min(rata_rata_waktu_pengiriman_per_state.values)
          else 'red' if val == max(rata_rata_waktu_pengiriman_per_state.values)
          else 'steelblue' for val in rata_rata_waktu_pengiriman_per_state.values]

# Visualisasi Rata-rata Waktu Pengiriman per State
plt.figure(figsize=(12, 6))
sns.barplot(x=rata_rata_waktu_pengiriman_per_state.index,
            y=rata_rata_waktu_pengiriman_per_state.values,
            palette=colors)
plt.title('Rata-rata Waktu Pengiriman per State')
plt.xlabel('State')
plt.ylabel('Rata-rata Waktu Pengiriman (hari)')
plt.xticks(rotation=90)
st.pyplot(plt)

st.subheader("Jumlah Pesanan Terlambat")

# Menentukan warna berdasarkan jumlah pesanan terlambat
colors_terlambat = ['chartreuse' if val == min(jumlah_pesanan_terlambat_per_state.values)
                    else 'red' if val == max(jumlah_pesanan_terlambat_per_state.values)
                    else 'steelblue' for val in jumlah_pesanan_terlambat_per_state.values]

# Visualisasi Jumlah Pesanan Terlambat per State
plt.figure(figsize=(12, 6))
sns.barplot(x=jumlah_pesanan_terlambat_per_state.index,
            y=jumlah_pesanan_terlambat_per_state.values,
            palette=colors_terlambat)
plt.title('Jumlah Pesanan Terlambat per State')
plt.xlabel('State')
plt.ylabel('Jumlah Pesanan Terlambat')
plt.xticks(rotation=90)
st.pyplot(plt)

# plot pertanyaan 3
st.subheader("Kategori Produk Terurut Berdasarkan Rata-rata Rating")

# Ambil 10 tertinggi dan 10 terendah
top_10 = kategori_produk_terurut_english.head(10)
bottom_10 = kategori_produk_terurut_english.tail(10)

# Tentukan rating tertinggi dan terendah di antara top_10 dan bottom_10
max_top = top_10.max()  # Rating tertinggi di top 10
min_bottom = bottom_10.min()  # Rating terendah di bottom 10

# Tentukan warna untuk top 10
colors_top = ['chartreuse' if val == max_top
              else 'steelblue' for val in top_10]

# Tentukan warna untuk bottom 10
colors_bottom = ['red' if val == min_bottom
                 else 'steelblue' for val in bottom_10]

# Visualisasi Kategori Produk dengan Rating Ulasan Tertinggi (Top 10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10.index, y=top_10.values, palette=colors_top)
plt.title('Kategori Produk dengan Rating Ulasan Tertinggi (Top 10)')
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-rata Rating Ulasan')
plt.xticks(rotation=90)
st.pyplot(plt)


# Visualisasi Kategori Produk dengan Rating Ulasan Terendah (Bottom 10)
plt.figure(figsize=(12, 6))
sns.barplot(x=bottom_10.index, y=bottom_10.values, palette=colors_bottom)
plt.title('Kategori Produk dengan Rating Ulasan Terendah (Bottom 10)')
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-rata Rating Ulasan')
plt.xticks(rotation=90)
st.pyplot(plt)



# plot pertanyaan 4
st.subheader("Korelasi waktu pengiriman dan kepuasan pelanggan")

# Visualisasi korelasi antara waktu pengiriman dan kepuasan pelanggan
plt.figure(figsize=(8, 6))
sns.heatmap([[correlation]], annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Korelasi antara Waktu Pengiriman dan Kepuasan Pelanggan')
plt.xlabel('Waktu Pengiriman')
plt.ylabel('Kepuasan Pelanggan')
st.pyplot(plt)


# ### Pertanyaan 4:
plt.figure(figsize=(8, 6))
sns.scatterplot(x='waktu_pengiriman', y='review_score', data=merged_4_df)
plt.title('Hubungan antara Waktu Pengiriman dan Kepuasan Pelanggan')
plt.xlabel('Waktu Pengiriman (hari)')
plt.ylabel('Rating Ulasan')
st.pyplot(plt)


# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(x="Recency", y="customer_id", data=rfm_df.sort_values(by="Recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(x="Frequency", y="customer_id", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(x="Monetary", y="customer_id", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)

st.pyplot(plt)

st.caption('Copyright © Dicoding 2023')
