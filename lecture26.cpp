#include<iostream>
using namespace std;

int main (){
    int arr[10] = {2,3,4};

    // cout<<"Address of first memory block is "<<arr<<endl;
    // cout<<"Address of first memory block is "<<&arr[0]<<endl;

    // cout<<"Ex1: "<<*arr<<endl;
    // cout<<"Ex2: "<<*arr + 1<<endl;
    // cout<<"Ex3: "<<*(arr + 1)<<endl;

    // int temp[10];
    // cout<<sizeof(temp)<<endl;

    // int *ptr = &temp[0];
    // cout<<sizeof(ptr)<<endl;  
    // cout<<sizeof(*ptr)<<endl; // Ek block ki memory
    // cout<<sizeof(&ptr)<<endl; //Address store karne ke liye memory

    // 3rd
    // ERROR
    // arr = arr+1;

    int *ptr = &arr[0];
    cout<<ptr<<endl;
    ptr = ptr +1;
    cout<<ptr<<endl;



    return 0;
}