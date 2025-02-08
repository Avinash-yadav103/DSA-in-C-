#include<iostream>
using namespace std;

class Solution {
public:
    int mySqrt(int x) {
        if(x==0){
            return 0;
        }
        int low = 1;
        int high = x;
        int result =0;
        while(low<=high){
            int mid = low + (high - low)/2;
            if(mid<=x/mid){
                result = mid;
                low = mid +1;
            }
            else{
                high = mid -1;
            }

        }

        return result;
    }
};
int main() {
    Solution sol;
    int num = 16; // Example input
    int result = sol.mySqrt(num);
    cout << "The square root of " << num << " is " << result << endl;
    return 0;
}