# COMP1110 Final Project (Topic B) — Python Version

A Python route recommendation program that finds possible paths between locations and ranks them using a weighted score based on:
- Cost
- Travel time
- Comfort

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

## Sample Test Cases

The project includes sample tests in [tests/test_main.py](tests/test_main.py). Each case is documented with its purpose so the expected behavior is clear.

| Test case | Purpose | What it checks |
|---|---|---|
| `test_build_graph_populates_expected_number_of_edges` | Confirms the sample transport network is built correctly | The graph contains the expected number of edges after setup |
| `test_get_valid_stop_choice_retries_until_valid_input` | Confirms invalid stop inputs are rejected | Non-numeric and out-of-range values are retried until valid input is entered |
| `test_get_weights_default_selection` | Confirms the default preset is correct | Option 1 returns the documented `35/40/25` split |
| `test_get_weights_custom_selection` | Confirms custom weights are accepted | A valid custom set that sums to 100 is returned unchanged |
| `test_compute_z_scores_prefers_better_route` | Confirms route ranking behavior | A route with better metrics receives a higher score |
| `test_main_handles_same_start_and_destination` | Confirms the CLI handles a zero-distance trip | The program prints the same-start/same-destination message and does not fail |

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

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



## Key Implementation Notes

1. **Data Structures**: Dataclasses used for clean code with type safety
2. **Input Handling**: Robust CLI input validation with retry loops for invalid values
3. **Graph Representation**: Adjacency list using Python lists for efficient traversal
4. **Formatting**: f-strings with `.2f` format specifiers for consistent decimal display
5. **Sorting**: Lambda functions for flexible route ranking by score

## Verification

The implementation correctly handles:
- Graph topology (13 stops with weighted edges)
- DFS pathfinding algorithm to locate all possible routes
- Scoring algorithm using min/max normalization with weighted Z-scores
- Top-5 route display logic
- Input validation and user prompts
- Restart loop behavior
