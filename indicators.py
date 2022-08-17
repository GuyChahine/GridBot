import pandas as pd
import numpy as np

class ExponentialMovingAverage():
    def __init__(self, length: int, data: np.ndarray) -> np.ndarray:
        self.length = length
        self.ma = pd.Series(data).ewm(span=self.length).mean().to_numpy()
            
class SimpleMovingAverage():
    def __init__(self, length: int, data: np.ndarray) -> np.ndarray:
        self.length = length
        temp_ma = np.convolve(data, np.ones(self.length), 'valid') / self.length
        self.ma = np.concatenate([[np.nan]*(self.length-1), temp_ma])