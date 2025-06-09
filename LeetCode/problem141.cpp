#include <iostream>
#include <unordered_set>

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    bool hasCycle(ListNode *head) {
        std::unordered_set<ListNode*> visited;
        while (head != nullptr) {
            if (visited.find(head) != visited.end()) {
                return true;
            }
            visited.insert(head);
            head = head->next;
        }
        return false;
    }
};

int main() {
    // Example usage:
    ListNode* head = new ListNode(3);
    ListNode* second = new ListNode(2);
    ListNode* third = new ListNode(0);
    ListNode* fourth = new ListNode(-4);

    head->next = second;
    second->next = third;
    third->next = fourth;
    fourth->next = second; // Creates a cycle

    Solution solution;
    if (solution.hasCycle(head)) {
        std::cout << "Cycle detected in the linked list." << std::endl;
    } else {
        std::cout << "No cycle detected in the linked list." << std::endl;
    }

    // Free memory (in a real scenario, ensure proper cleanup)
    delete head;
    delete second;
    delete third;
    delete fourth;

    return 0;
}