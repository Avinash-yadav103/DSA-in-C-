/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
};
*/

#include <iostream>
#include <vector>
using namespace std;

// Definition for a Node.
class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
    Node(int _val) : val(_val), prev(nullptr), next(nullptr), child(nullptr) {}
};

class Solution {
public:
    Node* flatten(Node* head) {
        Node* temp = head;
        while(temp != nullptr){
            Node* a = temp->next;
            if((temp->child) != nullptr){
                Node* c = temp->child;
                temp->child = NULL;
                c = flatten(c);
                c->prev = temp;
                temp->next = c;

                while(c->next != nullptr){
                    c = c->next;
                }
                c->next = a;
                if(a != nullptr){
                    a->prev = c;
                }
            }
            temp = a;
        }
        return head;
    }
};

// Helper function to print the flattened list
void printList(Node* head) {
    Node* curr = head;
    while (curr) {
        cout << curr->val << " ";
        curr = curr->next;
    }
    cout << endl;
}

// Helper function to create a multilevel doubly linked list for testing
Node* createTestList() {
    // Example: 1 - 2 - 3
    //               |
    //               4 - 5
    Node* n1 = new Node(1);
    Node* n2 = new Node(2);
    Node* n3 = new Node(3);
    Node* n4 = new Node(4);
    Node* n5 = new Node(5);

    n1->next = n2;
    n2->prev = n1;
    n2->next = n3;
    n3->prev = n2;

    n2->child = n4;
    n4->next = n5;
    n5->prev = n4;

    return n1;
}

int main() {
    Node* head = createTestList();
    Solution sol;
    Node* flat = sol.flatten(head);
    printList(flat);

    // Free memory (not strictly necessary for small test, but good practice)
    Node* curr = flat;
    while (curr) {
        Node* next = curr->next;
        delete curr;
        curr = next;
    }
    return 0;
}