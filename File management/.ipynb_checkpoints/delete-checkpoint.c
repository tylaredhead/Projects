#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc delete.c validateFileName.c handleChangeLog.c -o delete
// input ==> ./delete fileName

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
void changeFileType(char *fileName);

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
        printf("Usage: ./delete fileName\n");
    // checks if valid file name with correct file extensions 
    } else {
        // adds no of extra char to extraChar
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

                if (checkFileAlreadyExists(fileName)){
                    remove(fileName);
                    // removes the corresponding change log file 
                    changeFileType(fileName);
                    remove(fileName);
                    printf("The file has been removed \n");
                } else {
                    printf("The file does not exist \n");
                }
            }
            free(fileName);
        }
    }
    return 0;
}