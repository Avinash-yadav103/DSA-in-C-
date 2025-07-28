#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size(),m=matrix[0].size();
        //Taking transpose
        for(int i =0 ;i<n;i++){
            for(int j=i+1;j<n;j++){
                if(i!=j){
                    int temp = matrix[i][j];
                    matrix[i][j] = matrix[j][i];
                    matrix[j][i] = temp;
                }
            }
        }

        //Reversing the order
        for(int i=0;i<n;i++){
            for(int j=0;j<m/2;j++){
                int temp = matrix[i][j];
                    matrix[i][j] = matrix[i][n-j-1];
                    matrix[i][n-j-1] = temp;
            }
        }
    }
};

int main() {
    // Create a test matrix
    vector<vector<int>> matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    // Print original matrix
    cout << "Original matrix:" << endl;
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
    
    // Rotate the matrix
    Solution solution;
    solution.rotate(matrix);
    
    // Print rotated matrix
    cout << "\nRotated matrix:" << endl;
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
    
    return 0;
}