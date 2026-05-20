# Satellite Climate Monitoring System

An MVP data science project that measures vegetation change over time using satellite-style imagery and NDVI.

## Project Question

How has vegetation changed in one region over multiple years?

This MVP uses demo satellite bands so the project runs immediately without API keys. The pipeline is structured so real Landsat or Sentinel imagery can be added later.

## What It Does

1. Generates sample red and near-infrared satellite bands for 2020-2025.
2. Calculates NDVI for every year.
3. Computes average vegetation health over time.
4. Creates heatmaps and a trend chart.
5. Provides a Streamlit dashboard for interactive viewing.

## Project Structure

```text
satellite-climate-monitor/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── data/
├── outputs/
└── src/
    ├── __init__.py
    ├── generate_demo_data.py
    ├── ndvi.py
    ├── process.py
    └── visualize.py
```

## Quick Start

Create a virtual environment if you want one, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the full MVP pipeline:

```bash
python main.py
```

This creates:

```text
data/demo_region/
outputs/ndvi_summary.csv
outputs/ndvi_trend.png
outputs/ndvi_heatmaps.png
```

Launch the dashboard:

```bash
streamlit run app.py
```

## Core Science

NDVI stands for Normalized Difference Vegetation Index. It estimates vegetation health using near-infrared and red light bands.

```text
NDVI = (NIR - Red) / (NIR + Red)
```

Higher NDVI usually means denser or healthier vegetation. Lower NDVI may indicate urban areas, water, bare land, drought stress, or vegetation loss.

## MVP Output

The project produces a yearly table like:

```text
year,average_ndvi,vegetation_pixels
2020,0.53,25174
2021,0.50,23641
2022,0.47,22195
```

It also creates a line chart and heatmaps so the change is visually clear.

## How To Use Real Satellite Data Later

Replace the demo `.npy` files in `data/demo_region/` with real red and NIR bands from Landsat or Sentinel.

Recommended band pairings:

```text
Landsat 8/9: Red = Band 4, NIR = Band 5
Sentinel-2:  Red = Band 4, NIR = Band 8
```

Real-data upgrade steps:

1. Download cloud-filtered imagery for one region and several dates.
2. Crop all bands to the same bounding box.
3. Save aligned red and NIR arrays.
4. Run the same NDVI and visualization pipeline.

## Good Extensions

- Add real Landsat or Sentinel downloads.
- Add cloud masking.
- Compare two cities.
- Build a map view.
- Add forecasting for future vegetation loss.
- Train a model to classify land cover types.
