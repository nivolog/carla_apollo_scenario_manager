from .trajectory_metric import TMetric
from state import State
from utils import *


class TimeMetric(TMetric):
    def __init__(self, more_is_better=False):
          super().__init__(more_is_better)
    
    @staticmethod
    def evaluate_metric(trajectory, **kwargs):
        total_time = 0
        if (len(trajectory) < 2):
            return total_time
        else:
            return trajectory[-1].timestamp - trajectory[0].timestamp