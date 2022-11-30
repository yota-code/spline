/*Median of Medianshttp://cs.indstate.edu/~spitla/presentation.pdf*/

    int select(int *a, int s, int e, int k) {
    if(e-s+1 <= 5)
    {
        sort(a+s, a+e);
        return s+k-1;
    }

    for(int i=0; i<(e+1)/5; i++)
    {
        int left = 5*i;
        int right = left + 4;
        if(right > e) right = e;

        int median = select(a, left, right, 3);
        swap(a[median], a[i]);
    }
    return select(a, 0, (e+1)/5, (e+1)/10); }

    int main() 
    {  
    int a[] = {6,7,8,1,2,3,4,5,9,10};
    int n = 10;

    int mom = select(a, 0, n-1, n/2);
    cout<<"Median of Medians: " << a[mom] << endl;
    return 0; }


