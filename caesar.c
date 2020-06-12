#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key");
        return 1;
    }

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (isdigit(argv[1][i]) == false)
        {
            printf("Usage: ./caesar key");
            return 1;
        }
    }

    printf("Success\n");
    printf("%s\n", argv[1]);
    //change the key into integar
    int key = atoi(argv[1]);

    //get plain text
    string texts = get_string("Enter your texts: ");
    printf("plaintext: %s\n", texts);
    printf("ciphertext: ");

    for (int i = 0, n = strlen(texts); i < n; i++)
    {
        if (islower(texts[i]))
        {
            //process with key
            int pi = texts[i] - 97;
            pi = (pi + key) % 26;
            int ci = pi + 97;

            printf("%c", ci);
        }
        else if (isupper(texts[i]))
        {
            //process with key
            int pi = texts[i] - 65;
            pi = (pi + key) % 26;
            int ci = pi + 65;

            printf("%c", ci);
        }
        else
        {
            printf("%c", texts[i]);
        }

    }
    printf("\n");
    return 0;
}



