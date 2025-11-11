# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Critical Minerals Dashboard",
    page_icon="🔩",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    merged = pd.read_csv("merged_filtered_classified.csv")
    east = pd.read_csv("east_countries.csv")
    southeast = pd.read_csv("southeast_countries.csv")
    return merged, east, southeast

merged_df, east_df, southeast_df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "🌍 Select Region",
    ["East and Southeast Asia", "East Asia", "Southeast Asia"]
)

year_range = st.sidebar.slider(
    "📅 Select Year Range",
    int(merged_df["Time"].min()),
    int(merged_df["Time"].max()),
    (int(merged_df["Time"].min()), int(merged_df["Time"].max()))
)

category_filter = st.sidebar.multiselect(
    "🧩 Filter by Category Type",
    sorted(merged_df["CategoryType"].unique()),
    default=sorted(merged_df["CategoryType"].unique())
)

mineral_filter = st.sidebar.multiselect(
    "🔹 Filter by Critical Mineral",
    sorted(merged_df["critical_mineral"].unique()),
    default=sorted(merged_df["critical_mineral"].unique())
)

# -------------------------------
# FILTER DATA
# -------------------------------
if region == "East Asia":
    data = east_df
elif region == "Southeast Asia":
    data = southeast_df
else:
    data = merged_df

# Handle empty selections gracefully
if not category_filter:
    category_filter = sorted(data["CategoryType"].unique())
if not mineral_filter:
    mineral_filter = sorted(data["critical_mineral"].unique())

# Handle invalid or empty year range
min_year, max_year = int(data["Time"].min()), int(data["Time"].max())
if year_range[0] > year_range[1]:
    year_range = (min_year, max_year)

# Apply filters
data = data[
    (data["Time"].between(year_range[0], year_range[1])) &
    (data["CategoryType"].isin(category_filter)) &
    (data["critical_mineral"].isin(mineral_filter))
]

# -------------------------------
# DASHBOARD TITLE
# -------------------------------
st.title("🔩 Critical Minerals Trade Dashboard")
st.markdown(f"### Region: **{region}**  |  Years: **{year_range[0]} - {year_range[1]}**")

# -------------------------------
# SUMMARY STATS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

total_imports = data["Customs Value (Gen) ($US) (Default Member)"].sum()
top_country = data.groupby("Countries")["Customs Value (Gen) ($US) (Default Member)"].sum().idxmax()
top_commodity = data.groupby("Commodities")["Customs Value (Gen) ($US) (Default Member)"].sum().idxmax()

col1.metric("🌎 Total Import Value (USD)", f"{total_imports:,.0f}")
col2.metric("🏳️‍🌈 Top Importing Country", top_country)
col3.metric("⚙️ Top Commodity", top_commodity)
col4.metric("Total Countries", data["Countries"].nunique())

st.markdown("---")

# -------------------------------
# CHARTS SECTION
# -------------------------------
# 1. Imports Over Time
st.subheader("📈 Import Trends Over Time")
imports_by_year = data.groupby("Time")["Customs Value (Gen) ($US) (Default Member)"].sum().reset_index()
fig_time = px.line(
    imports_by_year,
    x="Time",
    y="Customs Value (Gen) ($US) (Default Member)",
    title="Total Imports Over Time",
    markers=True,
)
st.plotly_chart(fig_time, use_container_width=True)

# 2. Imports by Category
st.subheader("🧩 Imports by Category Type")
imports_by_category = (
    data.groupby("CategoryType")["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .reset_index()
    .sort_values(by="Customs Value (Gen) ($US) (Default Member)", ascending=False)
)
fig_cat = px.pie(
    imports_by_category,
    names="CategoryType",
    values="Customs Value (Gen) ($US) (Default Member)",
    title="Import Share by Category",
)
st.plotly_chart(fig_cat, use_container_width=True)

# 3. Imports by Critical Mineral
st.subheader("🔹 Imports by Critical Mineral")
imports_by_mineral = (
    data.groupby("critical_mineral")["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .reset_index()
    .sort_values(by="Customs Value (Gen) ($US) (Default Member)", ascending=False)
)
fig_mineral = px.bar(
    imports_by_mineral,
    x="Customs Value (Gen) ($US) (Default Member)",
    y="critical_mineral",
    orientation="h",
    title="Imports by Critical Mineral",
)
st.plotly_chart(fig_mineral, use_container_width=True)

# 4. Top Commodities
st.subheader("🏗️ Top 10 Commodities by Import Value")
imports_by_commodity = (
    data.groupby("Commodities")["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig_commodity = px.bar(
    imports_by_commodity,
    x="Customs Value (Gen) ($US) (Default Member)",
    y="Commodities",
    orientation="h",
    title="Top 10 Commodities",
)
st.plotly_chart(fig_commodity, use_container_width=True)

# 5. Imports by Country
st.subheader("🌏 Top 10 Countries by Import Value")
imports_by_country = (
    data.groupby("Countries")["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig_country = px.bar(
    imports_by_country,
    x="Customs Value (Gen) ($US) (Default Member)",
    y="Countries",
    orientation="h",
    title="Top 10 Countries",
)
st.plotly_chart(fig_country, use_container_width=True)



# # -------------------------------
# # DOWNLOAD BUTTON
# # -------------------------------
# csv = data.to_csv(index=False).encode("utf-8")
# st.download_button(
#     label="💾 Download Filtered Data as CSV",
#     data=csv,
#     file_name="filtered_data.csv",
#     mime="text/csv"
# )

# ==============================================================
# 🔍 ADVANCED ANALYTICS SECTION (merged from your second script)
# ==============================================================
st.markdown("---")
st.header("📊 Advanced Analytics")

# 1. Mineral Imports by Country Over Time
st.subheader("1️⃣ Mineral Imports by Country Over Time")
selected_mineral = st.selectbox("Select Mineral", sorted(data["critical_mineral"].unique()))
value_type = st.radio("Display as:", ["Absolute Values ($US)", "Percentage of Total"], horizontal=True)

df_mineral = data[data["critical_mineral"] == selected_mineral]
if not df_mineral.empty:
    pivot_data = df_mineral.groupby(["Time", "Countries"])["Customs Value (Gen) ($US) (Default Member)"].sum().reset_index()

    if value_type == "Percentage of Total":
        total_by_year = pivot_data.groupby("Time")["Customs Value (Gen) ($US) (Default Member)"].transform("sum")
        pivot_data["Value"] = (pivot_data["Customs Value (Gen) ($US) (Default Member)"] / total_by_year) * 100
        ylabel = "Percentage of Total Imports (%)"
    else:
        pivot_data["Value"] = pivot_data["Customs Value (Gen) ($US) (Default Member)"]
        ylabel = "Import Value ($US)"

    fig, ax = plt.subplots(figsize=(12, 6))
    for country in pivot_data["Countries"].unique():
        ax.plot(
            pivot_data[pivot_data["Countries"] == country]["Time"],
            pivot_data[pivot_data["Countries"] == country]["Value"],
            marker='o', label=country, linewidth=2
        )
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{selected_mineral} Imports by Country")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("No data available for selected mineral.")

# 2. Top Minerals by Import Volume
st.subheader("2️⃣ Top Minerals by Import Volume")
top_n = st.slider("Number of top minerals to display", 5, 20, 10)
mineral_imports = (
    data.groupby("critical_mineral")["Customs Value (Gen) ($US) (Default Member)"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)
fig, ax = plt.subplots(figsize=(12, 6))
mineral_imports.plot(kind='barh', ax=ax, color='steelblue')
ax.set_xlabel("Import Value ($US)")
ax.set_ylabel("Critical Mineral")
ax.set_title(f"Top {top_n} Critical Minerals by Import Value")
plt.tight_layout()
st.pyplot(fig)

# 3. Heatmap: Import Values by Country and Mineral
st.subheader("3️⃣ Heatmap: Import Values by Country and Mineral")
heatmap_mineral = st.selectbox("Select Mineral for Heatmap", ["All Minerals"] + sorted(data["critical_mineral"].unique()))
year_min, year_max = st.slider("Select Year Range for Heatmap", int(data["Time"].min()), int(data["Time"].max()), (int(data["Time"].min()), int(data["Time"].max())))

df_heatmap = data[data["Time"].between(year_min, year_max)]
if heatmap_mineral != "All Minerals":
    df_heatmap = df_heatmap[df_heatmap["critical_mineral"] == heatmap_mineral]

heatmap_data = df_heatmap.groupby(["Countries", "critical_mineral"])["Customs Value (Gen) ($US) (Default Member)"].sum().reset_index()
heatmap_pivot = heatmap_data.pivot(index="Countries", columns="critical_mineral", values="Customs Value (Gen) ($US) (Default Member)").fillna(0)

if not heatmap_pivot.empty:
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(heatmap_pivot, cmap="YlOrRd", ax=ax, cbar_kws={'label': 'Import Value ($US)'})
    ax.set_title(f"Import Values Heatmap: {heatmap_mineral} ({year_min}-{year_max})")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")

# 4. Year-over-Year Import Growth by Mineral
st.subheader("4️⃣ Year-over-Year Import Growth by Mineral")
yoy_data = data.groupby(["Time", "critical_mineral"])["Customs Value (Gen) ($US) (Default Member)"].sum().reset_index()
yoy_data = yoy_data.sort_values(["critical_mineral", "Time"])
yoy_data["YoY_Change"] = yoy_data.groupby("critical_mineral")["Customs Value (Gen) ($US) (Default Member)"].pct_change() * 100
yoy_data_filtered = yoy_data[yoy_data["YoY_Change"].notna()]
if not yoy_data_filtered.empty:
    top_minerals = data.groupby("critical_mineral")["Customs Value (Gen) ($US) (Default Member)"].sum().nlargest(10).index
    yoy_display = yoy_data_filtered[yoy_data_filtered["critical_mineral"].isin(top_minerals)]
    fig, ax = plt.subplots(figsize=(14, 8))
    pivot_yoy = yoy_display.pivot(index="Time", columns="critical_mineral", values="YoY_Change")
    for mineral in pivot_yoy.columns:
        ax.plot(pivot_yoy.index, pivot_yoy[mineral], marker='o', label=mineral, linewidth=2)
    ax.axhline(0, color='black', linestyle='--', alpha=0.6)
    ax.set_xlabel("Year")
    ax.set_ylabel("Year-over-Year Change (%)")
    ax.set_title("Import Growth Rate by Mineral (Top 10 by Volume)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Insufficient data for YoY change.")

# 5. Heatmap: Import Values by Country and Category
st.subheader("5️⃣ Heatmap: Import Values by Country and Category Type")
heatmap_category = st.selectbox("Select Category Type", ["All Categories"] + sorted(data["CategoryType"].unique()))
year_min_cat, year_max_cat = st.slider("Select Year Range for Category Heatmap", int(data["Time"].min()), int(data["Time"].max()), (int(data["Time"].min()), int(data["Time"].max())))
df_heatmap_cat = data[data["Time"].between(year_min_cat, year_max_cat)]
if heatmap_category != "All Categories":
    df_heatmap_cat = df_heatmap_cat[df_heatmap_cat["CategoryType"] == heatmap_category]

heatmap_cat_data = df_heatmap_cat.groupby(["Countries", "CategoryType"])["Customs Value (Gen) ($US) (Default Member)"].sum().reset_index()
heatmap_cat_pivot = heatmap_cat_data.pivot(index="Countries", columns="CategoryType", values="Customs Value (Gen) ($US) (Default Member)").fillna(0)
if not heatmap_cat_pivot.empty:
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_cat_pivot, cmap="Blues", annot=False, ax=ax, cbar_kws={'label': 'Import Value ($US)'})
    ax.set_title(f"Import Values by Category ({year_min_cat}-{year_max_cat})")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("No data available for selected category filters.")




st.subheader("🌏 World Map: Imports by Country")

# Country coordinates
country_coords = {
    "Japan": [36.2048, 138.2529],
    "Indonesia": [-0.7893, 113.9213],
    "Korea, South": [35.9078, 127.7669],
    "Vietnam": [14.0583, 108.2772],
    "Thailand": [15.8700, 100.9925],
    "Singapore": [1.3521, 103.8198],
    "Taiwan": [23.6978, 120.9605],
    "Hong Kong": [22.3193, 114.1694],
    "Malaysia": [4.2105, 101.9758],
    "Mongolia": [46.8625, 103.8467],
    "Philippines": [12.8797, 121.7740],
    "Laos": [19.8563, 102.4955],
    "Cambodia": [12.5657, 104.9910],
    "Macau": [22.1987, 113.5439],
    "Burma": [21.9162, 95.9560],
    "Brunei": [4.5353, 114.7277]
}

# Filter by mineral
map_mineral = st.selectbox(
    "Select Mineral for Map",
    ["All Minerals"] + sorted(data["critical_mineral"].unique())
)
df_map = data.copy()
if map_mineral != "All Minerals":
    df_map = df_map[df_map["critical_mineral"] == map_mineral]

# Aggregate import values by country
map_data = df_map.groupby("Countries")["Customs Value (Gen) ($US) (Default Member)"].sum().reset_index()


map_data = map_data.rename(columns={"Customs Value (Gen) ($US) (Default Member)": "import_value"})

# Add coordinates
map_data["Latitude"] = map_data["Countries"].map(lambda x: country_coords.get(x, [None, None])[0])
map_data["Longitude"] = map_data["Countries"].map(lambda x: country_coords.get(x, [None, None])[1])
map_data = map_data.dropna(subset=["Latitude", "Longitude"])

if not map_data.empty:
    # Normalize radius
    min_val = map_data["import_value"].min()
    max_val = map_data["import_value"].max()

    def normalize_radius(val, min_r=60000, max_r=300000):
        if max_val == min_val:
            return (min_r + max_r) / 2
        return min_r + (val - min_val) / (max_val - min_val) * (max_r - min_r)

    map_data["radius"] = map_data["import_value"].apply(normalize_radius)
    map_data["heat_value"] = map_data["import_value"]

    # Optional: formatted display value for tooltip
    map_data["import_value_display"] = map_data["import_value"].apply(lambda x: f"${x:,.0f}")

    # Define layers
    heat_layer = pdk.Layer(
        "HeatmapLayer",
        data=map_data,
        get_position='[Longitude, Latitude]',
        get_weight="heat_value",
        radiusPixels=60,
        opacity=0.4
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position='[Longitude, Latitude]',
        get_fill_color="[255, 140, 0, 180]",
        get_radius="radius",
        pickable=True,
    )

    # Tooltip for looking at details
    tooltip = {
        "html": "<b>Country:</b> {Countries} <br/>"
                "<b>Import Value ($US):</b> {import_value_display}",
        "style": {"backgroundColor": "white", "color": "black"}
    }

    # View state
    view_state = pdk.ViewState(
        latitude=15,
        longitude=110,
        zoom=3,
        pitch=0
    )

    # Render map
    st.pydeck_chart(pdk.Deck(
        layers=[heat_layer, scatter_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/dark-v10"
    ))
else:
    st.warning("No data available for selected mineral.")


# -------------------------------
# DATA PREVIEW
# -------------------------------
st.markdown("---")
st.subheader("📊 Filtered Data Preview")
st.dataframe(data.head(50))

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------
csv = data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="💾 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
