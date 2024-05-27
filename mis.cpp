#include<iostream>
using namespace std;

int main(){
    // int a ,b =1;
    // a =10;
    // if(++a){
    //     cout<<b;

    // }
    // else{
    //     cout<<++b;
    // }

    //Fibonacci series
    int n;
    cin>>n;
    int sum = 0;
    int a = 0;
    int b = 1;
    for(int i = 0; i<=n;i++){
        sum = a+b;
        cout<<sum<<" ";
        a=b;
        b = sum;
    }


    
}