/**
 * Definition for a binary tree node.
 * struct TreeNode {
#include <iostream>
using namespace std;

int main() {
    // Create two identical trees
    TreeNode* p = new TreeNode(1);
    p->left = new TreeNode(2);
    p->right = new TreeNode(3);
    
    TreeNode* q = new TreeNode(1);
    q->left = new TreeNode(2);
    q->right = new TreeNode(3);
    
    Solution sol;
    cout << (sol.isSameTree(p, q) ? "true" : "false") << endl;
    
    return 0;
}
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        // Both trees are empty
        if (p == NULL && q == NULL) 
            return true;


        if (p == NULL || q == NULL) 
            return false;


        return (p->val == q->val) && 
               isSameTree(p->left, q->left) && 
               isSameTree(p->right, q->right);


    }

        // Both trees are empty
        // One tree is empty, and the other is not
        // Check if the current nodes have the same value and
        // recursively check the left and right subtrees
};