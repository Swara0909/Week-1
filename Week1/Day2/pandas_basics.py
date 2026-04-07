import pandas as pd

# 1. Create Series
s = pd.Series([10, 20, 30, 40])
print("Series:\n", s)

# 2. Create DataFrame
data = {
    "Name": ["Swara", "Muskan", "Khusho"],
    "Marks": [90, 85, 88],
    "City": ["Surat", "Mumbai", "Delhi"]
}

df = pd.DataFrame(data)
print("DataFrame:\n", df)

# 3. Basic Info
print("Head:\n", df.head())
print("Info:\n")
df.info()

# 4. Select Columns
print("Names:\n", df["Name"])

# 5. Filter Data
print("Marks > 85:\n", df[df["Marks"] > 85])

# 6. Add New Column
df["Grade"] = ["A", "B", "A"]
print("Updated DF:\n", df)

# 7. Drop Column
df = df.drop("City", axis=1)
print("After Drop:\n", df)

# 8. Statistics
print("Mean Marks:", df["Marks"].mean())
print("Max Marks:", df["Marks"].max())

# 9. Sort Data
print("Sorted:\n", df.sort_values("Marks"))

# 10. Save to CSV
df.to_csv("students.csv", index=False)

print("\nFile saved as students.csv")