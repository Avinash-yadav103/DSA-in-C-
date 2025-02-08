#include<iostream>
#include<vector>
using namespace std;

int removeDuplicates(vector<int>& nums) {
    int k = 0;
    int n = nums.size();
    for(int i=0;i<n-1;i++){ 
        if(nums[i]==nums[i+1]){
            continue;
        }
        nums[k++] = nums[i];
    }
    nums[k++] = nums[n-1]; 

    return k;
}

int main(){
    vector<int> nums = {0,0,1,1,1,2,2,3,3,4};
    int k = removeDuplicates(nums);
    cout << "The number of unique elements is: " << k << endl;
    cout << "The unique elements are: ";
    for(int i = 0; i < k; i++) {
        cout << nums[i] << " ";
    }
    cout << endl;

    return 0;
}