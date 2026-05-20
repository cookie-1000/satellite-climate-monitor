import numpy as np


def calculate_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """Calculate NDVI from aligned near-infrared and red bands."""
    denominator = nir + red
    ndvi = np.divide(nir - red, denominator, out=np.zeros_like(nir), where=denominator != 0)
    return np.clip(ndvi, -1, 1)


def summarize_ndvi(year: int, ndvi: np.ndarray, vegetation_threshold: float = 0.30) -> dict[str, float | int]:
    vegetation_mask = ndvi >= vegetation_threshold
    return {
        "year": year,
        "average_ndvi": float(np.mean(ndvi)),
        "median_ndvi": float(np.median(ndvi)),
        "min_ndvi": float(np.min(ndvi)),
        "max_ndvi": float(np.max(ndvi)),
        "vegetation_pixels": int(np.sum(vegetation_mask)),
        "vegetation_percent": float(np.mean(vegetation_mask) * 100),
    }
