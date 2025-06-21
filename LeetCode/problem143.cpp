/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

// Uncomment this if the definition is not included elsewhere
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    void reorderList(ListNode* head) {
        if(!head || !head->next){
            return;
        }

        // Step 1: Find the middle of the linked list
        ListNode* slow = head;
        ListNode* fast = head;
        while(fast->next && fast->next->next){
            slow = slow->next;
            fast = fast->next->next;
        }

        // Step 2: Reverse the second half of the linked list
        ListNode* premiddle = slow;
        ListNode* precurrent = slow->next;
        while(precurrent && precurrent->next){
            ListNode* current = precurrent->next;
            precurrent->next = current->next;
            current->next = premiddle->next;
            premiddle->next = current;
        }
        
        // Step 3: Merge the first half with reversed second half
        ListNode* first = head;
        ListNode* second = premiddle->next;
        premiddle->next = nullptr; // Cut off the first half
        
        while(second){
            ListNode* temp1 = first->next;
            ListNode* temp2 = second->next;
            first->next = second;
            second->next = temp1;
            first = temp1;
            second = temp2;
        }
    }
};