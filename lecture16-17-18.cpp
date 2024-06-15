#include<iostream>
using namespace std;


void selectionSort(int arr[],int n){

    for(int i =0;i<n-1;i++){
        int minIndex = i;
        for(int j=i+1;j<n;j++){
            if(arr[j]<arr[minIndex]){
                minIndex = j;  //Ye loop se 
                //value nikal ke la rha haie
                //Value store bhi kr raha hai aage jane ke liye
                //Agar chota hua to store kr lega 
                //aur aage badh jaega
            }
        }
        swap(arr[minIndex],arr[i]);
    }
}

void bubbleSort(int arr[] ,int n){

    for(int i=1;i<n;i++){
        //for round 1 to n-1

        //optimazation
        bool swapped = false;
        for( int j=0;j<n-i;j++){
            // process element till n-i th index
            if(arr[j]>arr[j+1]){
                swap(arr[j],arr[j+1]);
                swapped = true;
                //agar swap hua hai kuch to loop
                // continue rahega
            }
            
        }
        if(swapped==false){
            break;
        }
    }
}

void insertionSort(int arr[] ,int n){
    
    for(int i= 1;i<n;i++){
        int temp = arr[i];
        int j =i-1;
        for (;j>=0;j--){
            if(arr[j]>temp){
                arr[j+1] = arr[j];  
            }
            else{
                break;
            }
        }
        arr[j+1] =temp;
    }
}

void printingArray(int arr[], int n){
    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;
}

int main(){

    int qw[5] = {64,25,12,22,11};
    selectionSort(qw,5);
    printingArray(qw,5);
    int kw[5] = {65,26,5,62,11};
    bubbleSort(kw,5);
    printingArray(kw,5);
    int cw[5] = {65,25,12,22,11};
    insertionSort(cw,5);
    printingArray(cw,5);

    return 0;
}