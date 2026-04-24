# COMP1110 Final Project (Topic B)

A C++ route recommendation program that finds possible paths between locations and ranks them using a weighted score based on:
- Cost
- Travel time
- Comfort

The program supports default weights or custom user-defined weights and displays the top route recommendations.

## Project Structure

- `main.cpp`: Main source file containing graph setup, route search, scoring, and CLI interaction.

## Requirements

- A C++ compiler with C++17 support (for example, `g++`)
- macOS, Linux, or Windows terminal environment

## Build

From the project root, compile with:

```bash
g++ -std=c++17 -Wall -Wextra -pedantic -g main.cpp -o main
```

## Run

After building:

```bash
./main
```

## Program Usage

When the program starts:
1. Choose weight mode:
   - `1` for default weights (Cost 35, Time 40, Comfort 25)
   - `2` for custom weights (must sum to 100)
2. Select start and destination stops from the displayed list.
3. Review top-ranked routes and route details.
4. Choose whether to run again.

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

## Notes for Submission

- This repository is configured to keep generated build artifacts out of version control.
- Main implementation is currently in a single file (`main.cpp`).


