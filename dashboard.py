# Membaca file CSV ke dalam dataframe
rfm_df = pd.read_csv("rfm_df.csv")
merged_4_df = pd.read_csv("merged_4_df.csv")
grouped_product_category_review_score = pd.read_csv("grouped_product_category_review_score.csv")
jumlah_pesanan_terlambat_per_state_df = pd.read_csv("jumlah_pesanan_terlambat_per_state_df.csv")
grouped_customer_data = pd.read_csv("grouped_customer_data.csv")
rata_rata_waktu_pengiriman_per_state_df = pd.read_csv("rata_rata_waktu_pengiriman_per_state_df.csv")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Judul
st.title("E-commerce Dashboard")

# Sidebar untuk filter
st.sidebar.title("Filters")

# Filter untuk pertanyaan 1 and 2 (date)
date_filter_1_2 = st.sidebar.date_input("Pilih Tanggal (untuk Pertanyaan 1 dan 2)", value=pd.to_datetime('2018-10-17'))
# Note: You'll need to adjust the filtering logic in your original code based on the 'order_purchase_timestamp' column

# Filter untuk pertanyaan 3 (top/bottom rating)
rating_filter_type = st.sidebar.radio("Pilih Filter Rating (untuk Pertanyaan 3)", ("Top 10", "Bottom 10"))

# Judul visdat
st.title("Visualisasi Data")

# Pertanyaan 1
st.header("Pertanyaan 1: Kategori Pelanggan dalam Setahun Terakhir")

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='Kategori Pelanggan', y='Count', data=grouped_customer_data, ax=ax)  # Replace with your data
plt.title('Kategori Pelanggan dalam Setahun Terakhir')
plt.xlabel('Kategori Pelanggan')
plt.ylabel('Jumlah Pelanggan')
st.pyplot(fig)

# Pertanyaan 2
st.header("Pertanyaan 2: Rata-rata Waktu Pengiriman dan Jumlah Pesanan Terlambat")
# Display 'rata_rata_waktu_pengiriman_per_state_df'
st.subheader("Rata-rata Waktu Pengiriman per State")
st.dataframe(rata_rata_waktu_pengiriman_per_state_df)

# Display 'jumlah_pesanan_terlambat_per_state_df'
st.subheader("Jumlah Pesanan Terlambat per State")
st.dataframe(jumlah_pesanan_terlambat_per_state_df)

# Visualisasi Rata-rata Waktu Pengiriman per State
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='geolocation_state', y='rata_rata_waktu_pengiriman', data=rata_rata_waktu_pengiriman_per_state_df, ax=ax)
plt.title('Rata-rata Waktu Pengiriman per State')
plt.xlabel('State')
plt.ylabel('Rata-rata Waktu Pengiriman (hari)')
plt.xticks(rotation=90)
st.pyplot(fig)

# Visualisasi Jumlah Pesanan Terlambat per State
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='geolocation_state', y='jumlah_pesanan_terlambat', data=jumlah_pesanan_terlambat_per_state_df, ax=ax)
plt.title('Jumlah Pesanan Terlambat per State')
plt.xlabel('State')
plt.ylabel('Jumlah Pesanan Terlambat')
plt.xticks(rotation=90)
st.pyplot(fig)


# Pertanyaan 3
st.header("Pertanyaan 3: Rating Ulasan Produk")

if rating_filter_type == "Top 10":
    top_10_categories = grouped_product_category_review_score.groupby('product_category_name_english')['review_score'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_10_categories.index, y=top_10_categories.values, ax=ax)
    plt.title('Kategori Produk dengan Rating Ulasan Tertinggi (Top 10)')
    plt.xlabel('Kategori Produk')
    plt.ylabel('Rata-rata Rating Ulasan')
    plt.xticks(rotation=90)
    st.pyplot(fig)
else:
    bottom_10_categories = grouped_product_category_review_score.groupby('product_category_name_english')['review_score'].mean().sort_values(ascending=True).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=bottom_10_categories.index, y=bottom_10_categories.values, ax=ax)
    plt.title('Kategori Produk dengan Rating Ulasan Terendah (Bottom 10)')
    plt.xlabel('Kategori Produk')
    plt.ylabel('Rata-rata Rating Ulasan')
    plt.xticks(rotation=90)
    st.pyplot(fig)

# pertanyaan 4
st.header("Relationship between Shipping Time and Customer Satisfaction")
correlation = merged_4_df["waktu_pengiriman"].corr(merged_4_df["review_score"])
st.write(f"Korelasi antara waktu pengiriman dan kepuasan pelanggan: {correlation:.2f}")

plt.figure(figsize=(8, 6))
sns.scatterplot(x="waktu_pengiriman", y="review_score", data=merged_4_df)
plt.title('Hubungan antara Waktu Pengiriman dan Kepuasan Pelanggan')
plt.xlabel('Waktu Pengiriman (hari)')
plt.ylabel('Rating Ulasan')
st.pyplot(plt)

# RFM analysis
st.header("RFM Analysis (Best Customer)")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
sns.barplot(
    x="Recency",
    y="customer_id",
    data=rfm_df.sort_values(by="Recency", ascending=True).head(5),
    palette=colors,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis="x", labelsize=15)

sns.barplot(
    x="Frequency",
    y="customer_id",
    data=rfm_df.sort_values(by="Frequency", ascending=False).head(5),
    palette=colors,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis="x", labelsize=15)

sns.barplot(
    x="Monetary",
    y="customer_id",
    data=rfm_df.sort_values(by="Monetary", ascending=False).head(5),
    palette=colors,
    ax=ax[2]
)
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis="x", labelsize=15)

plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)
st.pyplot(plt)
