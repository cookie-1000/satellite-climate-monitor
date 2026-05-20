from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def create_trend_chart(records: list[dict[str, float | int]], output_path: Path) -> None:
    years = [int(record["year"]) for record in records]
    average_ndvi = [float(record["average_ndvi"]) for record in records]
    vegetation_percent = [float(record["vegetation_percent"]) for record in records]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(years, average_ndvi, marker="o", linewidth=2.5, color="#287c71")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Average NDVI", color="#287c71")
    ax1.tick_params(axis="y", labelcolor="#287c71")
    ax1.set_ylim(0, max(average_ndvi) + 0.12)
    ax1.grid(True, alpha=0.25)

    ax2 = ax1.twinx()
    ax2.plot(years, vegetation_percent, marker="s", linewidth=2, color="#b85c38")
    ax2.set_ylabel("Vegetation Pixels (%)", color="#b85c38")
    ax2.tick_params(axis="y", labelcolor="#b85c38")
    ax2.set_ylim(0, 100)

    fig.suptitle("Vegetation Change Over Time")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def create_heatmap_grid(ndvi_by_year: dict[int, np.ndarray], output_path: Path) -> None:
    years = sorted(ndvi_by_year)
    cols = 3
    rows = int(np.ceil(len(years) / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(11, 7), constrained_layout=True)
    axes_array = np.atleast_1d(axes).ravel()

    for axis, year in zip(axes_array, years):
        image = axis.imshow(ndvi_by_year[year], cmap="RdYlGn", vmin=-0.2, vmax=0.8)
        axis.set_title(str(year))
        axis.set_xticks([])
        axis.set_yticks([])

    for axis in axes_array[len(years) :]:
        axis.axis("off")

    fig.colorbar(image, ax=axes_array.tolist(), shrink=0.82, label="NDVI")
    fig.suptitle("NDVI Heatmaps by Year")
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
