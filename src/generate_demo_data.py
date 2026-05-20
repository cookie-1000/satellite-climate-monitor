from pathlib import Path

import numpy as np


YEARS = range(2020, 2026)


def _vegetation_blob(height: int, width: int, center_y: float, center_x: float, spread: float) -> np.ndarray:
    y, x = np.mgrid[0:height, 0:width]
    distance = ((y - center_y) ** 2 + (x - center_x) ** 2) / (2 * spread**2)
    return np.exp(-distance)


def generate_demo_dataset(output_dir: Path, height: int = 120, width: int = 120) -> None:
    """Generate synthetic red and NIR bands with gradual vegetation loss."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)

    base_vegetation = (
        0.70 * _vegetation_blob(height, width, 35, 35, 26)
        + 0.55 * _vegetation_blob(height, width, 82, 75, 34)
        + 0.30 * _vegetation_blob(height, width, 65, 28, 18)
    )
    base_vegetation = np.clip(base_vegetation, 0, 1)

    for index, year in enumerate(YEARS):
        yearly_dir = output_dir / str(year)
        yearly_dir.mkdir(parents=True, exist_ok=True)

        urban_growth = np.zeros((height, width))
        urban_growth[72 - index * 3 : 105, 70 - index * 2 : 112] = 0.12 + index * 0.045
        drought_stress = index * 0.035

        vegetation = np.clip(base_vegetation - urban_growth - drought_stress, 0, 1)
        noise = rng.normal(0, 0.018, size=(height, width))

        red = np.clip(0.22 + (1 - vegetation) * 0.22 + noise, 0.02, 0.95)
        nir = np.clip(0.24 + vegetation * 0.58 + noise, 0.02, 0.98)

        np.save(yearly_dir / "red.npy", red.astype(np.float32))
        np.save(yearly_dir / "nir.npy", nir.astype(np.float32))
