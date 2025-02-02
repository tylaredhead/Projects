#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc showFile.c validateFileName.c -o showFile
// input ==> ./showFile fileName

// enables importing of func from file validateFileName.c
int validateFileName(char *a, int n, const char *fileType);

// displays all lines of a file
void showFile(char *fileName){
    FILE *fp;
    int len = 128;
    char s[len];
    fp = fopen(fileName, "r");

    if (fp){
        while(1){
            if (fgets(s, len, fp) == NULL){
                break;
            } else {
                printf("%s", s);
            }
        }
        fclose(fp);
    } else {
        printf("This file does not exist");
    }
    printf("\n");
}

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
        printf("Usage: ./showFile fileName\n");
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

                showFile(fileName);
            }
            free(fileName);
        }
    }
    return 0;
}
