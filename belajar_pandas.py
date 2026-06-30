import matplotlib.pyplot as plt
import pandas as pd

data = {
    "nama": ["Hafizh", "Budi", "Siti", "Andi", "Rini"],
    "umur": [19, 20, 21, 22, 23],      
    "nilai": [100, 95, 85, 80, 75]    
}

df = pd.DataFrame(data)

print(df)
print("\n--- Info ---")
print(df.describe())

# filter data nilai diatas 80
print("\n--- Nilai di atas 80 ---")
print(df[df["nilai"] > 80])

# urutan berdasarkan nilai
print('\n--- Urutan berdasarkan nilai tertinggi ---')
print(df.sort_values("nilai", ascending=False))

# rata-rata nilai
print("\n--- rata-rata nilai ---")
print(df["nilai"].mean())



# bikin bar chart
plt.figure(figsize=(8, 5))
plt.bar(df["nama"], df["nilai"], color="#e94560")
plt.title("Nilai Siswa")
plt.xlabel("Nama")
plt.ylabel("Nilai")
plt.show()

# line chart
plt.figure(figsize=(8, 5))
plt.plot(df["nama"], df["nilai"], color="#e94560", marker="o", linewidth=2)
plt.title("Perkembangan nilai")
plt.xlabel("Nama")
plt.ylabel("NIlai")
plt.grid(True)
plt.show()

# pie chart
plt.figure(figsize=(6, 6))
plt.pie(df["nilai"], labels=df["nama"], autopct="%1.1f%%")
plt.title("Proporsi Nilai")
plt.show()