import heapq

def a_star(matrix, start, target):
    rows, cols = len(matrix), len(matrix[0])

    def is_valid(x, y):
        """Check if all four required cells are valid."""
        return (
            0 <= x < rows and 0 <= y < cols and matrix[x][y] != 'wall' and
            0 <= x + 1 < rows and matrix[x + 1][y] != 'wall' and
            0 <= y + 1 < cols and matrix[x][y + 1] != 'wall' and
            0 <= x + 1 < rows and 0 <= y + 1 < cols and matrix[x + 1][y + 1] != 'wall'
        )

    def heuristic(a, b):
        """Calculate Manhattan distance."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Directions: Up, Down, Left, Right
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]

    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, position)
    came_from = {}  # To reconstruct the path

    g_score = {start: 0}
    f_score = {start: heuristic(start, target)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == target:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if is_valid(neighbor[0], neighbor[1]):
                tentative_g_score = g_score[current] + 1  # All moves cost 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, target)

                    if neighbor not in [pos for _, pos in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return empty path if no path exists