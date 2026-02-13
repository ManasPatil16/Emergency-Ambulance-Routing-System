"""
Mini Project: Emergency Ambulance Routing System

AI Concepts Used:
UNIT I   : Agent, Environment, State Space
UNIT II  : BFS (Uninformed), A* (Informed), Heuristic
UNIT III : Adversarial Environment (Traffic Blocks)
"""

import heapq
import random
from collections import deque


# ==========================================================
# UNIT I – ENVIRONMENT
# ==========================================================

class CityMap:
    """Grid environment"""
    def __init__(self, size):
        self.size = size
        self.blocked = set()

    def is_valid(self, pos):
        x, y = pos
        return (0 <= x < self.size and
                0 <= y < self.size and
                pos not in self.blocked)


# ==========================================================
# UNIT I – AGENT
# ==========================================================

class AmbulanceAgent:
    """Goal based agent"""
    def __init__(self, start, hospital):
        self.start = start
        self.hospital = hospital


# ==========================================================
# MOVEMENTS
# ==========================================================

def neighbors(pos):
    x, y = pos
    return [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]


# ==========================================================
# UNIT II – BFS SEARCH
# ==========================================================

def bfs(city, start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        if current in visited:
            continue
        visited.add(current)

        for n in neighbors(current):
            if city.is_valid(n):
                queue.append((n, path + [n]))

    return None


# ==========================================================
# UNIT II – A* SEARCH
# ==========================================================

def heuristic(a, b):
    """Manhattan distance heuristic"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(city, start, goal):
    heap = []
    heapq.heappush(heap, (0, start, [start]))
    visited = set()

    while heap:
        f, current, path = heapq.heappop(heap)

        if current == goal:
            return path

        if current in visited:
            continue
        visited.add(current)

        for n in neighbors(current):
            if city.is_valid(n):
                g = len(path)
                h = heuristic(n, goal)
                heapq.heappush(heap, (g+h, n, path + [n]))

    return None


# ==========================================================
# UNIT III – ADVERSARIAL TRAFFIC
# ==========================================================

def add_traffic(city, count=5):
    while len(city.blocked) < count:
        x = random.randint(0, city.size-1)
        y = random.randint(0, city.size-1)
        if (x, y) not in [(0,0), (city.size-1, city.size-1)]:
            city.blocked.add((x, y))


# ==========================================================
# DISPLAY FUNCTIONS
# ==========================================================

def print_header():
    print("\n==============================")
    print(" EMERGENCY AMBULANCE SYSTEM")
    print("==============================")


def print_details(start, goal, blocked):
    print("\nPatient Location  :", start)
    print("Hospital Location :", goal)
    print("\nBlocked Roads (Traffic):", blocked)


def print_path_result(name, path):
    print("\n--------------------------------")
    print(f"Using {name} Search (Unit II)")
    print("--------------------------------")

    if path:
        route = " → ".join(str(p) for p in path)
        print("Route:")
        print(route)
        print("\nTotal Steps =", len(path) - 1)
    else:
        print("No path available!")


def print_city(city, path, start, goal):
    print("\nCity Map:\n")
    for i in range(city.size):
        for j in range(city.size):
            if (i, j) == start:
                print("A", end=" ")
            elif (i, j) == goal:
                print("H", end=" ")
            elif (i, j) in city.blocked:
                print("X", end=" ")
            elif path and (i, j) in path:
                print("*", end=" ")
            else:
                print(".", end=" ")
        print()


# ==========================================================
# MAIN
# ==========================================================

def main():
    size = 7
    city = CityMap(size)

    start = (0, 0)
    hospital = (size-1, size-1)

    agent = AmbulanceAgent(start, hospital)

    # adversary
    add_traffic(city)

    print_header()
    print_details(start, hospital, city.blocked)

    # BFS
    path_bfs = bfs(city, agent.start, agent.hospital)
    print_path_result("BFS", path_bfs)
    print_city(city, path_bfs, start, hospital)

    # A*
    path_astar = astar(city, agent.start, agent.hospital)
    print_path_result("A*", path_astar)
    print_city(city, path_astar, start, hospital)


if __name__ == "__main__":
    main()
