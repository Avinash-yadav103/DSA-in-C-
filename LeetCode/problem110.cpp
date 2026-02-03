/**
 * Definition for a binary tree node.
 * struct TreeNode {
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
    bool isBalanced(TreeNode* root) {
        

        return false;
    }
};
#include <iostream>
#include <algorithm>

// NOTE: TreeNode must be declared before `class Solution` in this file.
// Move this struct above `class Solution` (or uncomment the provided definition).
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* l, TreeNode* r) : val(x), left(l), right(r) {}
};

static void deleteTree(TreeNode* root) {
    if (!root) return;
    deleteTree(root->left);
    deleteTree(root->right);
    delete root;
}

int main() {
    Solution sol;

    // Test 1: empty tree (balanced)
    {
        TreeNode* root = nullptr;
        std::cout << "Test 1 (empty): " << sol.isBalanced(root) << "\n";
    }

    // Test 2: single node (balanced)
    {
        TreeNode* root = new TreeNode(1);
        std::cout << "Test 2 (single): " << sol.isBalanced(root) << "\n";
        deleteTree(root);
    }

    // Test 3: balanced tree: [3,9,20,null,null,15,7]
    {
        TreeNode* root = new TreeNode(3);
        root->left = new TreeNode(9);
        root->right = new TreeNode(20, new TreeNode(15), new TreeNode(7));

        std::cout << "Test 3 (balanced): " << sol.isBalanced(root) << "\n";
        deleteTree(root);
    }

    // Test 4: unbalanced tree (left-skewed): 1->2->3->4
    {
        TreeNode* root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->left->left = new TreeNode(3);
        root->left->left->left = new TreeNode(4);

        std::cout << "Test 4 (unbalanced): " << sol.isBalanced(root) << "\n";
        deleteTree(root);
    }

    // Add more tests here...

    return 0;
}