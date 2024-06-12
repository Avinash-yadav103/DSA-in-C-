#include <iostream>
using namespace std;

int totalMoney(int n){
    int sum = 0;
    int m = 1;
    for (int i = 1; i <= n; i++)
    {
        sum += m;
        if (i % 7 == 0)
        {
            m = i / 7;
        }
        m++;
    }

    return sum;
}

int main(){
    totalMoney(12);
    return 0;
}