import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import json

# Load and preprocess
file_path = "output1.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Clean price column
def clean_price(price_str):
    if not price_str or price_str.strip() == "₹ 0":
        return 0
    price_str = re.sub(r"[^\d]", "", price_str)
    return int(price_str) if price_str else 0

df["price_num"] = df["price"].apply(clean_price)

# Extract product type keywords
def extract_product_type(name):
    name = name.lower()
    words = re.findall(r"[a-zA-Z]+", name)
    stopwords = {"for", "industrial", "and", "with", "unit"}
    filtered = [w for w in words if w not in stopwords]
    return " ".join(filtered[:2]) if filtered else name

df["product_type"] = df["name"].apply(extract_product_type)

# Summary statistics
summary_stats = {
    "total_records": len(df),
    "unique_companies": df["company"].nunique(),
    "missing_prices": (df["price_num"] == 0).sum(),
    "avg_price": df["price_num"].mean(),
    "median_price": df["price_num"].median(),
    "max_price": df["price_num"].max(),
    "min_price": df["price_num"].min(),
}
print("Summary Stats:\n", summary_stats)

# Price distribution
plt.figure(figsize=(12, 6))
sns.histplot(df[df["price_num"] > 0]["price_num"], bins=20, kde=False, color="skyblue")
plt.title("Price Distribution of Industrial Machines", fontsize=14, fontweight="bold")
plt.xlabel("Price (₹)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.ticklabel_format(style="plain", axis="x")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("price_distribution.png", dpi=300)

# Top product types
top_products = df["product_type"].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_products.index, y=top_products.values, palette="Blues_r")
plt.title("Top 10 Product Types by Frequency", fontsize=14, fontweight="bold")
plt.ylabel("Count", fontsize=12)
plt.xlabel("Product Type", fontsize=12)
plt.xticks(rotation=45, ha="right")  # rotate & align labels
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("top_products_frequency.png", dpi=300)
# Group prices by product type 
grouped_prices = ( df.groupby("product_type")["price_num"] .agg(["count", "mean", "median", "max", "min"]) .sort_values("mean", ascending=False) )
print("\nPrices by Product Type:\n", grouped_prices)  
grouped_prices["mean"].plot(kind="bar", color="coral")

plt.figure(figsize=(14, 7))
sns.barplot(x=grouped_prices.index[:10], y=grouped_prices["mean"][:10], palette="OrRd_r")
plt.title("Average Price by Product Type (Top 10)", fontsize=14, fontweight="bold")
plt.ylabel("Average Price (₹)", fontsize=12)
plt.xlabel("Product Type", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.ticklabel_format(style="plain", axis="y")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("avg_price.png", dpi=300)
