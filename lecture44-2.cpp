#include<iostream>
using namespace std;

class Node{
    public:
    int data;
    Node* next;

    //constructor
    Node(int data){
        this -> data = data;
        this -> next = NULL;
    }

    //Destructor
    ~Node(){
        int value = this->data;
        if(this->next != NULL){
            delete next;
            this->next = NULL;
        }
        cout<<" memory is free for node with data ";
    }
};


void insertNode(Node* &tail, int element, int d){
    // Empty list
    if(tail == NULL){
        Node* newNode = new Node(d);
        tail = newNode;
        newNode->next = newNode;
        return;
    }

    // Non-empty list
    Node* curr = tail;
    while(curr->data != element){
        curr = curr->next;
        if(curr == tail) break; // Element not found
    }

    Node* newNode = new Node(d);
    newNode->next = curr->next;
    curr->next = newNode;

    // Update tail if inserting after tail
    if(curr == tail) tail = newNode;
}

void deleteNode(Node* &tail, int value){
    // Empty list
    if(tail == NULL){
        cout << "List is empty, nothing to delete." << endl;
        return;
    }

    // Non-empty list
    Node* prev = tail;
    Node* curr = prev->next;

    while(curr->data != value){
        prev = curr;
        curr = curr->next;
        if(curr == tail->next) break; // Element not found
    }

    if(curr->data != value){
        cout << "Node with value " << value << " not found." << endl;
        return;
    }

    prev->next = curr->next;

    // Update tail if deleting tail
    if(curr == tail) tail = (curr == curr->next) ? NULL : prev;

    curr->next = NULL;
    delete curr;
}

int main(){
    Node* tail = NULL;

    // Insert nodes
    insertNode(tail, 0, 10); // First node
    insertNode(tail, 10, 20);
    insertNode(tail, 20, 30);
    insertNode(tail, 30, 40);

    // Print list
    Node* temp = tail->next;
    do{
        cout << temp->data << " ";
        temp = temp->next;
    } while(temp != tail->next);
    cout << endl;

    // Delete nodes
    deleteNode(tail, 20);
    deleteNode(tail, 40);

    // Print list after deletion
    if(tail != NULL){
        temp = tail->next;
        do{
            cout << temp->data << " ";
            temp = temp->next;
        } while(temp != tail->next);
    } else {
        cout << "List is empty." << endl;
    }

    return 0;
}