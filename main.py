#!/usr/bin/env python3
"""
COMP1110 Final Project (Topic B) - Route Recommendation System

A route recommendation program that finds possible paths between locations 
and ranks them using a weighted score based on:
- Cost
- Travel time
- Comfort
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict
import sys


@dataclass
class Edge:
    """Represents a connection between two stops."""
    to: int
    mode: str
    time: float
    cost: float
    comfort: float


@dataclass
class Route:
    """Represents a complete route with metrics."""
    stops: List[int] = field(default_factory=list)
    modes: List[str] = field(default_factory=list)
    totalTime: float = 0.0
    totalCost: float = 0.0
    averageComfort: float = 0.0
    transfers: int = 0
    adjustedComfort: float = 0.0
    zScore: float = 0.0


STOP_NAMES = [
    "Dorm",             # 0
    "Campus",           # 1
    "Mong Kok",         # 2
    "Sham Shui Po",     # 3
    "Kowloon Tong",     # 4
    "Sha Tin",          # 5
    "Tai Po",           # 6
    "Sai Kung",         # 7
    "Tsim Sha Tsui",    # 8
    "Central",          # 9
    "Admiralty",        # 10
    "Wan Chai",         # 11
    "Causeway Bay"      # 12
]

# Adjacency list representation
graph: List[List[Edge]] = [[] for _ in range(len(STOP_NAMES))]


def add_undirected_edge(a: int, b: int, mode: str, time: float, cost: float, comfort: float) -> None:
    """Add an undirected edge to the graph."""
    graph[a].append(Edge(to=b, mode=mode, time=time, cost=cost, comfort=comfort))
    graph[b].append(Edge(to=a, mode=mode, time=time, cost=cost, comfort=comfort))


def build_graph() -> None:
    """Build the transportation graph with all routes."""
    add_undirected_edge(0, 1, "Walk", 8, 0, 6)          # Dorm - Campus
    add_undirected_edge(0, 2, "Bus", 15, 5.5, 4)        # Dorm - Mong Kok
    add_undirected_edge(0, 3, "Walk", 12, 0, 5)         # Dorm - Sham Shui Po
    add_undirected_edge(1, 4, "Walk", 10, 0, 6)         # Campus - Kowloon Tong
    add_undirected_edge(1, 5, "Bus", 20, 5.5, 5)        # Campus - Sha Tin
    add_undirected_edge(1, 6, "Bus", 28, 7.0, 5)        # Campus - Tai Po
    add_undirected_edge(3, 2, "Walk", 6, 0, 5)          # Sham Shui Po - Mong Kok
    add_undirected_edge(2, 4, "MTR", 8, 5.0, 7)         # Mong Kok - Kowloon Tong
    add_undirected_edge(2, 8, "MTR", 7, 4.8, 7)         # Mong Kok - Tsim Sha Tsui
    add_undirected_edge(2, 12, "Bus", 20, 8.5, 4)       # Mong Kok - Causeway Bay
    add_undirected_edge(4, 5, "MTR", 14, 6.5, 7)        # Kowloon Tong - Sha Tin
    add_undirected_edge(4, 7, "Bus", 25, 8.0, 5)        # Kowloon Tong - Sai Kung
    add_undirected_edge(5, 6, "MTR", 11, 5.5, 7)        # Sha Tin - Tai Po
    add_undirected_edge(5, 7, "Bus", 24, 8.5, 5)        # Sha Tin - Sai Kung
    add_undirected_edge(6, 7, "Bus", 27, 9.0, 5)        # Tai Po - Sai Kung
    add_undirected_edge(8, 9, "Bus", 10, 6.0, 6)        # Tsim Sha Tsui - Central
    add_undirected_edge(8, 11, "MTR", 12, 6.0, 7)       # Tsim Sha Tsui - Wan Chai
    add_undirected_edge(9, 10, "Walk", 5, 0, 7)         # Central - Admiralty
    add_undirected_edge(10, 11, "Walk", 6, 0, 7)        # Admiralty - Wan Chai
    add_undirected_edge(11, 12, "MTR", 6, 4.5, 8)       # Wan Chai - Causeway Bay


def dfs_all_routes(current: int, destination: int, visited: List[bool],
                   path_stops: List[int], path_modes: List[str],
                   total_time: float, total_cost: float, comfort_sum: float,
                   edge_count: int, all_routes: List[Route]) -> None:
    """Find all possible routes from current to destination using DFS."""
    if current == destination:
        r = Route()
        r.stops = path_stops.copy()
        r.modes = path_modes.copy()
        r.totalTime = total_time
        r.totalCost = total_cost
        r.averageComfort = 0 if edge_count == 0 else comfort_sum / edge_count
        r.transfers = 0 if edge_count <= 0 else edge_count - 1
        r.adjustedComfort = r.averageComfort - 0.5 * r.transfers
        if r.adjustedComfort < 0:
            r.adjustedComfort = 0
        all_routes.append(r)
        return

    for e in graph[current]:
        if not visited[e.to]:
            visited[e.to] = True
            path_stops.append(e.to)
            path_modes.append(e.mode)

            dfs_all_routes(
                e.to, destination, visited,
                path_stops, path_modes,
                total_time + e.time,
                total_cost + e.cost,
                comfort_sum + e.comfort,
                edge_count + 1,
                all_routes
            )

            path_stops.pop()
            path_modes.pop()
            visited[e.to] = False


def normalize_smaller_better(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value where smaller is better (0-100 scale)."""
    if max_val == min_val:
        return 100.0
    return 100.0 * (max_val - value) / (max_val - min_val)


def normalize_larger_better(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value where larger is better (0-100 scale)."""
    if max_val == min_val:
        return 100.0
    return 100.0 * (value - min_val) / (max_val - min_val)


def compute_z_scores(routes: List[Route], w_cost: float, w_time: float, w_comfort: float) -> None:
    """Compute weighted Z-scores for all routes."""
    if not routes:
        return

    min_cost = routes[0].totalCost
    max_cost = routes[0].totalCost
    min_time = routes[0].totalTime
    max_time = routes[0].totalTime
    min_comfort = routes[0].adjustedComfort
    max_comfort = routes[0].adjustedComfort

    for r in routes:
        min_cost = min(min_cost, r.totalCost)
        max_cost = max(max_cost, r.totalCost)
        min_time = min(min_time, r.totalTime)
        max_time = max(max_time, r.totalTime)
        min_comfort = min(min_comfort, r.adjustedComfort)
        max_comfort = max(max_comfort, r.adjustedComfort)

    for r in routes:
        cost_score = normalize_smaller_better(r.totalCost, min_cost, max_cost)
        time_score = normalize_smaller_better(r.totalTime, min_time, max_time)
        comfort_score = normalize_larger_better(r.adjustedComfort, min_comfort, max_comfort)

        r.zScore = (w_cost * cost_score + w_time * time_score + w_comfort * comfort_score) / 100.0


def print_stops() -> None:
    """Print all available stops."""
    print("\nAvailable stops:")
    for i, name in enumerate(STOP_NAMES):
        print(f"{i + 1:2d}. {name}")


def get_valid_stop_choice(prompt: str) -> int:
    """Get a valid stop choice from user input."""
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(STOP_NAMES):
                return choice - 1
            print(f"Out of range. Please enter a number between 1 and {len(STOP_NAMES)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_weights() -> Tuple[float, float, float]:
    """Get weight settings from user."""
    while True:
        print("Choose weight setting:")
        print("1. Default (Cost 35, Time 40, Comfort 25)")
        print("2. Custom input")
        try:
            option = int(input("Enter 1 or 2: "))
            if option == 1:
                return 35.0, 40.0, 25.0
            elif option == 2:
                while True:
                    print("\nEnter weights for each category.")
                    print("Range for each: 0 to 100")
                    print("The total must equal 100.")
                    try:
                        w_cost = float(input("Cost weight: "))
                        w_time = float(input("Time weight: "))
                        w_comfort = float(input("Comfort weight: "))

                        if w_cost < 0 or w_time < 0 or w_comfort < 0 or \
                           w_cost > 100 or w_time > 100 or w_comfort > 100:
                            print("Each weight must be between 0 and 100.\n")
                            continue

                        total = w_cost + w_time + w_comfort
                        if total != 100:
                            print(f"The total is {total}, not 100. Please try again.\n")
                            continue

                        return w_cost, w_time, w_comfort
                    except ValueError:
                        print("Invalid input. Please enter numbers only.\n")
            else:
                print("Please enter only 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")


def print_route_details(route: Route, rank: int) -> None:
    """Print detailed information about a route."""
    print(f"\n===== Route Rank #{rank} =====")
    print(f"Z-score: {route.zScore:.2f}")
    print(f"Total time: {route.totalTime:.2f} minutes")
    print(f"Total cost: HKD {route.totalCost:.2f}")
    print(f"Average comfort: {route.averageComfort:.2f}/10")
    print(f"Transfers: {route.transfers}")
    print(f"Adjusted comfort: {route.adjustedComfort:.2f}/10\n")

    print("Navigation plan:")
    for i, mode in enumerate(route.modes):
        print(f"{i + 1}. {STOP_NAMES[route.stops[i]]} -> {STOP_NAMES[route.stops[i + 1]]} by {mode}")

    print("\nRoute summary:")
    route_summary = " -> ".join(STOP_NAMES[stop] for stop in route.stops)
    print(route_summary)


def main() -> None:
    """Main program loop."""
    build_graph()

    while True:
        w_cost, w_time, w_comfort = get_weights()

        print_stops()
        start = get_valid_stop_choice("\nEnter starting stop number: ")
        destination = get_valid_stop_choice("Enter destination stop number: ")

        if start == destination:
            print("\nStarting point and destination are the same.")
            print("Total time: 0 minutes")
            print("Total cost: HKD 0")
            print(f"Route: {STOP_NAMES[start]}")
        else:
            all_routes: List[Route] = []
            visited = [False] * len(STOP_NAMES)
            path_stops: List[int] = []
            path_modes: List[str] = []

            visited[start] = True
            path_stops.append(start)

            dfs_all_routes(start, destination, visited, path_stops, path_modes,
                          0, 0, 0, 0, all_routes)

            if not all_routes:
                print("\nNo route found.")
            else:
                compute_z_scores(all_routes, w_cost, w_time, w_comfort)

                all_routes.sort(key=lambda r: r.zScore, reverse=True)

                top_count = min(5, len(all_routes))
                print(f"\n===== Top {top_count} Route Recommendations =====")
                for i in range(top_count):
                    print_route_details(all_routes[i], i + 1)

                print(f"\nTotal possible routes checked: {len(all_routes)}")

        while True:
            rerun_choice = input("\nDo you want to run again? (y/n): ").strip().lower()
            if rerun_choice in ("y", "yes"):
                print()
                break
            elif rerun_choice in ("n", "no"):
                return
            else:
                print("Please enter y or n.")


if __name__ == "__main__":
    main()
