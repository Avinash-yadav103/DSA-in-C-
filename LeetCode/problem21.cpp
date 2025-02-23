#include <iostream>
#include<vector>
using namespace std;

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
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode* dummy = new ListNode(0);
        ListNode* newlist = dummy;

        while(list1 && list2){
            if(list1->val > list2->val){
                newlist->next = list2;
                list2 = list2->next;
            } else {
                newlist->next = list1;
                list1 = list1->next;
            }
            newlist = newlist->next;
        }
        if (list1) 
            newlist->next = list1;
        else 
            newlist->next = list2;

        ListNode* head = dummy->next;
        delete dummy; // Free the dummy node
        return head;
    }
};

// Helper function to create a linked list from a vector
ListNode* createList(const std::vector<int>& values) {
    ListNode* dummy = new ListNode(0);
    ListNode* current = dummy;
    for (int val : values) {
        current->next = new ListNode(val);
        current = current->next;
    }
    ListNode* head = dummy->next;
    delete dummy; // Free the dummy node
    return head;
}

// Helper function to print a linked list
void printList(ListNode* head) {
    while (head) {
        std::cout << head->val << " ";
        head = head->next;
    }
    std::cout << std::endl;
}

int main() {
    Solution solution;

    // Create two linked lists
    std::vector<int> values1 = {1, 2, 4};
    std::vector<int> values2 = {1, 3, 4};
    ListNode* list1 = createList(values1);
    ListNode* list2 = createList(values2);

    // Merge the two linked lists
    ListNode* mergedList = solution.mergeTwoLists(list1, list2);

    // Print the merged linked list
    printList(mergedList);

    // Free the merged linked list
    while (mergedList) {
        ListNode* temp = mergedList;
        mergedList = mergedList->next;
        delete temp;
    }

    return 0;
}