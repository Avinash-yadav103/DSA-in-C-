#include<iostream>
using namespace std;

void update(int n){
    n++;
}

void update2(int &n){
    n++;
}

int getSum(int arr[],int n){

    int sum=0;
    for(int i=0;i<n;i++){
        sum+=arr[i];
    }

    return sum;
}

int main(){

    // int i =5;
    // // Creating a reference variable 
    // int &j=i;
    // cout<<i<<endl;
    // i++;
    // cout<<i<<endl;
    // j++;
    // cout<<i<<endl;
    // int n=5;
    // cout<<"Before "<<n<<endl;
    // update(n);
    // cout<<"After "<<n<<endl;
    // update2(n);
    // cout<<"After "<<n<<endl;



    //Reference Variable
    char ch ='q';
    cout<<sizeof(ch)<<endl;

    char* c= &ch;
    cout<<sizeof(c)<<endl;


    //Dynamic Array
    int n;
    cin>>n;
    int *arr= new int[n];

    for(int i=0;i<n;i++){
        cin>>arr[i];
    }
    int ans = getSum(arr,n);
    cout<<"answer is "<<ans<<endl;

    return 0;
}