#include<iostream>
#include<vector>
using namespace std;
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        if(prices.empty()){
            return 0;
        }
        int min = prices[0];
        // int max = 0;
        int profit = 0;
        int n =prices.size();
        for(int i=0;i<n;i++){
            if(prices[i]<min){
                min = prices[i];
            }
            if((prices[i]-min>profit)){
                profit = prices[i]-min;
            }

        }
        return profit;
        // return 0;
    }
};

int main() {
    Solution solution;
    
    // Example test cases
    vector<int> prices1 = {7, 1, 5, 3, 6, 4};
    cout << "Max profit for prices1: " << solution.maxProfit(prices1) << endl; 
    
    vector<int> prices2 = {7, 6, 4, 3, 1};
    cout << "Max profit for prices2: " << solution.maxProfit(prices2) << endl; 
    
    vector<int> prices3 = {2, 4, 1};
    cout << "Max profit for prices3: " << solution.maxProfit(prices3) << endl;
    
    return 0;
}
