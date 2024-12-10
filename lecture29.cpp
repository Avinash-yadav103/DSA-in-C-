#include <iostream>
#include <vector>
using namespace std;
void countPathsUtil(int u, int d, vector<vector<int>>& adjList, vector<bool>& visited, int& pathCount) {
visited[u] = true;
if (u == d) {
pathCount++;
} else {
for (int v : adjList[u]) {
if (!visited[v]) {
countPathsUtil(v, d, adjList, visited, pathCount);
}
}
}
visited[u] = false;
}
int countPaths(int V, vector<vector<int>>& adjList, int start, int target) {
vector<bool> visited(V, false);
int pathCount = 0;
countPathsUtil(start, target, adjList, visited, pathCount);
return pathCount;
}
int main() {
int stations, edges;
cin >> stations;
cin >> edges;
vector<vector<int>> adjList(stations);
for (int i = 0; i < edges; i++) {
int u, v;
cin >> u >> v;
adjList[u].push_back(v);
}
int start, target;
cin >> start;
cin >> target;
int paths = countPaths(stations, adjList, start, target);
cout << paths << endl;
return 0;
}