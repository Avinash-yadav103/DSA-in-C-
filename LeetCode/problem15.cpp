#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
using namespace std;

class Solution {
public:
    // Brute force approach
    vector<vector<int>> threeSumBruteForce(vector<int>& nums) {
        vector<vector<int>> ans;
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                for (int k = j + 1; k < n; k++) {
                    if (nums[i] + nums[j] + nums[k] == 0) {
                        vector<int> temp = {nums[i], nums[j], nums[k]};
                        sort(temp.begin(), temp.end());
                        if (find(ans.begin(), ans.end(), temp) == ans.end()) {
                            ans.push_back(temp);
                        }
                    }
                }
            }
        }
        return ans;
    }
    
        //Better than brute force
        // set <vector<int>>  st;

        // for(int i =0;i<nums.size();i++){
        //     set<int> hashset;
        //     for(int j=i+1;j<nums.size();j++){
        //         int third = - (nums[i]+nums[j]);
        //         if(hashset.find(third) != hashset.end()){  //If hash.find is not pointing till end value is in the set
        //             vector<int> temp = {nums[i] , nums[j] , third};
        //             sort(temp.begin(),temp.end());
        //             st.insert(temp);
        //         }
        //         hashset.insert(nums[j]);
        //     }
        // }

        // vector<vector<int>> ans(st.begin(),st.end());
        // return ans;

    // Optimized approach
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> ans;
        sort(nums.begin(), nums.end());
        for (int i = 0; i < nums.size(); i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int j = i + 1;
            int k = nums.size() - 1;
            while (j < k) {
                int sum = nums[i] + nums[j] + nums[k];
                if (sum < 0) {
                    j++;
                } else if (sum > 0) {
                    k--;
                } else {
                    vector<int> temp = {nums[i], nums[j], nums[k]};
                    ans.push_back(temp);
                    j++;
                    k--;
                    while (j < k && nums[j] == nums[j - 1]) j++;
                    while (j < k && nums[k] == nums[k + 1]) k--;
                }
            }
        }
        return ans;
    }
};

int main() {
    Solution solution;
    vector<int> nums = {-1, 0, 1, 2, -1, -4};
    
    // Brute force approach
    vector<vector<int>> resultBruteForce = solution.threeSumBruteForce(nums);
    cout << "Brute Force Result:" << endl;
    for (const auto& triplet : resultBruteForce) {
        for (int num : triplet) {
            cout << num << " ";
        }
        cout << endl;
    }

    // Optimized approach
    vector<vector<int>> resultOptimized = solution.threeSum(nums);
    cout << "Optimized Result:" << endl;
    for (const auto& triplet : resultOptimized) {
        for (int num : triplet) {
            cout << num << " ";
        }
        cout << endl;
    }

    return 0;
}
