#include<iostream>
#include<cmath>
using namespace std;

bool isPalindrome(int x) {
    int i=x;
    int icount = 0;
    int ans=0;
    while(i!=0){
        int digit = i%10;
        i = i/10;
        ans = (digit* pow(10,icount)) + ans;
        icount++;
        
        
    }
    if(ans==x && x>=0){
        return true;
    }
    return false;

}

int main(){
    isPalindrome(121);


    return 0;
}