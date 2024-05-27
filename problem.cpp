#include<iostream>
#include<math.h>
using namespace std;

int main(){
    // Leetcode problem .
    // int a;
    // cin>>a;

    // int sum =0;
    // int product = 1;

    // while(a!=0){
    //     int x = a%10;
    //     int y = a/10;

    //     sum = x+sum;
    //     product = x*product;
    //     a = y;

    // }
    // cout<<sum<<" "<<product<<endl;
    // if(sum>product){
    //     cout<< sum-product;
    // }
    // else if(product>sum){
    //     cout<< product-sum;
    // }
    // else{
    //     cout<<0;
    // }

    // Leetcode problem 191



    // Decimal to binary
    // int n;
    // cin>>n;
    // //for positive integer
    // int number = 0;
    // int i = 0;
    // while(n!=0){
    //     int bit = n&1;
    //     number = bit * pow(10,i) + number;
    //     // number = bit+number*10;
    //     i++;
    //     n = n>>1;
    // }
    // cout<<number<<endl;
    //for negative integer (we know how it is stored)
    // int number = 0;





    // // Binary to Decimal
    // int n;
    // cin>>n;
    // int i=0;
    // int ans=0;

    // while(n!=0){
    //     // int bit = n&1;  Nhi krna hai
    //     int digit = n%10;
    //     if(digit==1){
    //         ans = ans+ pow(2,i);
    //     }
        
    //     n = n/10;
    //     i++;
    // }
    // cout<<ans;



    // // Leetcode problem 7(med).
    // int x;
    // cin>>x;
    // int num =0;
    //     while(x!=0){
    //         int digit = x%10;
    //         if(num>INT_MAX/10 || num<INT_MIN/10){
    //             return 0;
    //         }
    //         num = (num*10) + digit;
    //         x = x/10;
    //     }
    //     return num;


    // // Leetcode problem 1009
    // int n;
    // cin>>n;
    // int m = n;
    //     int mask = 0;

    //     if(n==0){
    //         return 1;
    //     }
    //     while(m!=0){
    //         mask = (mask<<1)|1 ;
    //         m = m>>1;
    //     }
    //     int num = (~n)& mask;
    //     return num;


    //Leetcode Problem 231
    int n;
    cin>>n;
    int count = 0;
        while(n!=0){
            if(n&1){
                count++;
            }
            
            n= n>>1;
        }
        if(count==1){
            return true;
        }
        else{
            return false;
        }


    return 0;
}

