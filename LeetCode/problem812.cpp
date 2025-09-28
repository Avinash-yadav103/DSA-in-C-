#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

class Solution {
public:
    double largestTriangleArea(vector<vector<int>>& points) {
        double max_area = 0.0;
        int n = points.size();
        for(int i =0;i<n-2;++i){
            for(int j = i+1;j<n-1;++j){
                for( int k = j+1;k<n;++k){
                    int x1 = points[i][0], y1 = points[i][1];
                    int x2 = points[j][0], y2 = points[j][1];
                    int x3 = points[k][0], y3 = points[k][1];
                    double area = 0.5 * abs(x1*(y2-y3)+ x2*(y3-y1) + x3*(y1-y2));
                    max_area = max(max_area,area);
                }
            }
        }
        return max_area;
    }
};

int main() {
    int n;
    cout << "Enter number of points: ";
    cin >> n;
    vector<vector<int>> points(n, vector<int>(2));
    cout << "Enter the points (x y):\n";
    for(int i = 0; i < n; ++i) {
        cin >> points[i][0] >> points[i][1];
    }
    Solution sol;
    double result = sol.largestTriangleArea(points);
    cout << "Largest Triangle Area: " << result << endl;
    return 0;
}