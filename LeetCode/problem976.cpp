#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int largestPerimeter(vector<int>& nums) {
        sort(nums.begin(), nums.end(), greater<int>());
        for(int i=0;i< nums.size()-2;i++){
            if(nums[i+1] + nums[i+2] > nums[i]){
                return nums[i] + nums[i+1] + nums[i+2];
            }
        }
        return 0;
    }
};

int main() {
    Solution sol;
    vector<int> nums = {2, 1, 2};  // example input
    int result = sol.largestPerimeter(nums);
    cout << "Largest perimeter: " << result << endl;
    
    // Test another example
    vector<int> nums2 = {1, 2, 1, 10};
    result = sol.largestPerimeter(nums2);
    cout << "Largest perimeter: " << result << endl;
    
    return 0;
}