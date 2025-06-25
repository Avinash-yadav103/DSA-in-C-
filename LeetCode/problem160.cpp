#include <iostream>

// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode* t1 = headA;
        ListNode* t2 = headB;
        while(t1!=t2){
            t1 = t1->next;
            t2 = t2->next;
            if(t1 == t2){
                return t1;
            }

            if(t1==NULL) t1= headB;
            if(t2==NULL) t2 = headA;
        }
        return t1;
    }
};

// Function to create a linked list
ListNode* createList(int arr[], int n) {
    if (n == 0) return NULL;
    
    ListNode* head = new ListNode(arr[0]);
    ListNode* current = head;
    
    for (int i = 1; i < n; i++) {
        current->next = new ListNode(arr[i]);
        current = current->next;
    }
    
    return head;
}

// Function to print a linked list
void printList(ListNode* head) {
    while (head) {
        std::cout << head->val << " -> ";
        head = head->next;
    }
    std::cout << "NULL" << std::endl;
}

int main() {
    // Create the common part
    int commonArr[] = {8, 4, 5};
    ListNode* commonPart = createList(commonArr, 3);
    
    // Create list A: 4->1->8->4->5
    int arrA[] = {4, 1};
    ListNode* headA = createList(arrA, 2);
    
    // Connect A to the common part
    ListNode* tailA = headA;
    while (tailA->next) {
        tailA = tailA->next;
    }
    tailA->next = commonPart;
    
    // Create list B: 5->6->1->8->4->5
    int arrB[] = {5, 6, 1};
    ListNode* headB = createList(arrB, 3);
    
    // Connect B to the common part
    ListNode* tailB = headB;
    while (tailB->next) {
        tailB = tailB->next;
    }
    tailB->next = commonPart;
    
    // Print the lists
    std::cout << "List A: ";
    printList(headA);
    std::cout << "List B: ";
    printList(headB);
    
    // Find intersection
    Solution solution;
    ListNode* intersection = solution.getIntersectionNode(headA, headB);
    
    if (intersection) {
        std::cout << "Intersection at node with value: " << intersection->val << std::endl;
    } else {
        std::cout << "No intersection found." << std::endl;
    }
    
    // Clean up memory (free all nodes)
    // Note: Be careful not to delete common nodes twice
    ListNode* current = headA;
    while (current != commonPart) {
        ListNode* temp = current;
        current = current->next;
        delete temp;
    }
    
    current = headB;
    while (current != commonPart) {
        ListNode* temp = current;
        current = current->next;
        delete temp;
    }
    
    // Now delete the common part
    while (commonPart) {
        ListNode* temp = commonPart;
        commonPart = commonPart->next;
        delete temp;
    }
    
    return 0;
}