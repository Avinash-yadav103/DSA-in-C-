#include<iostream>
using namespace std;

class Node{
    public:
    int data;
    Node* prev;
    Node* next;

    //Constructor
    Node(int d){
        this-> data = d;
        this->prev =NULL;
        this->next=NULL;
    }
};

void print(Node* head){
    Node* temp = head;

    while(temp!=NULL){
        cout<< temp->data;
        temp = temp->next;
        cout<<" ";
    }
    cout<<endl;
}


int getLength(Node* head){
    int len =0;
    Node* temp =head;
    while(temp!=NULL){
        len++;
        temp = temp->next;
    }

    return len;
}

void insertAtHead(Node* & head, int d){
    Node* temp = new Node(d);
    temp->next = head;
    head->prev = temp;
    temp = head;

}

void insertAtTail(Node* & tail, int d){
    Node* temp = new Node(d);
    tail->next = temp;
    temp->prev = tail;
    tail = temp;

}

void deleteNode(Node* &head, Node* &tail, int position) {
    // Deleting the first node
    if (position == 1) {
        Node* temp = head;
        head = head->next;
        if (head != NULL) {
            head->prev = NULL;
        } else {
            tail = NULL; // If the list becomes empty
        }
        delete temp;
        return;
    }

    Node* current = head;
    int cnt = 1;

    // Traverse to the node at the given position
    while (cnt < position && current != NULL) {
        current = current->next;
        cnt++;
    }

    // If the node to delete is the last node
    if (current != NULL && current->next == NULL) {
        tail = current->prev;
        tail->next = NULL;
        delete current;
        return;
    }

    // If the node is somewhere in the middle
    if (current != NULL) {
        current->prev->next = current->next;
        current->next->prev = current->prev;
        delete current;
    }
}

int main(){
    Node* node1 = new Node(10);
    Node* head = node1;
    print(head);
    cout<<getLength(head)<<endl;
    // Insert at tail
    Node* tail = head;
    insertAtTail(tail, 20);
    print(head);

    // Insert at head
    insertAtHead(head, 5);
    print(head);

    // Delete first node
    deleteNode(head, tail, 1);
    print(head);

    // Delete last node
    deleteNode(head, tail, getLength(head));
    print(head);

    // Delete middle node
    deleteNode(head, tail, 2);
    print(head);
    insertAtHead(head,11);
    print(head);
    return 0;
}