// Implements a dictionary's functionality
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Hash table
const unsigned int N = 10000;
node *table[N];

// Initiate dictionary size count
int count = 0;

// Hashes word to a number
// credit to djb2 http://www.cse.yorku.ca/~oz/hash.html.
unsigned int hash(const char *word)//2
{
    unsigned int hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 2) + hash) + tolower(c);
    }

    return hash % N;
}


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash word for a hash value
    unsigned int n = hash(word);

    if (table[n] == NULL)
    {
        return false;
    }

    node *cursor = table[n];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }

    return false;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    //read strings from file, until return EOF
    char word[LENGTH + 1];
    while (fscanf(dict, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        //check if there is enough memory for malloc
        if (new_node == NULL)
        {
            unload();
            return false;
        }

        //string copy
        unsigned int n = hash(word);
        strcpy(new_node->word, word);

        //insert node into the hash table
        new_node->next = table[n];
        table[n] = new_node;
        count++;
    }

    fclose(dict);
    return true;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return count;
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *cursor = table[i];

            while (cursor != NULL)
            {
                node *tmp = cursor;
                cursor = cursor->next;
                free(tmp);
            }
        }
    }

    return true;
}
