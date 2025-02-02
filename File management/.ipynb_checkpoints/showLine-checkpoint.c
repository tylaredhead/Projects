#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc showLine.c validateFileName.c -o showLine
// input ==> ./showLine fileName

// enables importing of func from file validateFileName.c
int validateFileName(char *a, int n, const char *fileType);

// keeps getting an input until an int is entered
int getValidInt(char *prompt){
    int num;
    char s[100];

    while (1){
        printf("%s", prompt);
        fgets(s, sizeof(s), stdin);
        s[strlen(s) - 1] = '\0'; // replaces the \n with \0 to signify end of string
        num = atoi(s);
        if (atoi(s) != 0){
            return num;
        } else if (strcmp(s, "0") == 0){
            printf("Line number must be greater than 0 \n ");
        } else {
            printf("Invalid input \n");
        }
    } 
}

void showLine(char *fileName){  
    int len = 128, lineNo = 1, found = 0;
    char s[len];
    
    FILE *fp = fopen(fileName, "r");

    int targetLineNo = getValidInt("Which line do you want to print? \n  ==>");
    
    if (fp == NULL) {
        printf("Error opening file");
    } else {
        while (1){
            if (fgets(s, len, fp) == NULL){
                break;
            }

            if (targetLineNo == lineNo){              
                found = 1;
                printf("%s", s);
            } else if (lineNo > targetLineNo){ // prevents unncessary reading of lines once target line has been found
                break;
            }

            // accounts for if len(s) < len(line)
            char lastChar = s[strlen(s) - 1];
            if (lastChar == '\n'){
                lineNo++;
            }
        }
        
        fclose(fp);
        // only displays if line number has not been found
        if (!found){
            printf("The line number is outside the number of lines within the file \n");
        } else {
            printf("\n");
        }
	}
}

// prevents overwriting of files if one already exists
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
        printf("Usage: ./showLine fileName\n");
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

                showLine(fileName);
            }
            free(fileName);
        }
    }
    return 0;
}