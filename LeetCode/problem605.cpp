#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    bool canPlaceFlowers(vector<int>& flowerbed, int n) {
        int count = 0;
        for (int i = 0; i < flowerbed.size(); i++) {
            if (flowerbed[i] == 0) {
                bool left = (i == 0) || (flowerbed[i - 1] == 0);
                bool right = (i == flowerbed.size() - 1) || (flowerbed[i + 1] == 0);

                if (left && right) {
                    flowerbed[i] = 1;
                    count++;
                    if (count >= n) {
                        return true;
                    }
                }
            }
        }
        return count >= n;
    }
};

int main() {
    Solution solution;
    vector<int> flowerbed = {1, 0, 0, 0, 1};
    int n = 1;
    bool result = solution.canPlaceFlowers(flowerbed, n);
    cout << (result ? "True" : "False") << endl;

    flowerbed = {1, 0, 0, 0, 1};
    n = 2;
    result = solution.canPlaceFlowers(flowerbed, n);
    cout << (result ? "True" : "False") << endl;

    return 0;
}