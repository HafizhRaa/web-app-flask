import pandas as pd
import matplotlib.pyplot as plt

# read file csv
df = pd.read_csv("data_siswa.csv")

print(df)
print("\n--- Statistik ---")
print(df.describe()) 

# rata-rata nilai per kota
print("\n--- Rata-rata nilai per kota ---")
print(df.groupby ("kota")["nilai"].mean().sort_values(ascending=False))

# siapa yang nilai tertinggi
print("\n--- Nilai tertinggi ---")
print(df[df["nilai"] == df["nilai"].max()])

# berapa orang per kota
print("\n--- jumlah siswa per kota ---")
print(df["kota"].value_counts())

# grafik rata-rata nilai orang per kota
rata_kota = df.groupby("kota")["nilai"].mean().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
plt.bar(rata_kota.index, rata_kota.values, color="#e94560")
plt.title("Rata-rata Nilai perkota")
plt.xlabel("Kota")
plt.ylabel("Raata-rata nilai")
plt.show()
