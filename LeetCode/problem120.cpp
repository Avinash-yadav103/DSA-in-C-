#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int minimum = INT_MAX;
        vector<int> linear;
        int n = triangle.size();
        for(int i=n;i>0;i--){
            for(int j=n;j>1;j--){
                int minimum = min(triangle[i][j],triangle[i][j+1]);
                
            }
            linear.push_back(minimum);
        }
        int total_sum=0;
        for(int i=0;i<triangle.size();i++){
            total_sum += linear[i];
        }
        return total_sum;
    }
};
