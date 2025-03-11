import numpy as np
from collections import deque
from datetime import datetime

class FrozenFrameDetector:
    def __init__(self, buffer_size=60, similarity_threshold=0.99, required_match_count=45):
        self.buffer_size = buffer_size
        self.similarity_threshold = similarity_threshold
        self.required_match_count = required_match_count
        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.is_currently_frozen = False
        self.freeze_start_time = None

    def histogram_similarity(self, hist1, hist2):
        hist1 = np.array(hist1)
        hist2 = np.array(hist2)
        return np.corrcoef(hist1, hist2)[0, 1]

    def add_frame(self, histogram):
        self.frame_buffer.append(histogram)

    def is_frozen(self, new_histogram, timestamp):
        if len(self.frame_buffer) < self.buffer_size:
            return False

        similarities = [self.histogram_similarity(hist, new_histogram) for hist in self.frame_buffer]
        high_similarity_count = sum(1 for sim in similarities if sim > self.similarity_threshold)

        is_now_frozen = high_similarity_count >= self.required_match_count

        if is_now_frozen and not self.is_currently_frozen:
            self.freeze_start_time = datetime.fromtimestamp(timestamp / 1000)
            self.is_currently_frozen = True

        elif not is_now_frozen and self.is_currently_frozen:
            freeze_end_time = datetime.fromtimestamp(timestamp / 1000)
            print(f"Frames were frozen from {self.freeze_start_time.strftime('%H:%M:%S')} to {freeze_end_time.strftime('%H:%M:%S')}")

            self.is_currently_frozen = False
            self.freeze_start_time = None

        return is_now_frozen
