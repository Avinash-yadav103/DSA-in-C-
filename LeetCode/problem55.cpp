#include <iostream>
#include <vector>
using namespace std;

bool canJump(vector<int>& nums) {

    int jump = 0;
    for (int i = 0; i < nums.size(); ++i) {
        if (i > jump) {
            return false;
        }
        jump = max(jump, i + nums[i]);
        if (jump >= nums.size() - 1) {
            return true;
        }
    }
    return false;
}

int main() {
    vector<int> nums = {2, 3, 1, 1, 4}; // Example input
    if (canJump(nums)) {
        cout << "Can jump to the last index." << endl;
    } else {
        cout << "Cannot jump to the last index." << endl;
    }
    return 0;
}