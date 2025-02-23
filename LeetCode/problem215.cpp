#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
    public:
        int findKthLargest(vector<int>& nums, int k) {
            sort(nums.begin(), nums.end());
            return nums[nums.size() - k];
        }
};

int main() {
    Solution solution;
    vector<int> nums = {3, 2, 1, 5, 6, 4};
    int k = 2;
    cout << "The " << k << "th largest element is " << solution.findKthLargest(nums, k) << endl;
    return 0;
}