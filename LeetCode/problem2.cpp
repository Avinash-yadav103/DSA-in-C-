#include<iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
       ListNode* dummy=new ListNode();
       ListNode* temp=dummy;
       int carry=0;
       while(l1!=NULL || l2!=NULL || carry){
          int sum=0;
          if(l1!=NULL){
             sum+=l1->val;
             l1=l1->next;
          }
          if(l2!=NULL){
             sum+=l2->val;
             l2=l2->next;
          }
          sum+=carry;
          carry=sum/10;
          ListNode* newnode=new ListNode(sum%10);
          temp->next=newnode;
          temp=temp->next;
       }
       return dummy->next;
    }
};

void printList(ListNode* head) {
    while (head != nullptr) {
       cout << head->val << " ";
       head = head->next;
    }
    cout << endl;
}

int main() {
    // Create first linked list: 2 -> 4 -> 3
    ListNode* l1 = new ListNode(2, new ListNode(4, new ListNode(3)));

    // Create second linked list: 5 -> 6 -> 4
    ListNode* l2 = new ListNode(5, new ListNode(6, new ListNode(4)));

    Solution solution;
    ListNode* result = solution.addTwoNumbers(l1, l2);

    // Print the result
    cout << "Resultant Linked List: ";
    printList(result);

    return 0;
}