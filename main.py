import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

files = ["data1.csv", "data2.csv", "data3.csv"]

dfs = [pd.read_csv(f) for f in files]
merged_df = pd.concat(dfs, ignore_index = True)

remove = ["Bhutan", "Maldives","ASEAN - Association of Southeast Asian Nations","APEC - Asia Pacific Economic Co-operation","Asia - South"]
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

merged_df["Commodities"] = merged_df["Commodities"].str.strip()
commod_list = merged_df["Commodities"].unique().tolist()
print(commod_list)
print(len(commod_list))

merged_df["HS_Code"] = merged_df["Commodities"].str.split().str[0]
merged_df["HS_Code"] = merged_df["HS_Code"].astype(str)

# Complete commodity → critical mineral mapping
critical_mineral_map = {
    "74 Copper And Articles Thereof": "Copper",
    "76 Aluminum And Articles Thereof": "Aluminum",
    "75 Nickel And Articles Thereof": "Nickel",
    "80 Tin And Articles Thereof": "Tin",
    "8108 Titanium & Articles Thereof, Includ Waste & Scrap": "Titanium",
    "7226 Fl-rl Alloy Steel Nesoi Un 600mm Wide": "Alloy Steel",
    "8112 Beryllium,chromium,hafnium,rhenium Etc & Articles": "Beryllium/Chromium/Hafnium/Rhenium",
    "3910 Silicones, In Primary Forms": "Silicon",
    "3801 Artificial Graphite; Collodial Graphite & Prep Etc": "Graphite",
    "2504 Natural Graphite": "Graphite",
    "8111 Manganese And Artcles Thereof, Inc Waste And Scrap": "Manganese",
    "7225 Fl-rl Alloy Steel Nesoi Nun 600mm Wide": "Alloy Steel",
    "2846 Rare-earth Metal Compounds Of Yttrium Or Scandium": "Rare Earth Elements",
    "7110 Platinum, Unwrought, Semimfr Forms Or In Powder Fm": "Platinum Group Metals",
    "8110 Antimony And Artcls Throf Incl Waste And Scrap": "Antimony",
    "8105 Cobalt Mattes Etc, Cobalt & Art, Inc Waste & Scrap": "Cobalt",
    "2801 Fluorine, Chlorine, Bromine & Iodine": "Fluorine",
    "2614 Titanium Ores And Concentrates": "Titanium",
    "2820 Manganese Oxides": "Manganese",
    "2604 Nickel Ores And Concentrates": "Nickel",
    "2603 Copper Ores And Concentrates": "Copper",
    "2605 Cobalt Ores And Concentrates": "Cobalt",
    "2602 Manganese Ores A Concntrts Inc Ferr Mangn Iron Ore": "Manganese",
    "2606 Aluminum Ores And Concentrates": "Aluminum",
    "2609 Tin Ores And Concentrates": "Tin",
    "282520 Lithium Oxide And Hydroxide": "Lithium",
    "282540 Nickel Oxides And Hydroxides": "Nickel",
    "282550 Copper Oxides And Hydroxides": "Copper",
    "282580 Antimony Oxides": "Antimony",
    "711041 Iridium, Osmium And Ruthenium, Unwrought Or Powder": "Platinum Group Metals",
    "711049 Iridium, Osmium And Ruthenium, Semimanufactured": "Platinum Group Metals",
    "850511 Permanent Magnets Made Of Metal": "Electric Steel",
    "850650 Primary Cells And Batteries, Lithium": "Lithium",
    "2615906090 Vanadium Ores And Concentrates (kg)": "Vanadium"
}

# Add the new column by mapping directly
merged_df["critical_mineral"] = merged_df["Commodities"].map(critical_mineral_map)

# If any commodity wasn't found (shouldn't happen here), label it "Other"
merged_df["critical_mineral"] = merged_df["critical_mineral"].fillna("Other")

#Custom classification method
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
#Feature engineering a new column for category type
merged_df["CategoryType"] = merged_df["Commodities"].apply(classify_commodity)

#Converting time to numeric
merged_df["Time"] = merged_df["Time"].replace("2025 through June", "2025")
merged_df["Time"] = merged_df["Time"].astype(int)

#Converting import value to numeric
merged_df["Customs Value (Gen) ($US) (Default Member)"] = pd.to_numeric(merged_df["Customs Value (Gen) ($US) (Default Member)"])

#Sort numerically by HS code
merged_df = merged_df.sort_values(by="HS_Code")

merged_df.to_csv("merged_filtered_classified.csv", index=False)

# subsection: number of digits in HS code
df_2digit = merged_df[merged_df["HS_Code"].str.len() == 2]
df_4digit = merged_df[merged_df["HS_Code"].str.len() == 4]
df_6digit = merged_df[merged_df["HS_Code"].str.len() == 6]

df_2digit.to_csv("hs2digit_data.csv", index=False)
df_4digit.to_csv("hs4digit_data.csv", index=False)
df_6digit.to_csv("hs6digit_data.csv", index=False)

#206 missing values for Customs Value (Cons) but 0 for the rest
print(f"Number of Missing Values: \n{merged_df.isna().sum()}")

print(merged_df["Countries"].unique())

# subsection: southeast asia
southeast = ["Singapore", "Indonesia", "Vietnam", "Philippines", "Brunei", "Malaysia", "Thailand", "Cambodia", "Laos", "Burma"]
southeast_countries_df = merged_df[merged_df["Countries"].isin(southeast)]
southeast_countries_df.to_csv("southeast_countries.csv", index = False)

# subsection: east asia
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

#0 duplicates
print(f"Number of Duplicates: \n{merged_df.duplicated().sum()}")

#Top commodities per region
top_southeast_commodities = (
    southeast_countries_df.groupby("Commodities")["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
top_southeast_commodities.plot(kind="barh", title="Top 10 Commodities - Southeast Asia", xlabel="Value ($US)")
plt.show()

#Growth in Imports
imports_by_year_diff = imports_by_year.diff()  
imports_by_year_pct = imports_by_year.pct_change() * 100  

print("Year-over-year change in imports:")
print(imports_by_year_diff)
print("\nYear-over-year % change:")
print(imports_by_year_pct)


imports_by_year_pct.plot(kind="bar", title="YoY % Change in Total Imports", ylabel="% Change")
plt.show()

#Commodity Breakdown
imports_by_year_category = (
    merged_df.groupby(["Time", "CategoryType"])["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .unstack(fill_value=0)  # Each category becomes a column
)

imports_by_year_category.plot(kind="area", stacked=True, figsize=(12,6), title="Imports by Category Over Time", ylabel="Value ($US)")
plt.show()

#Average imports per country
avg_imports_per_country = merged_df.groupby("Countries")["Customs Value (Gen) ($US) (Default Member)"].mean().sort_values(ascending=False)
print(avg_imports_per_country)

avg_imports_per_country.head(10).plot(kind="barh", title="Top 10 Countries by Average Import Value")
plt.show()

#Categories by Region
southeast_category_share = (
    southeast_countries_df.groupby("CategoryType")["Customs Value (Gen) ($US) (Default Member)"].sum()
)
southeast_category_share.plot(kind="pie", autopct="%1.1f%%", title="Southeast Asia Imports by Category")
plt.show()

# Total import per commodity per year
imports_commodity_year = merged_df.groupby(["Time", "Commodities"])["Customs Value (Gen) ($US) (Default Member)"].sum().unstack(fill_value=0)

# Percentage growth from first to last year
growth = (imports_commodity_year.iloc[-1] - imports_commodity_year.iloc[0]) / imports_commodity_year.iloc[0] * 100
top_growth = growth.sort_values(ascending=False).head(10)
print("Top 10 fastest growing commodities (% increase from first year to last):")
print(top_growth)



