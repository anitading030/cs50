#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    //get texts
    string texts = get_string("Text: ");

    //count characterss
    int characters = 0;
    for (int c = 0, n = strlen(texts); c < n; c++)
    {
        texts[c] = tolower(texts[c]);
        if (isalpha(texts[c]))
        {
            characters = characters + 1;
        }
    }


    //count words
    int words = 1;
    for (int w = 0, n = strlen(texts); w < n; w++)
    {
        if (texts[w] == ' ' && texts[w + 1] != ' ')
        {
            words = words + 1;
        }
    }


    //count sentences
    int sentences = 0;
    for (int s = 0, n = strlen(texts); s < n; s++)
    {
        if (texts[s] == '.' || texts[s] == '?' || texts[s] == '!')
        {
            sentences = sentences + 1;
        }
    }

    //calculate readability grade
    float L = 100 * (float)characters / words;
    float S = 100 * (float)sentences / words;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", round(index));
    }
}


