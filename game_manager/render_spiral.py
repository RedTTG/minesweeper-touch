import math
import heapq

def render_spiral(start_x, start_y, end_x, end_y, max_chunks_to_render):
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2

    def distance_from_center(x, y):
        return max(abs(x - mid_x), abs(y - mid_y))

    points_heap = []
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            distance = distance_from_center(x, y)
            if len(points_heap) < max_chunks_to_render:
                heapq.heappush(points_heap, (-distance, x, y))
            else:
                heapq.heappushpop(points_heap, (-distance, x, y))

    for _, x, y in sorted(points_heap):
        yield x, y
