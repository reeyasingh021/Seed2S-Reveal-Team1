# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="Critical Minerals Import Dashboard", layout="wide")

# -------------------------------
# Load and preprocess data
# -------------------------------
st.title("Critical Minerals Import Dashboard")

@st.cache_data
def load_and_process_data(files):
    # Load CSVs
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)

    # Remove unwanted countries
    remove = ["Bhutan", "Maldives","ASEAN - Association of Southeast Asian Nations",
              "APEC - Asia Pacific Economic Co-operation","Asia - South"]
    df = df[~df["Countries"].isin(remove)]

    # Keep important columns
    important_cols = ["Commodities", "Countries", "Time",
                      "Customs Value (Gen) ($US) (Default Member)",
                      "Customs Value (Cons) ($US)"]
    df = df[important_cols]

    # Clean Commodities
    df["Commodities"] = df["Commodities"].str.strip()
    df["HS_Code"] = df["Commodities"].str.split().str[0].astype(str)

    # Critical mineral mapping
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

    df["critical_mineral"] = df["Commodities"].map(critical_mineral_map).fillna("Other")

    # Commodity category
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

    df["CategoryType"] = df["Commodities"].apply(classify_commodity)

    # Time and numeric conversions
    df["Time"] = df["Time"].replace("2025 through June", "2025").astype(int)
    df["Customs Value (Gen) ($US) (Default Member)"] = pd.to_numeric(
        df["Customs Value (Gen) ($US) (Default Member)"]
    )

    df = df.sort_values(by="HS_Code")
    return df

files = ["data1.csv", "data2.csv", "data3.csv"]
df = load_and_process_data(files)

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

# Year filter
years = df["Time"].unique()
selected_years = st.sidebar.multiselect("Select Years", options=years, default=years)

# Region filter
regions = {
    "Southeast Asia": ["Singapore", "Indonesia", "Vietnam", "Philippines", "Brunei",
                       "Malaysia", "Thailand", "Cambodia", "Laos", "Burma"],
    "East Asia": ["Taiwan", "Korea, South", "Hong Kong", "Japan", "Macau", "Mongolia"],
}
selected_region = st.sidebar.selectbox("Select Region", options=list(regions.keys()))

# Commodity filter
commodities = df["Commodities"].unique()
selected_commodities = st.sidebar.multiselect("Select Commodities", options=commodities, default=commodities[:5])

# Apply filters
df_filtered = df[
    (df["Time"].isin(selected_years)) &
    (df["Countries"].isin(regions[selected_region])) &
    (df["Commodities"].isin(selected_commodities))
]

st.write(f"Showing {df_filtered.shape[0]} records after filtering.")

# -------------------------------
# Metrics
# -------------------------------
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Import Value ($US)", f"{df_filtered['Customs Value (Gen) ($US) (Default Member)'].sum():,.0f}")
col2.metric("Number of Commodities", len(df_filtered["Commodities"].unique()))
col3.metric("Number of Countries", len(df_filtered["Countries"].unique()))

# -------------------------------
# Visualizations
# -------------------------------
st.subheader("Imports Over Time")
imports_by_year = df_filtered.groupby("Time")["Customs Value (Gen) ($US) (Default Member)"].sum()
st.line_chart(imports_by_year)

st.subheader("Top Commodities")
imports_by_commodity = df_filtered.groupby("Commodities")["Customs Value (Gen) ($US) (Default Member)"].sum().sort_values(ascending=False).head(10)
st.bar_chart(imports_by_commodity)

st.subheader("Imports by Category Type")
imports_by_category = df_filtered.groupby("CategoryType")["Customs Value (Gen) ($US) (Default Member)"].sum()
fig, ax = plt.subplots(figsize=(6, 6))
imports_by_category.plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90, ylabel='')
st.pyplot(fig)

# -------------------------------
# Data Table
# -------------------------------
st.subheader("Data Table")
st.dataframe(df_filtered.reset_index(drop=True))

# -------------------------------
# CSV Download
# -------------------------------
csv = df_filtered.to_csv(index=False)
st.download_button("Download Filtered Data", csv, "filtered_data.csv", "text/csv")




