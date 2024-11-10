#include<iostream>
using namespace std;

void print(int *p){
    cout<<p<<endl;
    cout<<*p<<endl;
}

void update(int *p){
    p=p+1;
    cout<<"inside "<<p<<endl;
    *p = *p+1;
}

int getSum(int arr[],int n){

    cout<<"Size: "<<sizeof(arr)<<endl;
    int sum=0;
    for(int i=0;i<n;i++){
        sum+=arr[i];
    }

    return sum;
}

int main (){
    // int arr[10] = {2,3,4};

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

    // int *ptr = &arr[0];
    // cout<<ptr<<endl;
    // ptr = ptr +1;
    // cout<<ptr<<endl;


    // Character Arrays
    // int arr[5] = {1,2,3,4,5};
    // char ch[6] = "abcde";

    // cout<<arr<<endl;
    // cout<<ch<<endl;

    // char *ptr = &ch[0];
    // cout<<ptr;

    // char temp = 'z';
    // char*p = &temp;
    // cout<<p;

    int value = 5;
    int *p = &value;
    print(p);



    int arr[5] = {1,2,3,4,5};
    cout<<"Sum of array: "<<getSum(arr,5);


    return 0;
}