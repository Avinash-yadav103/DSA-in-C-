#include<iostream>
#include<vector>
using namespace std;

vector<int> rotate(vector<int>& nums, int k) {
    //  for(int i =0; i<nums.size()-1;i++){
    //         swap(nums[i],nums[++k]);
    //         // k++;
    //         if(k>nums.size()){
    //             k=0;
    //         }
    //     else{
    //         break;
    //     }
    // }

    vector<int> temp(nums.size());

    for(int i =0;i<nums.size();i++){
        temp[(i+k)%nums.size()] = nums[i];

    }
    nums = temp;
} 

void printingVec(vector<int> v){
    for(int i=0;i<v.size();i++){
        cout<<v[i]<<" ";
    }
}

int main(){

    vector<int> nums = {1,2,3,4,5,6};
    vector<int> ans = rotate(nums,3);
    printingVec(ans);

    return 0;
}