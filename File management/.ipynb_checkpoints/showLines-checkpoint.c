#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc showLines.c validateFileName.c handleChangeLog.c -o showLine
// input ==> ./showLine fileName

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
int getLastNoOfLines(char *fileName);
void changeFileType(char *fileName);

// keeps getting an input until an int is entered
int getValidInt(char *prompt){
    int num;
    char s[100];
    // check bounds of int
    while (1){
        printf("%s", prompt);
        fgets(s, sizeof(s), stdin);
        num = atoi(s);
        if (atoi(s) != 0){
            return num;
        } else if (strlen(s) == 1){ // accounts for \n added
            return -1;
        } else {
            printf("Invalid input \n");
        }
    } 
}

void showLines(char *fileName){  
    int len = 128, lineNo = 0, found = 0;
    int startLineNo, endLineNo;
    
    FILE *fp = fopen(fileName, "r");
    char s[len];


    if (fp == NULL) {
        printf("Error opening file");
    } else {
        //allocates memory for a fileName and convert to log to get total line number from log file;
        char *changeLogFileName = (char *) malloc(sizeof(char)*strlen(fileName));
        if (changeLogFileName != NULL) {
            strcpy(changeLogFileName, fileName);
            changeFileType(changeLogFileName);
        
            // Gets range of line ==> accepts enter as either the very start or end depending on which input
            startLineNo = getValidInt("Input the starting line number \n  ==>");
            if (startLineNo == -1){
                startLineNo = 1;
            }
            endLineNo = getValidInt("Input the end line number you want displayed \n  ==>");
            if (endLineNo == -1){
                endLineNo = getLastNoOfLines(changeLogFileName);
            }
    
            if (getLastNoOfLines(changeLogFileName) < endLineNo){
                printf("The line number is outside the number of lines within the file \n");
            } else if (startLineNo > endLineNo){
                printf("End index can not be less than start index \n ");
            } else {
                while (1){               
                    if (fgets(s, len, fp) == NULL){
                        break;
                    }  
    
                    if (startLineNo - 1 < lineNo && lineNo <= endLineNo){            
                        printf("%d: %s", lineNo, s);
                    } else if (lineNo > endLineNo){ // prevents unncessary reading of lines once target line has been found
                        break;
                    }
                    char lastChar = s[strlen(s) - 1];
                    if (lastChar == '\n'){
                        lineNo++;
                    }
                }
                printf("\n");
            }
        }
        else 
        {
            printf("Error allocating memory\n");
        }
        fclose(fp);
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
    // Specifies fileType
    const char *fileType = ".txt";
    int extraChar;

    // checks if the user has inputted the correct number of arguments
    if (argc != 2){
        printf("Usage: ./showLines fileName\n");
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
                    strcat(fileName, fileType);
                }
                showLines(fileName);
            }
            free(fileName);
        }
    }
    return 0;
}