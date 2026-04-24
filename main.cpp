#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <algorithm>

using namespace std;

struct Edge {
    int to;
    string mode;
    double time;
    double cost;
    double comfort;
};

struct Route {
    vector<int> stops;
    vector<string> modes;
    double totalTime = 0;
    double totalCost = 0;
    double averageComfort = 0;
    int transfers = 0;
    double adjustedComfort = 0;
    double zScore = 0;
};

vector<string> stopNames = {
    "Dorm",             // 0
    "Campus",           // 1
    "Mong Kok",         // 2
    "Sham Shui Po",     // 3
    "Kowloon Tong",     // 4
    "Sha Tin",          // 5
    "Tai Po",           // 6
    "Sai Kung",         // 7
    "Tsim Sha Tsui",    // 8
    "Central",          // 9
    "Admiralty",        // 10
    "Wan Chai",         // 11
    "Causeway Bay"      // 12
};

vector<vector<Edge>> graph(stopNames.size());

void addUndirectedEdge(int a, int b, const string& mode, double time, double cost, double comfort) {
    graph[a].push_back({b, mode, time, cost, comfort});
    graph[b].push_back({a, mode, time, cost, comfort});
}

void buildGraph() {
    addUndirectedEdge(0, 1, "Walk", 8, 0, 6);          // Dorm - Campus
    addUndirectedEdge(0, 2, "Bus", 15, 5.5, 4);        // Dorm - Mong Kok
    addUndirectedEdge(0, 3, "Walk", 12, 0, 5);         // Dorm - Sham Shui Po
    addUndirectedEdge(1, 4, "Walk", 10, 0, 6);         // Campus - Kowloon Tong
    addUndirectedEdge(1, 5, "Bus", 20, 5.5, 5);        // Campus - Sha Tin
    addUndirectedEdge(1, 6, "Bus", 28, 7.0, 5);        // Campus - Tai Po
    addUndirectedEdge(3, 2, "Walk", 6, 0, 5);          // Sham Shui Po - Mong Kok
    addUndirectedEdge(2, 4, "MTR", 8, 5.0, 7);         // Mong Kok - Kowloon Tong
    addUndirectedEdge(2, 8, "MTR", 7, 4.8, 7);         // Mong Kok - Tsim Sha Tsui
    addUndirectedEdge(2, 12, "Bus", 20, 8.5, 4);       // Mong Kok - Causeway Bay
    addUndirectedEdge(4, 5, "MTR", 14, 6.5, 7);        // Kowloon Tong - Sha Tin
    addUndirectedEdge(4, 7, "Bus", 25, 8.0, 5);        // Kowloon Tong - Sai Kung
    addUndirectedEdge(5, 6, "MTR", 11, 5.5, 7);        // Sha Tin - Tai Po
    addUndirectedEdge(5, 7, "Bus", 24, 8.5, 5);        // Sha Tin - Sai Kung
    addUndirectedEdge(6, 7, "Bus", 27, 9.0, 5);        // Tai Po - Sai Kung
    addUndirectedEdge(8, 9, "Bus", 10, 6.0, 6);        // Tsim Sha Tsui - Central
    addUndirectedEdge(8, 11, "MTR", 12, 6.0, 7);       // Tsim Sha Tsui - Wan Chai
    addUndirectedEdge(9, 10, "Walk", 5, 0, 7);         // Central - Admiralty
    addUndirectedEdge(10, 11, "Walk", 6, 0, 7);        // Admiralty - Wan Chai
    addUndirectedEdge(11, 12, "MTR", 6, 4.5, 8);       // Wan Chai - Causeway Bay
}

void dfsAllRoutes(int current, int destination, vector<bool>& visited,
                  vector<int>& pathStops, vector<string>& pathModes,
                  double totalTime, double totalCost, double comfortSum, int edgeCount,
                  vector<Route>& allRoutes) {
    if (current == destination) {
        Route r;
        r.stops = pathStops;
        r.modes = pathModes;
        r.totalTime = totalTime;
        r.totalCost = totalCost;
        r.averageComfort = (edgeCount == 0) ? 0 : comfortSum / edgeCount;
        r.transfers = (edgeCount <= 0) ? 0 : edgeCount - 1;
        r.adjustedComfort = r.averageComfort - 0.5 * r.transfers;
        if (r.adjustedComfort < 0) r.adjustedComfort = 0;
        allRoutes.push_back(r);
        return;
    }

    for (const Edge& e : graph[current]) {
        if (!visited[e.to]) {
            visited[e.to] = true;
            pathStops.push_back(e.to);
            pathModes.push_back(e.mode);

            dfsAllRoutes(
                e.to, destination, visited,
                pathStops, pathModes,
                totalTime + e.time,
                totalCost + e.cost,
                comfortSum + e.comfort,
                edgeCount + 1,
                allRoutes
            );

            pathStops.pop_back();
            pathModes.pop_back();
            visited[e.to] = false;
        }
    }
}

double normalizeSmallerBetter(double value, double minVal, double maxVal) {
    if (maxVal == minVal) return 100.0;
    return 100.0 * (maxVal - value) / (maxVal - minVal);
}

double normalizeLargerBetter(double value, double minVal, double maxVal) {
    if (maxVal == minVal) return 100.0;
    return 100.0 * (value - minVal) / (maxVal - minVal);
}

void computeZScores(vector<Route>& routes, double wCost, double wTime, double wComfort) {
    double minCost = routes[0].totalCost, maxCost = routes[0].totalCost;
    double minTime = routes[0].totalTime, maxTime = routes[0].totalTime;
    double minComfort = routes[0].adjustedComfort, maxComfort = routes[0].adjustedComfort;

    for (const Route& r : routes) {
        minCost = min(minCost, r.totalCost);
        maxCost = max(maxCost, r.totalCost);
        minTime = min(minTime, r.totalTime);
        maxTime = max(maxTime, r.totalTime);
        minComfort = min(minComfort, r.adjustedComfort);
        maxComfort = max(maxComfort, r.adjustedComfort);
    }

    for (Route& r : routes) {
        double costScore = normalizeSmallerBetter(r.totalCost, minCost, maxCost);
        double timeScore = normalizeSmallerBetter(r.totalTime, minTime, maxTime);
        double comfortScore = normalizeLargerBetter(r.adjustedComfort, minComfort, maxComfort);

        r.zScore = (wCost * costScore + wTime * timeScore + wComfort * comfortScore) / 100.0;
    }
}

void printStops() {
    cout << "\nAvailable stops:\n";
    for (int i = 0; i < (int)stopNames.size(); i++) {
        cout << setw(2) << i + 1 << ". " << stopNames[i] << '\n';
    }
}

int getValidStopChoice(const string& prompt) {
    int choice;
    while (true) {
        cout << prompt;
        cin >> choice;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(10000, '\n');
            cout << "Invalid input. Please enter a number.\n";
            continue;
        }
        if (choice >= 1 && choice <= (int)stopNames.size()) {
            return choice - 1;
        }
        cout << "Out of range. Please enter a number between 1 and " << stopNames.size() << ".\n";
    }
}

void getWeights(double& wCost, double& wTime, double& wComfort) {
    int option;
    while (true) {
        cout << "Choose weight setting:\n";
        cout << "1. Default (Cost 35, Time 40, Comfort 25)\n";
        cout << "2. Custom input\n";
        cout << "Enter 1 or 2: ";
        cin >> option;

        if (cin.fail()) {
            cin.clear();
            cin.ignore(10000, '\n');
            cout << "Invalid input. Please enter 1 or 2.\n";
            continue;
        }

        if (option == 1) {
            wCost = 35;
            wTime = 40;
            wComfort = 25;
            break;
        } else if (option == 2) {
            while (true) {
                cout << "\nEnter weights for each category.\n";
                cout << "Range for each: 0 to 100\n";
                cout << "The total must equal 100.\n";

                cout << "Cost weight: ";
                cin >> wCost;
                cout << "Time weight: ";
                cin >> wTime;
                cout << "Comfort weight: ";
                cin >> wComfort;

                if (cin.fail()) {
                    cin.clear();
                    cin.ignore(10000, '\n');
                    cout << "Invalid input. Please enter numbers only.\n\n";
                    continue;
                }

                if (wCost < 0 || wTime < 0 || wComfort < 0 ||
                    wCost > 100 || wTime > 100 || wComfort > 100) {
                    cout << "Each weight must be between 0 and 100.\n\n";
                    continue;
                }

                if (wCost + wTime + wComfort != 100) {
                    cout << "The total is " << (wCost + wTime + wComfort)
                         << ", not 100. Please try again.\n\n";
                    continue;
                }
                break;
            }
            break;
        } else {
            cout << "Please enter only 1 or 2.\n";
        }
    }
}

void printRouteDetails(const Route& route, int rank) {
    cout << "\n===== Route Rank #" << rank << " =====\n";
    cout << fixed << setprecision(2);
    cout << "Z-score: " << route.zScore << '\n';
    cout << "Total time: " << route.totalTime << " minutes\n";
    cout << "Total cost: HKD " << route.totalCost << '\n';
    cout << "Average comfort: " << route.averageComfort << "/10\n";
    cout << "Transfers: " << route.transfers << '\n';
    cout << "Adjusted comfort: " << route.adjustedComfort << "/10\n\n";

    cout << "Navigation plan:\n";
    for (int i = 0; i < (int)route.modes.size(); i++) {
        cout << i + 1 << ". " << stopNames[route.stops[i]]
             << " -> " << stopNames[route.stops[i + 1]]
             << " by " << route.modes[i] << '\n';
    }

    cout << "\nRoute summary:\n";
    for (int i = 0; i < (int)route.stops.size(); i++) {
        cout << stopNames[route.stops[i]];
        if (i != (int)route.stops.size() - 1) cout << " -> ";
    }
    cout << '\n';
}

int main() {
    buildGraph();

    while (true) {
        double wCost, wTime, wComfort;
        getWeights(wCost, wTime, wComfort);

        printStops();
        int start = getValidStopChoice("\nEnter starting stop number: ");
        int destination = getValidStopChoice("Enter destination stop number: ");

        if (start == destination) {
            cout << "\nStarting point and destination are the same.\n";
            cout << "Total time: 0 minutes\n";
            cout << "Total cost: HKD 0\n";
            cout << "Route: " << stopNames[start] << '\n';
        } else {
            vector<Route> allRoutes;
            vector<bool> visited(stopNames.size(), false);
            vector<int> pathStops;
            vector<string> pathModes;

            visited[start] = true;
            pathStops.push_back(start);

            dfsAllRoutes(start, destination, visited, pathStops, pathModes,
                         0, 0, 0, 0, allRoutes);

            if (allRoutes.empty()) {
                cout << "\nNo route found.\n";
            } else {
                computeZScores(allRoutes, wCost, wTime, wComfort);

                sort(allRoutes.begin(), allRoutes.end(), [](const Route& a, const Route& b) {
                    return a.zScore > b.zScore;
                });

                int topCount = min(5, (int)allRoutes.size());
                cout << "\n===== Top " << topCount << " Route Recommendations =====\n";
                for (int i = 0; i < topCount; i++) {
                    printRouteDetails(allRoutes[i], i + 1);
                }
                cout << "\nTotal possible routes checked: " << allRoutes.size() << '\n';
            }
        }

        string rerunChoice;
        while (true) {
            cout << "\nDo you want to run again? (y/n): ";
            cin >> rerunChoice;

            if (cin.fail()) {
                cin.clear();
                cin.ignore(10000, '\n');
                cout << "Invalid input. Please enter y or n.\n";
                continue;
            }

            transform(rerunChoice.begin(), rerunChoice.end(), rerunChoice.begin(), ::tolower);
            if (rerunChoice == "y" || rerunChoice == "yes") {
                cout << '\n';
                break;
            }
            if (rerunChoice == "n" || rerunChoice == "no") {
                return 0;
            }
            cout << "Please enter y or n.\n";
        }
    }

    return 0;
}
