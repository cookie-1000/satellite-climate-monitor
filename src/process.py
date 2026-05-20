from pathlib import Path
import csv

import numpy as np

from src.ndvi import calculate_ndvi, summarize_ndvi


SUMMARY_COLUMNS = [
    "year",
    "average_ndvi",
    "median_ndvi",
    "min_ndvi",
    "max_ndvi",
    "vegetation_pixels",
    "vegetation_percent",
]


def _load_band(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Missing required band: {path}")
    return np.load(path)


def run_ndvi_pipeline(data_dir: Path, output_dir: Path) -> tuple[list[dict[str, float | int]], dict[int, np.ndarray]]:
    output_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, float | int]] = []
    ndvi_by_year: dict[int, np.ndarray] = {}

    year_dirs = sorted(path for path in data_dir.iterdir() if path.is_dir() and path.name.isdigit())
    if not year_dirs:
        raise FileNotFoundError(f"No yearly data folders found in {data_dir}")

    for year_dir in year_dirs:
        year = int(year_dir.name)
        red = _load_band(year_dir / "red.npy")
        nir = _load_band(year_dir / "nir.npy")

        if red.shape != nir.shape:
            raise ValueError(f"Red and NIR bands for {year} have different shapes.")

        ndvi = calculate_ndvi(nir=nir, red=red)
        np.save(year_dir / "ndvi.npy", ndvi.astype(np.float32))

        records.append(summarize_ndvi(year, ndvi))
        ndvi_by_year[year] = ndvi

    summary_path = output_dir / "ndvi_summary.csv"
    with summary_path.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(records)

    return records, ndvi_by_year
