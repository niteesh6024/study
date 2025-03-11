import numpy as np

class BlankFrameDetector:
    def __init__(self, mean_threshold=15, std_dev_threshold=10, dark_pixel_ratio=0.95):
        self.mean_threshold = mean_threshold
        self.std_dev_threshold = std_dev_threshold
        self.dark_pixel_ratio = dark_pixel_ratio

    def is_blank(self, grey_histogram):
        total_pixels = sum(grey_histogram)
        if total_pixels == 0:
            return False

        intensity_levels = np.arange(len(grey_histogram))
        mean_intensity = sum(intensity_levels * np.array(grey_histogram)) / total_pixels

        variance = sum(((intensity_levels - mean_intensity) ** 2) * np.array(grey_histogram)) / total_pixels
        std_dev = np.sqrt(variance)

        dark_pixel_count = sum(grey_histogram[:50])
        dark_pixel_ratio_actual = dark_pixel_count / total_pixels

        return (
            mean_intensity < self.mean_threshold
            and std_dev < self.std_dev_threshold
            and dark_pixel_ratio_actual > self.dark_pixel_ratio
        )
