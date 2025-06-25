#include <iostream>

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        if (!head || !head->next) return NULL;
        
        ListNode* slow = head;
        ListNode* fast = head;
        
        // Find meeting point inside the cycle
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) break;
        }
        
        // If no cycle, return NULL
        if (!fast || !fast->next) return NULL;
        
        // Find cycle start
        slow = head;
        while (slow != fast) {
            slow = slow->next;
            fast = fast->next;
        }
        
        return slow;
    }
};

int main() {
    // Create a linked list with a cycle: 1->2->3->4->2 (4 points back to 2)
    ListNode* node1 = new ListNode(1);
    ListNode* node2 = new ListNode(2);
    ListNode* node3 = new ListNode(3);
    ListNode* node4 = new ListNode(4);
    
    node1->next = node2;
    node2->next = node3;
    node3->next = node4;
    node4->next = node2;  // Create cycle
    
    Solution solution;
    ListNode* cycleStart = solution.detectCycle(node1);
    
    if (cycleStart) {
        std::cout << "Cycle detected, starts at node with value: " << cycleStart->val << std::endl;
    } else {
        std::cout << "No cycle detected" << std::endl;
    }
    
    // Clean up memory - note that with a cycle we need to break it first
    node4->next = NULL;
    delete node1;
    delete node2;
    delete node3;
    delete node4;
    
    return 0;
}