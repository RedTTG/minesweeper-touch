import math
import heapq


def render_spiral(start_x, start_y, end_x, end_y, max_chunks_to_render):
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2

    def distance_from_center(x, y):
        # Calculate the distance of each point from the center along both x and y axes separately
        x_distance = abs(x - mid_x)
        y_distance = abs(y - mid_y)
        return max(x_distance, y_distance)

    points_heap = []
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            distance = distance_from_center(x, y)
            if len(points_heap) < max_chunks_to_render:
                heapq.heappush(points_heap, (-distance, x, y))
            else:
                heapq.heappushpop(points_heap, (-distance, x, y))

    for distance, x, y in sorted(points_heap):
        yield x, y, distance
