#include<bits/stdc++.h>
using namespace std;

int n=1000;
bool result[1001][1001];

int main(){
    for(int j=0;j<=n;j++)
        for(int i=0;i<=j;i++){
            for(int k=1;k<=i-k;k++)
                result[i][j]=result[i][j]||!result[i-k*2][j-k];
            for(int k=1;i+k<=j-k;k++)
                result[i][j]=result[i][j]||!result[i+k][j-k];
            for(int k=1;k<=j-k;k++){
                int a[3]={k,i,j-k}; sort(a,a+3);
                result[i][j]=result[i][j]||!result[a[1]-a[0]][a[2]-a[0]];
            }
        }
    for(int i=0;i<=n;i++)
        for(int j=0;j<=n;j++)
            printf("%d%c",result[i][j]," \n"[j==n]);
    return 0;
}
