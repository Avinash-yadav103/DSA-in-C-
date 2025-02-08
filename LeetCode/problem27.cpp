#include<iostream>
#include<vector>
using namespace std;

int removeElement(vector<int>& nums, int val) {
    int n = nums.size();
    int k = 0;
    for(int i=0;i<n;i++){
        if(nums[i]!=val){
            nums[k] = nums[i];
            k++;
        }
    }
    return k;
}

int main() {
    vector<int> nums = {3, 2, 2, 3};
    int val = 3;
    int newLength = removeElement(nums, val);

    cout << "New length: " << newLength << endl;
    cout << "Modified array: ";
    for (int i = 0; i < newLength; i++) {
        cout << nums[i] << " ";
    }
    cout << endl;

    return 0;
}