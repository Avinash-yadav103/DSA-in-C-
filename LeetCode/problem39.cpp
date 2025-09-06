#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void findCombination(int ind, int target, vector<int> &arr, vector<vector<int>> &ans, vector<int> &ds){
        if(ind == arr.size()){
            if(target==0){
                ans.push_back(ds);
            }
            return;
        }
        if(arr[ind] <= target){
            ds.push_back(arr[ind]);
            findCombination(ind, target- arr[ind], arr, ans, ds);
            ds.pop_back();
        }
        findCombination(ind+1, target, arr, ans, ds);
    }

    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> ans;
        vector<int> ds;
        findCombination(0, target, candidates, ans, ds);
        return ans;
    }
};

int main() {
    Solution sol;
    
    // Example test case
    vector<int> candidates = {2, 3, 6, 7};
    int target = 7;
    
    vector<vector<int>> result = sol.combinationSum(candidates, target);
    
    // Print the results
    cout << "Combinations that sum to " << target << ":" << endl;
    for (const auto& combination : result) {
        cout << "[ ";
        for (int num : combination) {
            cout << num << " ";
        }
        cout << "]" << endl;
    }
    
    return 0;
}