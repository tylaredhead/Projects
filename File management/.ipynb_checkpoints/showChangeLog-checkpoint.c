#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc showChangeLog.c validateFileName.c handleChangeLog.c -o showChangeLog
// input ==> ./showChangeLog fileName

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
void changeFileType(char *fileName);

void dispFile(char *fileName){
    FILE *fp = fopen(fileName, "r");

    int len = 512, i = 0, changesCount = 1;
    char s[len];
    
    // rotates prompts through a mod display
    char *prompt[4] = {"Command: ", "Description: ", "Total line number: ", " "};
    
    if (fp){
        int reading = 1;
        printf("\n");
        while (reading){
            if (fgets(s, len, fp) == NULL){
                reading = 0;
            } else {
                // Prints that a new log is being printed
                printf("%d ==> ", changesCount);

                // gets substrings between delimiters, getting suitable prompt using mod for cyclic approach
                char *token = strtok(s, "¬");
                while (token != NULL){
                    printf("%s%s \n", prompt[i%4], token);
                    token = strtok(NULL, "¬");
                    i++;
                }
            }
            changesCount++;
        }
    } else {
        printf("This file can not be read or does not exist \n");
    }
}

// this copies the contents of one string to another in memory
void copyString(char *from, char *to, int n){
    int i = 0;
    for (i; i < n; i++){
        to[i] = from[i];
    }
}

int main(int argc, char *argv[]){
    const char *expectedFileType = ".txt";
    const char *actualFileType = ".log";
    int extraChar;

    // checks if the user has inputted the correct number of arguments
    if (argc != 2){
        printf("Usage: ./showChangeLog fileName\n");
    } else {
        // Checks if valid file name with correct file extensions 
        if ((extraChar = validateFileName(argv[1], strlen(argv[1]), expectedFileType)) == -1){
            printf("Invalid file name \n");
        } else {
            // allocates memory to account for file type extension if needed to be added
            char *fileName = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
            if (fileName == NULL) {
                printf("Error with memory allocation \n");
            } else {
                copyString(argv[1], fileName, strlen(argv[1]));
                // if no file type, adds .log else replaces .txt with .log
                if (extraChar > 0){
                    fileName = strcat(fileName, actualFileType);
                } else {
                    changeFileType(fileName);
                }
                
                dispFile(fileName);
                free(fileName);
            }
        }
    }
    return 0;
}
