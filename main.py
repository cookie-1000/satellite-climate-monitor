from pathlib import Path

from src.generate_demo_data import generate_demo_dataset
from src.process import run_ndvi_pipeline
from src.visualize import create_heatmap_grid, create_trend_chart


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "demo_region"
OUTPUT_DIR = BASE_DIR / "outputs"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating demo satellite bands...")
    generate_demo_dataset(DATA_DIR)

    print("Calculating NDVI and yearly summaries...")
    records, ndvi_by_year = run_ndvi_pipeline(DATA_DIR, OUTPUT_DIR)

    print("Creating visualizations...")
    create_trend_chart(records, OUTPUT_DIR / "ndvi_trend.png")
    create_heatmap_grid(ndvi_by_year, OUTPUT_DIR / "ndvi_heatmaps.png")

    print("\nMVP pipeline complete.")
    print(f"Summary: {OUTPUT_DIR / 'ndvi_summary.csv'}")
    print(f"Trend chart: {OUTPUT_DIR / 'ndvi_trend.png'}")
    print(f"Heatmaps: {OUTPUT_DIR / 'ndvi_heatmaps.png'}")


if __name__ == "__main__":
    main()
