from metrics.trajectory_metric import TMetric
from state import State
from utils import *

class MaxCurvatureMetric(TMetric):
    """
    Computes the maximum curvature of the given trajectory.
	    @param trajectory The trajectory to evaluate.
	    @return Maximum curvature.
    """
    
    def __init__(self, more_is_better=False):
        super().__init__(more_is_better)
    
    @staticmethod
    def evaluate_metric(path, **kwargs):
        x1 = x2 = x3 = y1 = y2 = y3 = v1x = v2x = v1y = v2y = v1 = v2 = 0.0
        infinity = 1e10
        maxK = 0.0
        
        traj_size = len(path)

        # Handles the empty input path, setting curvature to infinity
        if traj_size == 0:
            maxK = infinity
            return maxK
		
        # Handles the input path of length 1 or 2, setting curvature to 0
        if traj_size < 3:
            return 0

        # We can compute the curvature in all the points of the path
        # except the first and the last one
        for i in range(traj_size - 2):
            # skip by 2 two steps in both directions
            # to better catch abrupt changes in position
            x1 = path[i].x
            y1 = path[i].y

            while True:
                i += 1
                if i >= len(path):
                    return maxK
                x2 = path[i].x
                y2 = path[i].y
                if distance(x1, y1, x2, y2) >= 0.3:
                    break
            while True:
                i += 1
                if i >= len(path):
                    return maxK
                x3 = path[i].x
                y3 = path[i].y
                if distance(x2, y2, x3, y3) >= 0.3:
                    break
			
            # if two points in a row repeat, we skip curvature computation
            if (x1 == x2 and y1 == y2 or x2 == x3 and y2 == y3):
                continue

			# Infinite curvature in case the path goes a step backwards:
			# p1 - p2 - p1
            if (x1 == x3 and y1 == y3):
                continue

			# Compute center of circle that goes through the 3 points
            cx = (x3**2 * (-y1 + y2) + x2**2 * (y1 - y3) - \
                (x1**2 + (y1 - y2) * (y1 - y3)) * (y2 - y3)) / \
                    (2. * (x3 * (-y1 + y2) + x2 * (y1 - y3) + x1 * (-y2 + y3)))
            cy = (-(x2**2 * x3) + x1**2 * (-x2 + x3) + x3 \
                * (y1**2 - y2**2) + x1 * (x2**2 - x3**2 + y2**2 - y3**2) \
                + x2 * (x3**2 - y1**2 + y3**2)) / (2. * (x3 * (y1 - y2) + x1 * (y2 - y3) + x2 * (-y1 + y3)))

			# Curvature = 1/Radius
            radius = hypot(x1 - cx, y1 - cy)
            ki = 1. / radius

            if (ki > maxK):
                maxK = ki
        return maxK
    