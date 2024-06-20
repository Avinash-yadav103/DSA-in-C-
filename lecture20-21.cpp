#include<iostream>
#include<vector>
using namespace std;

void reverseArray(int arr[],int n){
    int s =0;
    int e = n-1;
    while(s < e){
        swap(arr[s],arr[e]);
        s++;
        e--;
    }
}

vector<int> reverseVector(vector<int> v){
    int s =0;
    int e = v.size()-1;
    while(s <=e){
        swap(v[s],v[e]);
        s++;
        e--;
    }
    return v;
}

void printingArray(int arr[], int n){
    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
}

void printingVec(vector<int> v){
    for(int i=0;i<v.size();i++){
        cout<<v[i]<<" ";
    }
}

// mergesortedArray using vectors
// vector<int> mergesortedArray(vector<int> a,vector<int> b){

// }

// mergesortedArray using arrays
void mergesortedArray(int arr1[], int n ,int arr2[], int m,int arr3[]){

    int i = 0;
    int j = 0;
    int k = 0;
    while(i<n && j<m){
        if(arr1[i]>arr2[j]){
            arr3[k] = arr2[j];  //Optimize by writing k++ in place of k and same for j
            j++;    //Then remove ++ from here
            k++;

        }
        else{
            arr3[k] = arr1[i];  //Optimize by writing k++ in place of k and same for i
            i++;    //Then remove ++ from here
            k++;
        }
    }

    //Printing remaining elements of arr1
    while(i<n){
        arr3[k]=arr1[i];
        i++;k++;
    }
    //Printing remaining elements of arr2
    while(j<m){
        arr3[k]=arr1[i];
        i++;k++;
    }
}

// Leetcode folder me
// vector<int> mergesortedVectors(){
    
// }

void moveZeroes(int nums[],int n){
    int i = 0;
    int j = 0;
    while(j<n){
        if(nums[j]!=0){
            swap(nums[i],nums[j]);
            i++;
        }
        j++;
    }
}

vector<int> rotate(vector<int>& nums, int k){

    for(int i =0; i<nums.size()-1;i++){
        swap(nums[i],nums[k]);
        if(k<nums.size()){
            k++;
        }
        else{
            break;
        }
    }
    return nums;
}

int main(){
    // int arr[] = {1,2,3,4,5};
    // reverseArray(arr,5);
    // vector<int> arr = {1,2,3,4,5};
    // // arr.push_back(6);
    // vector<int> ans = reverseVector(arr);
    // printingVec(ans);

    // int array1[] = {1,3,5,7,9};
    // int array2[] = {2,4,6,8};

    // int array3[9];
    // mergesortedArray(array1,5,array2,4,array3);
    // printingArray(array3,9);
    // cout<<"hellp";

    // int arr[] ={0,1,0,4,0,3};
    // moveZeroes(arr,6);
    // printingArray(arr,6);

    vector<int> nums = {5,9,7,6,3};
    rotate(nums,2);
    // vector<int> ans = nums;
    printingVec(nums);
}



