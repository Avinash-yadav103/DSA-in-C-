// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        if (!head || k == 1) return head;

        ListNode dummy(0);
        dummy.next = head;

        ListNode* prevGroupTail = &dummy;
        ListNode* curr = head;

        while (true) {
            // Check if there are at least k nodes left
            ListNode* temp = curr;
            int count = 0;
            while (temp && count < k) {
                temp = temp->next;
                count++;
            }
            if (count < k) break;

            // Reverse k nodes
            ListNode* prev = nullptr;
            ListNode* next = nullptr;
            ListNode* groupHead = curr;
            for (int i = 0; i < k; i++) {
                next = curr->next;
                curr->next = prev;
                prev = curr;
                curr = next;
            }

            // Connect previous group to reversed group
            prevGroupTail->next = prev;

            // Connect end of reversed group to next part
            groupHead->next = curr;

            // Move prevGroupTail to end of this group
            prevGroupTail = groupHead;
        }

        return dummy.next;
    }
};
