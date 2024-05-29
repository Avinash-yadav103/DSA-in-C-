#include<iostream>
using namespace std;

int main() {
    
    // Switch case questions
    // 1.
    int a, b;

    cout <<" Enter the value of a "<<endl;
    cin >> a;

    cout<<" Enter the value of b " <<endl;
    cin >> b;

    char op;
    cout<<" Enter the Operation you want to perform" <<endl;
    cin >> op;

    switch( op ) {

        case '+':  cout << (a+b) <<endl; 
                  break;

        case '-': cout<< (a-b) <<endl;
                  break;  

        case '*': cout<< (a*b) <<endl;
                  break;

        case '/': cout<< (a/b) <<endl;
                  break;

        case '%': cout<< (a%b) <<endl;
                  break;

        default: cout << "Please enter a valid Operation " << endl;

    }

    // 2. How many notes of 100,50,20,10 you'll require to make n amount of money.
    int money;
    int hundred=100;
    int fifty=50;
    int twenty=20;
    int ten=10;
    cin>>money;
    
    switch (money){
        case 100:{
            hundred =money/100;
            cout<<"You'll need"<<hundred<<"notes of hundred";
            money= money-hundred*100;
        };
        case 50:{
            fifty =money/50;
            cout<<"You'll need"<<fifty<<"notes of hundred";
            money= money-fifty*50;
        };
        case 20:{
            twenty =money/20;
            cout<<"You'll need"<<twenty<<"notes of hundred";
            money= money-twenty*20;
        };
        case 10:{
            ten =money/10;
            cout<<"You'll need"<<ten<<"notes of hundred";
            money= money-ten*10;
        };
        

    }

    int n;
    cin>>n;
    
    
    
  

    return 0;
}

