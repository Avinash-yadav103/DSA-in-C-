#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    vector<int> searchRange(vector<int> &nums, int target)
    {
        pair<int, int> p;
        int s = 0;
        int e = nums.size() - 1;

        p.first = -1;
        p.second = -1;

        // Find the first occurrence
        while (s <= e)
        {
            int mid = s + (e - s) / 2;
            if (nums[mid] == target)
            {
                p.first = mid;
                e = mid - 1; // Narrow down to find the first occurrence
            }
            else if (nums[mid] > target)
            {
                e = mid - 1;
            }
            else
            {
                s = mid + 1;
            }
        }

        s = 0;
        e = nums.size() - 1;

        // Find the last occurrence
        while (s <= e)
        {
            int mid = s + (e - s) / 2;
            if (nums[mid] == target)
            {
                p.second = mid;
                s = mid + 1; // Narrow down to find the last occurrence
            }
            else if (nums[mid] > target)
            {
                e = mid - 1;
            }
            else
            {
                s = mid + 1;
            }
        }

        return {p.first, p.second};
    }
};