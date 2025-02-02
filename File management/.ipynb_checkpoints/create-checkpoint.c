#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc create.c validateFileName.c handleChangeLog.c -o create
// input ==> ./create fileName

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
int handleChangeLog(char *fileName, char *command, char *msg, int lineNo);

// creates file ==> returns 1 if file created, else 0
int createFile(char *fileName){
    FILE *fp;
    fp = fopen(fileName, "w");

    // Creates file if memory allocated
    if (fp == NULL){
        printf("Error: can't create txt \n");
        return 0;
    } else {
        fclose(fp);
        printf("File created \n");
        return 1;
    }
}

// prevents overwriting of files if one already exists ==> returns 1 if file can be read else 0
int checkFileAlreadyExists(char *fileName){
    FILE *fp;
    fp = fopen(fileName, "r");
    if (fp) {
        fclose(fp);
        return 1;
    }
    return 0;
}

// this copies the contents of one string to another in memory
void copyString(char *from, char *to, int n){
    int i = 0;
    for (i; i < n; i++){
        to[i] = from[i];
    }
}

int main(int argc, char *argv[]){
    // Specifies fileType
    const char *fileType = ".txt";
    int extraChar;

    // checks if the user has inputted the correct number of arguments
    if (argc != 2){
        printf("Usage: ./create fileName\n");
    } else {
        // Checks if valid file name with correct file extensions 
        if ((extraChar = validateFileName(argv[1], strlen(argv[1]), fileType)) == -1){
            printf("Invalid file name \n");
        } else {
            // allocates memory to account for file type extension if needed to be added
            char *fileName = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
            if (fileName == NULL) {
                printf("Error with memory allocation \n");
            } else {
                // Assigns the new memory the fileName with correct file type
                copyString(argv[1], fileName, strlen(argv[1]));
                if (extraChar > 0){
                    fileName = strcat(fileName, fileType);
                }

                // Check file wont be overwritten
                if (checkFileAlreadyExists(fileName) == 1){
                    printf("A file already exists with this file name \n");
                } else {
                    if (createFile(fileName)){
                        handleChangeLog(fileName, "Created file", "Txt file made", 0);
                    }
                }
            }
            free(fileName);
        }
    }
    return 0;
}