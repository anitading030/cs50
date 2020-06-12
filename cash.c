#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollar;
    do
    {
        dollar = get_float("Change Owed: ");
    }
    while (dollar <= 0);
    
    int cent = round (dollar*100);
    int coin = 0;
    
    while(cent>=25)
    {
        cent = cent-25;
        coin++;
    }
    while(cent>=10)
    {
        cent = cent-10;
        coin++;
    }
    while(cent>=5)
    {
        cent = cent-5;
        coin++;
    }
    while(cent>=1)
    {
        cent = cent-1;
        coin++;
    }
    printf("%i\n", coin);
}