#include<iostream>
using namespace std;

int binarySearch(int arr[],int size,int key){
    int start =0;
    int end =size-1;
    
    int mid = start+(end-start)/2;

    while(start<=end){
        if(arr[mid]==key){
            return mid;
        }

        if(key>arr[mid]){
            start = mid+1;
        }
        else{
            end =mid-1;
        }
        mid = start+(end-start)/2;
    }

    return -1;
}


int main(){

    int even[6] = {};
    // int odd[5] = {};

    int search = binarySearch(even,6,10);
    cout<<"The index of key is "<<search;

    return 0;
}