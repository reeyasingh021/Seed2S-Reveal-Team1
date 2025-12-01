# Critical Minerals and International Trade: Data Visualization Project

**SEED2S + Reveal Global Consulting**  
*Authors: Zoe Caruncho, Vikranth Reddy Karnati, & Reeya Singh*

## 📋 Project Overview

This project examines U.S. critical mineral import patterns from East and Southeast Asia (2001-2025) to assess supply chain diversity, resilience, and geopolitical risks. The analysis focuses on 16 countries across the region, excluding China to reveal alternative diversification opportunities beyond the dominant global processor.

### Key Findings
- **$92.7 billion** in total U.S. imports from the region (2001-2025)
- **300% increase** in import values from 2001 to 2022
- **85%** of imports concentrated in just 5 countries (Japan, South Korea, Thailand, Taiwan, Indonesia)
- **73.5%** of imports are refined metals or finished products (not raw materials)
- **Only 1.5%** are raw ores, revealing heavy reliance on foreign processing capacity

---

## 🗂️ Repository Structure

```
├── data/
│   ├── raw/                          # Raw CSV files from USA Trade Online
│   │   ├── segment_1.csv
│   │   ├── segment_2.csv
│   │   └── segment_3.csv
│   ├── processed/
│   │   └── cleaned_trade_data.csv    # Cleaned and categorized dataset
│   └── mappings/
│       ├── country_regions.csv       # Regional classification of countries
│       └── hs_code_minerals.csv      # HS code to mineral type mapping
│
├── scripts/
│   ├── data_cleaning.py              # Data preparation and cleaning
│   ├── data_analysis.py              # Exploratory data analysis
│   └── utils.py                      # Helper functions
│
├── dashboard/
│   ├── app.py                        # Main Streamlit dashboard application
│   ├── visualizations.py             # Chart and map generation functions
│   └── config.py                     # Dashboard configuration settings
│
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── whitepaper.pdf                     # Full project white paper
```

---

## 📊 Datasets

### 1. Primary Data Source
**USA Trade Online** - U.S. Census Bureau  
- **URL**: https://usatrade.census.gov/
- **Description**: Official U.S. import and export statistics with HS-coded trade data
- **Time Period**: 2001 - Mid-2025 (monthly data aggregated annually)
- **Geographic Scope**: 16 countries across East and Southeast Asia

#### Countries Included:
**East Asia**: Japan, South Korea, Taiwan, Hong Kong, Macau, Mongolia  
**Southeast Asia**: Indonesia, Vietnam, Philippines, Thailand, Singapore, Malaysia, Cambodia, Laos, Burma (Myanmar), Brunei

**Note**: China excluded due to dominant market position (60-100% control across key minerals)

### 2. Data Structure
Each record contains:
- **HS Code**: Harmonized System commodity classification code
- **Commodity Description**: Detailed product description
- **Country**: Country of origin
- **Year/Month**: Temporal dimension
- **Customs Value**: Import value in U.S. dollars

### 3. Critical Minerals Analyzed
Based on the **2025 U.S. Department of Energy List of Critical Minerals**:
- **Base Metals**: Copper, Aluminum, Nickel, Zinc
- **Battery Materials**: Lithium, Cobalt, Graphite, Manganese
- **Rare Earth Elements**: Dysprosium, Neodymium, Praseodymium
- **Strategic Metals**: Titanium, Platinum Group Metals

### 4. Data Limitations
- Dataset downloaded in three segments due to USA Trade Online export size limits
- Lacks physical quantity measures (kg/tons) - analysis based on monetary value only
- Partial 2025 data (through mid-year)
- No inflation adjustment applied

---

## 🔧 Data Cleaning & Analysis Scripts

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/critical-minerals-trade.git
cd critical-minerals-trade
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Script 1: `data_cleaning.py`

**Purpose**: Merge raw data segments, standardize commodity names, categorize processing stages, and output cleaned dataset.

**Key Functions**:
- `merge_segments()`: Combines three raw CSV files into unified dataset
- `classify_commodity_type()`: Categorizes commodities into processing stages:
  - **Ore/Raw**: Unprocessed minerals and concentrates
  - **Compound**: Chemical forms (oxides, hydroxides)
  - **Refined/Articles**: Processed metals and manufactured products
  - **Advanced Product**: Batteries, magnets, high-tech components
- `standardize_names()`: Cleans whitespace and formatting inconsistencies
- `validate_data()`: Checks for missing values and duplicates

**Usage**:
```bash
python scripts/data_cleaning.py
```

**Input**: `data/raw/segment_*.csv`  
**Output**: `data/processed/cleaned_trade_data.csv`

**Expected Runtime**: 2-5 minutes depending on dataset size

---

### Script 2: `data_analysis.py`

**Purpose**: Exploratory data analysis generating summary statistics and preliminary visualizations.

**Key Functions**:
- `temporal_analysis()`: Calculates year-over-year growth rates and trends
- `country_concentration()`: Measures geographic concentration using top-N suppliers
- `commodity_composition()`: Breaks down imports by mineral type and processing stage
- `generate_heatmaps()`: Creates cross-country import value matrices
- `export_summary_stats()`: Produces CSV summaries for key metrics

**Usage**:
```bash
python scripts/data_analysis.py
```

**Outputs**:
- Summary statistics printed to console
- Static visualizations saved to `outputs/figures/`
- Summary CSV files in `outputs/tables/`

**Key Insights Generated**:
- Top importing countries by value
- Mineral composition breakdown
- Processing stage distribution
- Annual import trends

---

### Script 3: `utils.py`

**Purpose**: Shared utility functions for data processing and visualization.

**Key Functions**:
- `load_data()`: Standardized data loading with error handling
- `filter_by_year_range()`: Temporal filtering helper
- `calculate_concentration_index()`: Computes HHI and other concentration metrics
- `format_currency()`: Consistent monetary value formatting
- `get_country_coordinates()`: Returns lat/lon for mapping

**Usage**: Import functions as needed in other scripts
```python
from utils import load_data, filter_by_year_range
```

---

## 🎛️ Interactive Dashboard

### Access the Dashboard

**Live Application**: https://seed2s-reveal-team1.streamlit.app/

The dashboard is deployed on Streamlit Cloud and accessible directly via the link above. No local installation required for viewing.

---

### Running the Dashboard Locally

If you want to run the dashboard on your local machine:

1. **Ensure all dependencies are installed**
```bash
pip install -r requirements.txt
```

2. **Navigate to dashboard directory**
```bash
cd dashboard
```

3. **Launch Streamlit app**
```bash
streamlit run app.py
```

4. **Access in browser**: The app will automatically open at `http://localhost:8501`

---

### Dashboard Features

#### 🔍 Interactive Filters
- **Year Range Selector**: Analyze specific time periods (2001-2025)
- **Region Filter**: Toggle between East Asia, Southeast Asia, or combined view
- **Commodity Type**: Filter by Ore/Raw, Compound, Refined/Articles, or Advanced Products
- **Mineral Selector**: Focus on specific critical minerals

#### 📈 Visualizations

1. **Temporal Trends**
   - Line charts showing import values over time
   - Year-over-year growth rates
   - Peak and decline identification

2. **Geographic Distribution**
   - Interactive map with bubble sizes representing import values
   - Color-coded by region
   - Hover tooltips with detailed country statistics

3. **Commodity Composition**
   - Pie charts of import breakdown by processing stage
   - Bar charts of top minerals by value
   - Stacked area charts showing composition changes over time

4. **Concentration Analysis**
   - Heatmaps of country-year import values
   - Top-N supplier concentration metrics
   - Diversification scoring

#### 🗺️ Geospatial Mapping
Built with **Pydeck**, the map visualization:
- Plots all 16 countries with precise coordinates
- Scales bubble size to import volume
- Allows zoom and pan for detailed regional analysis
- Updates dynamically based on filter selections

---

### Dashboard Code Structure

#### `app.py` - Main Application
```python
# Core structure:
# 1. Load and cache data
# 2. Render sidebar filters
# 3. Apply user selections
# 4. Generate filtered visualizations
# 5. Display summary statistics
```

**Key Libraries**:
- `streamlit`: Web application framework
- `pandas`: Data manipulation
- `plotly`: Interactive charts
- `pydeck`: Geospatial visualization
- `matplotlib`: Static plots

#### `visualizations.py` - Chart Generation
Contains modular functions for each visualization type:
- `create_temporal_chart()`
- `create_commodity_breakdown()`
- `create_country_map()`
- `create_heatmap()`

#### `config.py` - Configuration
- Country coordinates dictionary
- Color schemes
- Default filter values
- Map styling parameters

---

## 🛠️ Technical Requirements

### Python Version
- **Python 3.8+** required

### Dependencies
```txt
pandas>=1.5.0
numpy>=1.23.0
streamlit>=1.28.0
plotly>=5.17.0
pydeck>=0.8.0
matplotlib>=3.7.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 📖 How to Use This Repository

### For Policy Analysts
1. Access the **live dashboard** to explore import patterns interactively
2. Review the **white paper** for detailed findings and national security implications
3. Use filter combinations to assess specific minerals or countries of interest

### For Data Scientists
1. **Clone the repository** and examine the data cleaning pipeline
2. Run **analysis scripts** to reproduce findings
3. Modify `data_analysis.py` to test alternative hypotheses
4. Extend the dashboard with additional metrics or visualizations

### For Researchers
1. Review the **methodology section** in the white paper
2. Examine **HS code classifications** and processing stage categorization
3. Build on this foundation for expanded regional analysis or scenario modeling

---

## 🔐 National Security Implications

This analysis reveals critical vulnerabilities in U.S. critical mineral supply chains:

1. **Processing Dependency**: 73.5% of imports are refined products, creating midstream chokepoints
2. **Geographic Concentration**: 5 countries control 85% of supply
3. **Strategic Mineral Risk**: Limited diversification in lithium, rare earths, and nickel
4. **Defense Exposure**: High-purity compounds essential for defense electronics concentrated in few suppliers

**Key Recommendations**:
- Expand domestic refining capacity
- Strengthen partnerships with emerging regional suppliers (Indonesia, Vietnam, Philippines)
- Reduce midstream processing bottlenecks
- Enhance supply chain transparency and monitoring

---

## 📚 References & Resources

1. **International Energy Agency** - Global Critical Minerals Outlook 2025  
   https://www.iea.org/reports/global-critical-minerals-outlook-2025

2. **U.S. Department of Interior** - 2025 List of Critical Minerals  
   https://www.doi.gov/pressreleases/interior-department-releases-final-2025-list-critical-minerals

3. **U.S. Census Bureau** - USA Trade Online  
   https://usatrade.census.gov/

4. **U.S. Department of Energy** - Critical Minerals and Materials  
   https://www.energy.gov/policy/critical-minerals-and-materials

---

## 🤝 Contributing

This project was developed for SEED2S and Reveal Global Consulting. For questions or collaboration opportunities:

- Review the white paper for detailed methodology
- Submit issues or suggestions via GitHub Issues
- Contact project team for data access or technical questions

---

## 📄 License

This project is part of an academic/consulting collaboration. Please contact the project team for usage permissions.

---

## 🔄 Future Research Directions

1. **Country-Specific Case Studies**: Deep-dive analyses of Indonesia, Vietnam, Philippines
2. **Midstream Bottleneck Mapping**: Identify specific processing facilities and capacity constraints
3. **Trade Policy Analysis**: Assess impact of FTAs and export restrictions
4. **Scenario Modeling**: Quantify risks from regional disruptions
5. **Technology Development Tracking**: Monitor regional innovation in battery tech and materials processing

---

## 📞 Contact

**Project Team**: SEED2S + Reveal Global Consulting  
**Authors**: Zoe Caruncho, Vikranth Reddy Karnati, Reeya Singh

For inquiries about this analysis or dashboard access, please refer to the white paper or contact the project team.

---

*Last Updated: December 2025*
