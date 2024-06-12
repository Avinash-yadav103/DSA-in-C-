#include <iostream>
using namespace std;

int addDigits(int num){
    int sum = 0;
    if (num / 10 == 0)
    {
        return num;
    }
    
    while (num != 0 | (num/10==0))
    {
        sum = num % 10 + sum;
        num = num / 10;
    }
    num=sum;

    return num;
}

int addDigits2(int num){
    while (num / 10){
        int sum = 0;
        while (num > 0){
            sum += num % 10;
            num /= 10;
        }
        num = sum;
    }
    return num;

}

int main(){
    cout<<addDigits(443);
    cout << "hello";
    return 0;
}