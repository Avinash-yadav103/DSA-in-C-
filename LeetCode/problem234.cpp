#include <iostream>

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
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    bool isPalindrome(ListNode* head) {
        ListNode *slow = head, *fast = head, *prev, *temp;
        while (fast && fast->next)
            slow = slow->next, fast = fast->next->next;
        prev = slow, slow = slow->next, prev->next = NULL;
        while (slow)
            temp = slow->next, slow->next = prev, prev = slow, slow = temp;
        fast = head, slow = prev;
        while (slow)
            if (fast->val != slow->val) return false;
            else fast = fast->next, slow = slow->next;
        return true;
    }
};

// Utility function to create a linked list from an array
ListNode* createLinkedList(int arr[], int n) {
    if (n == 0) return nullptr;
    
    ListNode* head = new ListNode(arr[0]);
    ListNode* current = head;
    
    for (int i = 1; i < n; i++) {
        current->next = new ListNode(arr[i]);
        current = current->next;
    }
    
    return head;
}

// Utility function to delete a linked list
void deleteLinkedList(ListNode* head) {
    while (head) {
        ListNode* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    // Test case 1: 1->2->2->1 (Palindrome)
    int arr1[] = {1, 2, 2, 1};
    ListNode* list1 = createLinkedList(arr1, 4);
    
    Solution solution;
    bool result1 = solution.isPalindrome(list1);
    std::cout << "Test case 1: " << (result1 ? "Palindrome" : "Not a Palindrome") << std::endl;
    
    // Test case 2: 1->2 (Not a Palindrome)
    int arr2[] = {1, 2};
    ListNode* list2 = createLinkedList(arr2, 2);
    
    bool result2 = solution.isPalindrome(list2);
    std::cout << "Test case 2: " << (result2 ? "Palindrome" : "Not a Palindrome") << std::endl;
    
    // Clean up memory
    deleteLinkedList(list1);
    deleteLinkedList(list2);
    
    return 0;
}