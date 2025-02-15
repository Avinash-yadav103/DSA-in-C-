#include <iostream>
#include <vector>

using namespace std;

class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        int s = 0;
        int e = nums.size() -1;
        int mid = s + (e-s)/2;

        while(s<e){
            if(nums[mid]==target){
                return mid;
            }
            if(nums[mid]>target){
                e = mid -1;
            }
            else{
                s = mid +1;
            }
            // if(nums[mid]==e){
            //     cout<<"hi";
            //     return mid +1;
            // }
            
        }
        return s;

    }
};


int main() {
    Solution solution;
    vector<int> nums = {1, 3, 5, 6};
    int target = 5;
    int result = solution.searchInsert(nums, target);
    cout << "The index is: " << result << endl;
    return 0;
}