#include <iostream>
using namespace std;

int main()
{
    // // 1. Prime or not
    // cout << "Hello, world!" << endl;
    // int n;
    // cin >> n;
    // int num = 2;

    // while(num<n){
    //     if(num%n==0){
    //         cout<<"Not prime"<<endl;
    //     }
    //     else{
    //         cout<<"Prime"<<endl;
    //     }
    //     num = num+1;
    // }

    // // 2.1 Pattern Questions
    // int n;
    // cin>>n;
    // int i = 0;
    // //shifting through columns
    // while(i<n){
    //     int j=0;
    //     //printing rows
    //     while(j<n){
    //         cout<<"* ";
    //         j++;
    //     }
    //     cout<<endl;
    //     i++;
    // }

    // // 2.2 Pattern
    // int n;
    // cin>>n;
    // int i = 1;
    // //shifting through columns
    // while(i<n){
    //     int j=1;
    //     //printing rows
    //     while(j<n){
    //         cout<<i<<" ";
    //         j++;
    //     }
    //     cout<<endl;
    //     i++;
    // }

    // // 2.3 Pattern
    // int n;
    // cin>>n;
    // int i = 1;
    // while(i<n){
    //     int j = 0;
    //     while(j<n){
    //         cout<<n-j<<" ";
    //         j++;
    //     }
    //     cout<<endl;
    //     i++;
    // }

    // // 2.4 Pattern
    // // Counting
    // int n;
    // int count = 1;
    // cin>>n;
    // int i = 1;
    // while(i<n){
    //     int j = 0;
    //     while(j<n){
    //         cout<<count<<" ";
    //         count++;
    //         j++;
    //     }
    //     cout<<endl;
    //     i++;
    // }

    // // 2.5 Pattern
    // int n;
    // int count = 1;
    // cin>>n;
    // int i = 1;
    // while(i<n){
    //     int j = 0;
    //     while(j<i){
    //         cout<<count<<" ";
    //         count++;
    //         j++;
    //     }
    //     cout<<endl;
    //     i++;
    // }

    // // 2.6 Pattern
    // int n;
    // int count = 1;
    // cin>>n;
    // int i = 1;
    // while(i<n){
    //     int j = 0;
    //     while(j<i){
    //         cout<<count<<" ";
    //         count++;
    //         j++;
    //     }
    //     cout<<endl;
    //     i++;
    //     count=i;
    // }

    // 2.7 Pattern
    int n;
    cin>>n;
    int i = 1;
    while(i<n){
        int j = 0;
        while(j<i){
            cout<<"* ";
            j++;
        }
        cout<<endl;
        i++;
    }

    return 0;
}