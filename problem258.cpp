#include<iostream>
using namespace std;


int addDigits(int num) {
        int sum = 0;
        if(num/10==0){
            return num;
        }
        else{
            while(num!=0 && num/10==0){
                sum = num%10 + sum;
                num =num/10;
            }
        }

        return sum;
    }

int main(){

    addDigits(43);




    return 0;
}