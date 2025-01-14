#include<iostream>
#include<vector>

using namespace std;

void merge(vector<int>& nums1, int m, vector<int>& nums2, int n){

    int i = 0;
    int j = 0;
    int k = 0;
        vector<int> v;
        v = nums1;
        while(i<n && j<m){
        if(v[i]>nums2[j]){
            nums1[k++] = nums2[j++];
        }
        else{
            // if(v[i]==0){
            //     i++;
            //     continue;
            // }
            nums1[k++] = v[i++];
        }}

        //Printing remaining elements of arr1
        while(i<n){
            // if(v[i]==0){
            //     i++;
            //     continue;
            // }
            nums1[k++]=v[i++];
        }
        //Printing remaining elements of arr2
        while(j<m){
            nums1[k++]=nums2[j++];
        }


}

vector<int> mergeTwosortedVec(vector<int>& nums1, int m, vector<int> nums2, int n){
    // int i =0;
    // int j= 0;
    // vector<int> v;
    // while(i<m && j<n){
    //     if(nums1[i]<nums2[j]){
    //         v.push_back(nums1[i]);
    //         i++;
    //     }
    //     else{
    //          v.push_back(nums2[j]);
    //          j++;
    //     }
    // }
    // while(i<n){
    //     v.push_back(nums1[i]);
    //     i++;
    // }
    // while(j<m){
    //     v.push_back(nums2[j]);
    //     j++;
    // }

    // return v;


    int i =0;
        int j= 0;
        vector<int> v = nums1;
        nums1.clear();
        while(i<m && j<n){
            if(v[i]<nums2[j]){
                nums1.push_back(v[i]);
                i++;
            }
            else{
                nums1.push_back(nums2[j]);
                j++;
            }
        }
        while(i<n){
            nums1.push_back(v[i]);
            i++;
        }
        while(j<m){
            nums1.push_back(nums2[j]);
            j++;
        }

    return nums1; 
}


void printingVec(vector<int> v){
    for(int i=0;i<v.size();i++){
        cout<<v[i]<<" ";
    }
}


int main(){
    
    vector<int> nums1 = {1,2,3,0,0,0};
    vector<int> nums2 = {2,5,6};
    // vector<int> v;

    vector<int> v = mergeTwosortedVec(nums1,3,nums2,3);
    printingVec(v);
    
    return 0;
}