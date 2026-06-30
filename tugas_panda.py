import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("penjualan.csv")

print(df)
print("\n=== Produk ===")
print(df.describe())

print("\n=== Total ===")
df["total"] = df["jumlah"] * df["harga"]
print (df.groupby("produk")["total"].sum())

print("\n=== Produk terlaris ===")
print(df[df["jumlah"] == df["jumlah"].max()])

print("\n=== Bulanan dengan penjualan tertinggi ===")
print(df["bulan"].value_counts())

total_produk = df.groupby("produk")["total"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(total_produk.index, total_produk.values, color="#e94560")
plt.title("Total Penjualan Produk")
plt.xlabel("Produk")
plt.ylabel("Total Penjualan")
plt.show()