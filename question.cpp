//Armstrong Number

#include<iostream>
#include<math.h>
using namespace std;

void isArmstrong(int n){
    // for number of digits
    int count = 0;
    int digit;
    int sum = 0;
    while(n!=0){
        n = n/=10;
        count++;
    }

    while(n!=0){
        n = n/=10;
        digit = n%10;
        sum += pow(digit,count);

    }

    if(sum == n){
        cout<<"Armstrong";
    }
    else{
        cout<<"Not Armstrong";
    }
}

int main(){
    
    isArmstrong(153);
}