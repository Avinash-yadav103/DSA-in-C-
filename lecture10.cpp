#include<iostream>
using namespace std;


void swapAlternate(int arr[],int size){

    for(int i=0;i<size;i=i+2){
        if(i+1<size){
            swap(arr[i],arr[i+1]);
        }
        
    }
    
}

void PrintingArray(int arr[],int size){
    for(int i=0;i<size;i++){
        cout<<arr[i]<<" ";
    }
}

int gettingUniqueNum(int arr[], int size){
    int ans = 0;
    for(int i=0;i<size;i++){
        ans = ans^arr[i];
    }

    return ans;
}

int repeatingNum(int arr[], int size){
    int x = 0;
    for(int i =0;i<size;i++){
        for(int j=0;j<size;j++){
            if(arr[i]==arr[j]){
                x=arr[i];             
            }
            else{
                x=0;
            }
            
        }
    }
    
    return x;
}


int main(){


    // int even[8]={5,2,9,4,7,6,1,0};
    // int odd[5] = {11,33,9,76,43};
    // int mirror[7] ={5,3,4,4,5,3,1};
    // swapAlternate(even,8);
    // swapAlternate(odd,5);
    // PrintingArray(even,8);
    // cout<<endl;
    // PrintingArray(odd,5);
    // cout<<endl;
    // cout<<gettingUniqueNum(mirror, 7)<<endl;
    // PrintingArray(mirror,7);
    int arr[5] ={5,2,3,4,7};
    cout<<repeatingNum(arr,5);

    return 0;
}