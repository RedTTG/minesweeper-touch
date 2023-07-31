import math


def render_spiral(start_x, start_y, end_x, end_y, max_chunks_to_render):
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2

    direction = 1  # 0: right, 1: down, 2: left, 3: up
    distance = 1
    step_count = 0

    x, y = mid_x, mid_y

    max_chunks_to_render = int(math.ceil(math.sqrt(max_chunks_to_render))) ** 2

    for _ in range(max_chunks_to_render):
        # if start_x <= x < end_x and start_y <= y < end_y:
        yield x, y, False

        if step_count == distance:
            step_count = 0
            if direction in [0, 2]:
                distance += 1

            direction = (direction + 1) % 4

        if direction == 0:
            x += 1
        elif direction == 1:
            y += 1
        elif direction == 2:
            x -= 1
        elif direction == 3:
            y -= 1

        step_count += 1

        if x < start_x or x >= end_x:  # and start_y > y >= end_y:
            direction = [
                1,
                2,
                -1,
                0,
            ][direction]

        if x < start_x:
            x += 1
            y -= distance + 2

        if x >= end_x:
            x -= 1
            y += distance + 1

