#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result = {{}};
        for(int num: nums){
            int n = result.size(); 
            for( int i =0;i<n; i++){
                vector<int> newsubset = result[i];
                newsubset.push_back(num);
                result.push_back(newsubset);
            }
        }
        return result;
    }
};

int main() {
    Solution sol;
    vector<int> nums = {1, 2, 3};
    
    vector<vector<int>> result = sol.subsets(nums);
    
    cout << "All subsets:" << endl;
    for(const auto& subset : result) {
        cout << "[ ";
        for(int num : subset) {
            cout << num << " ";
        }
        cout << "]" << endl;
    }
    
    return 0;
}