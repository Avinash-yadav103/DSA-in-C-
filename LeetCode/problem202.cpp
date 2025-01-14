class Solution {
public:
    // bool isHappy(int n) {
    //     int sum=0;
    //     if(n/10==0){
    //         if(n==1){
    //             return true;
    //         }
    //         return false;
    //     }
    //     // while(n/10){
    //         while(n>0){
    //             int x = n%10;
    //             int y = x*x;
    //             sum =sum+y;
    //             n = n/10;
    //             if(n/10==0){
    //                 int z = n*n;
    //                 sum = sum+z;
    //             }
    //             n=sum;
    //         }
    //     // }
    //     return true;
    // }

     bool isHappy(int n) {
        auto getNext = [](int num) {
            int sum = 0;
            while (num > 0) {
                int digit = num % 10;
                sum += digit * digit;
                num /= 10;
            }
            return sum;
        };
        
        int slow = n;
        int fast = getNext(n);
        
        while (fast != 1 && slow != fast) {
            slow = getNext(slow);
            fast = getNext(getNext(fast));
        }
        
        return fast == 1;
    }
};

int main(){


    return 0;
}