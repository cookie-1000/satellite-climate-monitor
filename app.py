from pathlib import Path

import pandas as pd
import streamlit as st

from src.generate_demo_data import generate_demo_dataset
from src.process import run_ndvi_pipeline
from src.visualize import create_heatmap_grid, create_trend_chart


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "demo_region"
OUTPUT_DIR = BASE_DIR / "outputs"
SUMMARY_PATH = OUTPUT_DIR / "ndvi_summary.csv"
TREND_PATH = OUTPUT_DIR / "ndvi_trend.png"
HEATMAP_PATH = OUTPUT_DIR / "ndvi_heatmaps.png"


st.set_page_config(page_title="Satellite Climate Monitor", layout="wide")

st.title("Satellite Climate Monitoring System")
st.caption("MVP dashboard for vegetation change detection using NDVI.")


def ensure_outputs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not SUMMARY_PATH.exists() or not TREND_PATH.exists() or not HEATMAP_PATH.exists():
        generate_demo_dataset(DATA_DIR)
        records, ndvi_by_year = run_ndvi_pipeline(DATA_DIR, OUTPUT_DIR)
        create_trend_chart(records, TREND_PATH)
        create_heatmap_grid(ndvi_by_year, HEATMAP_PATH)


ensure_outputs()

summary = pd.read_csv(SUMMARY_PATH)

latest = summary.iloc[-1]
first = summary.iloc[0]
change = latest["average_ndvi"] - first["average_ndvi"]
change_pct = (change / first["average_ndvi"]) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Start Year", int(first["year"]), f"{first['average_ndvi']:.3f} NDVI")
col2.metric("Latest Year", int(latest["year"]), f"{latest['average_ndvi']:.3f} NDVI")
col3.metric("NDVI Change", f"{change:+.3f}", f"{change_pct:+.1f}%")

left, right = st.columns([1, 1])

with left:
    st.subheader("Average NDVI Trend")
    st.image(str(TREND_PATH), width="stretch")

with right:
    st.subheader("Yearly NDVI Summary")
    st.dataframe(summary, hide_index=True, width="stretch")

st.subheader("NDVI Heatmaps")
st.image(str(HEATMAP_PATH), width="stretch")
