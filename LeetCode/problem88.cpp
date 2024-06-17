#include<iostream>
#include<vector>

using namespace std;

void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {

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
        if(v[i]==0){
        i++;
                continue;
            }
            nums1[k++] = nums1[i++];
        }

        //Printing remaining elements of arr1
        while(i<n){
            if(v[i]==0){
                i++;
                continue;
            }
            nums1[k++]=v[i++];
        }
        //Printing remaining elements of arr2
        while(j<m){
            nums1[k++]=v[i++];
        }

}


int main();{

    // merge();
    // return 0;
}