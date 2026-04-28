# COMP1110 Final Project (Topic B) — Python Version

A Python route recommendation program that finds possible paths between locations and ranks them using a weighted score based on:
- Cost
- Travel time
- Comfort

This is a direct translation of the C++ implementation maintaining 100% feature and behavior parity.

## Project Structure

- `main.py`: Main source file containing graph setup, route search, scoring, and CLI interaction

## Requirements

- Python 3.7+ (for dataclasses support)
- No external dependencies

## Run

From the project root, execute:

```bash
python3 main.py
```

Or on Windows:

```bash
python main.py
```

## Program Usage

When the program starts:
1. Choose weight mode:
   - `1` for default weights (Cost 35, Time 40, Comfort 25)
   - `2` for custom weights (must sum to 100)
2. Select start and destination stops from the displayed list
3. Review top-ranked routes and route details
4. Choose whether to run again

## Example Session (Short)

```text
Choose weight setting:
1. Default (Cost 35, Time 40, Comfort 25)
2. Custom input
Enter 1 or 2: 1

Available stops:
 1. Dorm
 2. Campus
...
Enter starting stop number: 1
Enter destination stop number: 13
```

## C++ → Python Mapping

| C++ | Python |
|-----|--------|
| `struct Edge` | `@dataclass Edge` |
| `struct Route` | `@dataclass Route` |
| `vector<string> stopNames` | Global list `STOP_NAMES` |
| `vector<vector<Edge>> graph` | Global list `graph: List[List[Edge]]` |
| `addUndirectedEdge()` | `add_undirected_edge()` |
| `buildGraph()` | `build_graph()` |
| `dfsAllRoutes()` | `dfs_all_routes()` |
| `normalizeSmallerBetter()` | `normalize_smaller_better()` |
| `normalizeLargerBetter()` | `normalize_larger_better()` |
| `computeZScores()` | `compute_z_scores()` |
| `printStops()` | `print_stops()` |
| `getValidStopChoice()` | `get_valid_stop_choice()` |
| `getWeights()` | `get_weights()` |
| `printRouteDetails()` | `print_route_details()` |
| `main()` | `main()` |

## Key Implementation Notes

1. **Data Structures**: Dataclasses used instead of structs for cleaner code with type safety
2. **Input Handling**: Python's `input()` replaces C++'s `cin`, with built-in exception handling for type conversion errors
3. **List Operations**: Python lists replace C++ vectors; copying used where needed (e.g., in DFS backtracking)
4. **Formatting**: `f-strings` and `.2f` format specifiers replicate C++'s `fixed` + `setprecision(2)`
5. **String Handling**: Python's `.lower()` and `.strip()` replace C++'s `transform()` and stream operations
6. **Sorting**: Lambda function replaces C++'s comparison functor

## Differences from C++

1. **Error Handling**: Python uses exceptions (`ValueError`) for invalid input instead of C++'s `cin.fail()`
2. **No explicit type casting**: Python handles type conversions implicitly
3. **Memory Management**: Python's automatic garbage collection vs. C++'s stack/heap management
4. **Floating-point representation**: Minor precision differences possible due to Python vs. C++ floating-point implementations

## Verification

The Python version maintains identical behavior to the C++ version:
- Same graph topology (13 stops, identical edges)
- Same DFS pathfinding algorithm
- Same scoring algorithm (min/max normalization with weighted Z-score)
- Same top-5 route display logic
- Same input validation and user prompts
- Same restart loop behavior
