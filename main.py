import pandas as pd
import matplotlib.pyplot as plt

files = ["data1.csv", "data2.csv", "data3.csv"]

dfs = [pd.read_csv(f) for f in files]
merged_df = pd.concat(dfs, ignore_index = True)

remove = ["Bhutan", "Maldives"]
merged_df = merged_df[~merged_df["Countries"].isin(remove)]

merged_df.to_csv("merged_data.csv", index = False)



important_cols = ["Commodities",
    "Countries",
    "Time",
    "Customs Value (Gen) ($US) (Default Member)",
    "Customs Value (Cons) ($US)"]
merged_df = merged_df[important_cols]

merged_df.to_csv("merged_filtered.csv", index=False)

print(merged_df.columns)
commod_list = merged_df["Commodities"].unique().tolist()
print(commod_list)
print(len(commod_list))

def classify_commodity(commodity):
    if "Ore" in commodity or "Concentrates" in commodity:
        return "Ore/Raw"
    elif "Oxide" in commodity or "Compound" in commodity:
        return "Compound"
    elif "Article" in commodity or "And Articles" in commodity:
        return "Refined/Articles"
    elif "Battery" in commodity or "Magnet" in commodity:
        return "Advanced Product"
    else:
        return "Other"

merged_df["CategoryType"] = merged_df["Commodities"].apply(classify_commodity)

print(merged_df.isna().sum())

print(merged_df["Countries"].unique())

organizations = ["Asia - South", "APEC - Asia Pacific Economic Co-operation", "ASEAN - Association of Southeast Asian Nations"]
filtered_regions_df = merged_df[merged_df["Countries"].isin(organizations)]
filtered_regions_df.to_csv("filtered_regions.csv", index = False)


southeast = ["Singapore", "Indonesia", "Vietnam", "Philippines", "Brunei", "Malaysia", "Thailand", "Cambodia", "Laos", "Burma"]
southeast_countries_df = merged_df[merged_df["Countries"].isin(southeast)]
southeast_countries_df.to_csv("southeast_countries.csv", index = False)

east = ["Taiwan", "Korea, South", "Hong Kong", "Japan", "Macau", "Mongolia"]
east_countries_df = merged_df[merged_df["Countries"].isin(east)]
east_countries_df.to_csv("east_countries.csv", index = False)

# Total imports per year
imports_by_year = merged_df.groupby("Time")["Customs Value (Gen) ($US) (Default Member)"].sum()

# Total imports by commodity (top 10)
imports_by_commodity = merged_df.groupby("Commodities")["Customs Value (Gen) ($US) (Default Member)"].sum().sort_values(ascending=False).head(10)

# Imports by category type
imports_by_category = merged_df.groupby("CategoryType")["Customs Value (Gen) ($US) (Default Member)"].sum()


# Trend over time
imports_by_year.plot(kind="line", title="Total Imports Over Time", ylabel="Value ($US)")
plt.show()

# Top commodities
imports_by_commodity.plot(kind="barh", title="Top 10 Commodities by Import Value", xlabel="Value ($US)")
plt.show()

# By category type
imports_by_category.plot(kind="pie", autopct="%1.1f%%", title="Import Breakdown by Category Type")
plt.show()