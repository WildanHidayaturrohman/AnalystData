# Membaca file CSV ke dalam dataframe
rfm_df = pd.read_csv("output1.csv")
merged_4_df = pd.read_csv("output2.csv")
kategori_produk_terurut_english = pd.read_csv("output3.csv")
jumlah_pesanan_terlambat_per_state = pd.read_csv("output4.csv")
customer_kategori_sorted = pd.read_csv("output5.csv")
rata_rata_waktu_pengiriman_per_state = pd.read_csv("output6.csv")

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
st.sidebar.header("Filters")

# Filter untuk pertanyaan 1 dan 2
date_range = st.sidebar.date_input(
    "Select Date Range (Last Year Before 2018-10-17 17:30:18):",
    [pd.to_datetime("2017-10-17"), pd.to_datetime("2018-10-17")]
)

# Filter untuk pertanyaan 3
top_bottom_filter = st.sidebar.radio("Question 3 Filter:", ["Top 10", "Bottom 10"])


# pertanyaan 1
st.header("Customer Segmentation")

# Visualisasi kategori pelanggan
plt.figure(figsize=(8, 6))

sns.countplot(x="Kategori Pelanggan", data=customer_kategori_sorted)
plt.title('Kategori Pelanggan dalam Setahun Terakhir')
plt.xlabel('Kategori Pelanggan')
plt.ylabel('Jumlah Pelanggan')
st.pyplot(plt)

# pertanyaan 2
st.header("Shipping Time Analysis")

plt.figure(figsize=(12, 6))
sns.barplot(
    x="geolocation_state",
    y="waktu_pengiriman",
    data=rata_rata_waktu_pengiriman_per_state
)
plt.title('Rata-rata Waktu Pengiriman per State')
plt.xlabel('State')
plt.ylabel('Rata-rata Waktu Pengiriman (hari)')
plt.xticks(rotation=90)
st.pyplot(plt)

# pertanyaan 3
st.header("Product Category Performance")
if top_bottom_filter == "Top 10":
    data_to_plot = kategori_produk_terurut_english.head(10)
else:
    data_to_plot = kategori_produk_terurut_english.tail(10)

plt.figure(figsize=(12, 6))
sns.barplot(x=data_to_plot.index, y=data_to_plot.values)
plt.title(f"Kategori Produk dengan Rating Ulasan {top_bottom_filter}")
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-rata Rating Ulasan')
plt.xticks(rotation=90)
st.pyplot(plt)

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
