// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//prototype
void destroy(node *p);

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

//mark if dict is loaded
bool dict_load = false;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //get the hash value of the word
    int hashv = hash(word);
    //go to the location it the table that corresponds with the hash value and store it in a variable
    node *current = table[hashv];

    while(current != NULL)
    {
        if(strcasecmp(word,current -> word) == 0)
        {
            return true;
        }
        current = current -> next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file;
    // If the small dictionary was inputted then open the small dictionary
    if(strcmp(dictionary, "dictionaries/small") == 0)
    {
        file = fopen("dictionaries/small", "r");
    }
    //else use the big dictionary
    else
    {
        file = fopen(dictionary, "r");
    }

    //intialize all elements of hash table to start with NULL
    for(int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    //create a char that will store each char read from file
    char c;
    //a int that stores the index of current word
    int index = 0;
    //store the words read from file
    char *word = malloc(sizeof(char) * (LENGTH + 1));
    //create a pointer that will store value when appending to linked list
    node *temp;
    //create a pointer that will store address of new node
    node *p;
    //store hash value of word
    int hashv;
    //store the index of the word when adding to new node
    int index1 = 0;

    //while not at the end of the file read wordrs.
    while (fread(&c, sizeof(char), 1, file))
    {
        //only allow for lowecase letters and ' to be added to the word
        if(isalpha(c) || (c == '\''))
        {
            word[index] = c;
            index++;
        }
        //if the end of the word is reached end word
        else if(c == '\n')
        {
            word[index] = c;
            //if create a new node
            p = malloc(sizeof(node));
            //get hash value of word
            hashv = hash(word);

            //if there are no existing nodes then add a nodes and have the table store to the head of the list.
            if(table[hashv] == NULL)
            {
                //store old value of table in a var
                temp = table[hashv];
                //set table to point to head of list
                table[hashv] = p;
                //make the new node point to the old location that table was pointing to
                p -> next = temp;
            }
            //if there is already a node then append a new node
            else
            {
                //store old value of table
                temp = table[hashv];
                //have table point to the new node
                table[hashv] = p;
                //have the new node point to the old location of the table
                p -> next = temp;
            }

            //copy string to the new node
            while(word[index1] != '\n')
            {
                p -> word[index1] = word[index1];
                index1++;
            }
            p -> word[index1] = '\0';

            //reset the indexs
            index1 = 0;
            index = 0;
        }
    }
    //free memory
    fclose(file);
    free(word);
    //mark that dictionary was loaded
    dict_load = true;
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    //if the dict isn't loaded then return 0
    if(dict_load == false)
    {
        return 0;
    }
    //keep track of the amonut of words
    int wcounter = 0;
    //keep track of the current node
    node *current;
    //search through entire hash table
    for(int i = 0; i < N; i++)
    {
        //if there is nothing in that area then continue the loop
        if(table[i] == NULL)
        {
            continue;
        }
        //if there is something in the hash table then see how many nodes there are
        else
        {
            current = table[i];
            while(current != NULL)
            {
                wcounter++;
                current = current -> next;
            }
        }
    }
    return wcounter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for(int i = 0; i < N; i++)
    {
        //if there is no memory to free then check next hash table section
        if(table[i] == NULL)
        {
            continue;
        }
        else
        {
            destroy(table[i]);
        }
    }
    return true;
}

void destroy(node * p)
{
    if(p == NULL)
    {
        return;
    }

    if(p -> next == NULL)
    {
        free(p);
    }
    else
    {
        destroy(p -> next);
        free(p);
    }
}
