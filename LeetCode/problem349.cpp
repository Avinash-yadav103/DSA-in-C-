#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> ans;
        unordered_set<int> nums2Set(nums2.begin(), nums2.end());
        for (int i : nums1) {
            if (nums2Set.count(i)) {
                ans.insert(i);
            }
        }
        return vector<int>(ans.begin(), ans.end());
    }
};

int main() {
    Solution solution;
    vector<int> nums1 = {1, 2, 2, 1};
    vector<int> nums2 = {2, 2};
    
    vector<int> result = solution.intersection(nums1, nums2);
    
    cout << "Intersection: ";
    for (int num : result) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}