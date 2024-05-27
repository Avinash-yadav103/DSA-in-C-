#include<iostream>
using namespace std;

int get_Max(int arr[],int size){
    // int x =0;
    int i;
    int max = arr[0];
    for(i=0;i<size;i++){
        if(arr[i]>max){
            max =arr[i];
        }
    }
    return max; 
}

int get_Min(int arr[],int size){
    // int x =0;
    int i;
    int min = arr[0];
    for(i=0;i<size;i++){
        if(arr[i]<min){
            min=arr[i];
        }
    }
    return min; 
}

int sumArray(int arr[], int size){
    int sum = 0;
    for(int i =0; i<size;i++){
        sum = sum + arr[i];
    }

    return sum;
}

bool linearSearch(int arr[],int size, int key){
    for(int i=0;i<size;i++){
        if(arr[i]==key){
            return true;
        }
    }
    return false;
}

void reverseArray(int arr[], int size){

    int start =0;
    int end =size-1;
    
    while(start<=end){
        swap(arr[start],arr[end]);
        start++;
        end--;
    }
    
}

int main(){
    int n;
    cin>>n;
    int arr[5];
    for(int i=0; i<n;i++){
        cout<<"Enter "<<i<<" number :";
        cin>>arr[i];
    }
    for(int i=0;i<n;i++){
        cout<<i<<" number is";
        cout<<arr[i]<<endl;
    }
    // cout<<"Maximum value of the array is"<<get_Max(arr,n);
    // cout<<"Minimum value of the array is"<<get_Min(arr,n);
    // cout<<"Sum of array is "<<sumArray(arr,n);
    linearSearch(arr,n,7);
    
    reverseArray(arr,n);
    
    return 0;
}

