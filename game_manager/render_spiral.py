import math


def render_spiral(start_x, start_y, end_x, end_y, max_chunks_to_render):
    mid_x = (start_x + end_x) // 2
    mid_y = (start_y + end_y) // 2

    points = []
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            distance = math.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2)
            points.append((x, y, distance))

    points.sort(key=lambda p: p[2])  # Sort points by distance from center

    for i in range(min(max_chunks_to_render, len(points))):
        x, y, _ = points[i]
        yield x, y
