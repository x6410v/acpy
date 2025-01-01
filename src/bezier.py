import numpy as np
from model import generate_control_points
import math


def bezier_curve(start, end, n_points=100):
    control_points = generate_control_points(start, end)
    points = np.array([start] + control_points + [end])  # Convert points to NumPy array
    n = len(points) - 1
    t = np.linspace(0, 1, n_points)
    curve = np.zeros((n_points, 2))

    for i in range(n_points):
        for j in range(n + 1):
            bernstein = (math.factorial(n) /
                        (math.factorial(j) * math.factorial(n - j))) * \
                        (t[i] ** j) * ((1 - t[i]) ** (n - j))
            curve[i] += bernstein * points[j]  # points[j] is now a NumPy array

    return curve