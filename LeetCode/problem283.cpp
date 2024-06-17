#include<iostream>
using namespace std;

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

int main(){

}