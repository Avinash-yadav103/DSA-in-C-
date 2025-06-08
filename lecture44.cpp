#include<iostream>
using namespace std;

class Node{
    public:
    int data;
    Node* next;

    //Constructor
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

void insertAtHead(Node* &head,int d){
    Node* temp = new Node(d);
    temp -> next = head;
    head = temp;
}

void insertAtTail(Node* &tail,int d){
    Node* temp = new Node(d);
    tail -> next = temp;
    tail = tail -> next;
}

void insertAtPosition(Node* &tail,Node* &head,int position, int d){
    if(position == 1){
        insertAtHead(head,d);
        return;
    }
    Node* temp = head;
    int cnt=1;

    while(cnt<position-1){
        temp= temp ->next;
        cnt++;
    }

    //inserting at last position
    if(temp->next == NULL){
        insertAtTail(tail,d);
        return;
    }

    //Creating new node
    Node* nodetoInsert = new Node(d);
    nodetoInsert -> next = temp -> next;
    temp -> next = nodetoInsert;

}

void deleteNode(int position, Node* &head){
    //deleting first node
    if(position==1){
        Node* temp = head;
        head = head -> next;
        temp->next = NULL;
        delete temp;
    }else{
        Node* curr = head;
        Node* prev = NULL;
        int cnt=1;
        while(cnt<position){
            prev = curr;
            curr = curr->next;
            cnt++;
        }
        prev ->next = curr->next;
        curr->next = NULL;
        delete curr;
    }
}

void print(Node* &head){
    Node* temp = head;

    while(temp!=NULL){
        cout<< temp -> data<<" ";
        temp = temp -> next;
    }
    cout<<endl;

}


int main(){

    Node* node1 = new Node(10);
    Node* head = node1;
    Node* tail = node1;

    insertAtTail(tail, 22);
    insertAtTail(tail, 45);
    insertAtTail(tail, 2);
    insertAtTail(tail, 90);
    
    cout<<node1 -> data<<endl;
    cout<<node1 -> next<<endl;


    // Node* head = node1;
    // Node* tail = node1;
    print(head);

    insertAtHead(head,12);
    insertAtTail(tail,15);
    insertAtPosition(tail,head,5,7);

    print(head);

    return 0;
}