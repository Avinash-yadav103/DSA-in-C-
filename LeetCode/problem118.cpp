#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> generatePascalTriangle(int numRows) {
        // int n = numRows.size();
        vector<vector<int>> res;
        for(int i=0;i<=i+1;i++){
            for(int j=0;j<=numRows;j++){
                
            }
        }
        return res;
    }
    int main() {
        Solution solution;
        int numRows;
        cout << "Enter the number of rows for Pascal's Triangle: ";
        cin >> numRows;

        vector<vector<int>> result = solution.generatePascalTriangle(numRows);

        cout << "Pascal's Triangle:" << endl;
        for (const auto& row : result) {
            for (int num : row) {
                cout << num << " ";
            }
            cout << endl;
        }

        return 0;
    }
};