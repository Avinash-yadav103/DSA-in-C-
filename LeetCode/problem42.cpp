class Solution {
public:
    int trap(vector<int>& height) {
        int leftMax = 0;
        int rightMax = 0;
        int total = 0;
        int h = height.size();
        int l = 0;
        int r = h-1;
        while(l<r){
            if( height[l] <= height[r]){
                if(leftMax > height[l]){
                    total += leftMax - height[l];
                }else{
                    leftMax = height[l];
                }
                l++;
            }else{
                if(rightMax>height[r]){
                    total += rightMax - height[r];
                }else{
                    rightMax = height[r];
                }
                r--;
            }
        }
        return total;
    }
};