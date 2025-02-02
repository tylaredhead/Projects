#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc appendLine.c validateFileName.c handleChangeLog.c -o appendLine
// input ==> ./appendLine fileName

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
int handleChangeLog(char *fileName, char *command, char *msg, int lineNo);
void changeFileType(char *fileName);
int getLastNoOfLines(char *fileName);

// args ==> fileName for opening file and input for memory buffer fo input so can be accessed for change log
// return ==> 1 if valid command else 0
int appendLine(char *fileName, char *input){
    FILE *fp = fopen(fileName, "a");
    char *changeLogFile = (char *) malloc(sizeof(char)*strlen(fileName));
  
    if (fp){
        if (changeLogFile){
        // Converts file type from .txt to .log so can access the change log for last no of lines
            strcpy(changeLogFile, fileName);
            changeFileType(changeLogFile);
            
            //Gets user input and if first line, add directly else create new line first
        	printf("Enter new line to add:\n");
            fgets(input, sizeof(input), stdin);
            input[strlen(input) - 1] = '\0'; // removes \n
            if (getLastNoOfLines(changeLogFile) != 0){
                fprintf(fp, "\n%s", input);
            } else {
                fprintf(fp, "%s", input);
            }
            
            printf("Line has been added \n ");
            
        	fclose(fp);
            free(changeLogFile);
            return 1;
        }
    } else {
        printf("This file does not exist \n ");
        return 0;
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
        printf("Usage: ./appendLine fileName \n");
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

                // checks if file exists
                if (checkFileAlreadyExists(fileName)){
                    char *line, input[512];
                    if (appendLine(fileName, input)){
                        // Gets a concat of text and the line just added 
                        const char text[] = "Line added at end of file: ";
                        char *msg = (char *) malloc(sizeof(char)*(strlen(text) + strlen(input) + 1));
    
                        if (msg){
                            strcpy(msg, text);
                            strcat(msg, input);
                            changeFileType(fileName);
                            handleChangeLog(fileName, "\nAppend line", msg, getLastNoOfLines(fileName) + 1);
    
                            free(msg);
                        }
                    }
                } else {
                    printf("This file does not exist \n ");
                }
            }
            free(fileName);
        }
    }
    return 0;
}