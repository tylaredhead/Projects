#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
// imported from other files

// finds the last record from the change log and gets the 3rd part (current total line number) ==> returns int found
int getLastNoOfLines(char *fileName){
    FILE *fp = fopen(fileName, "r");
    if (fp){
        int lastNoOfLines;
        char line[512];

        while(fgets(line, sizeof(line), fp)){
            // Gets each part of a line separated by // and converting the string to int
            char *token = strtok(line, "¬");
            for (int i = 0; token != NULL; i++) {
                // if token cannot be converted to an int it returns 0, so manual check for "0"
                if (atoi(token) != 0){
                    lastNoOfLines = atoi(token);
                // Accounts for atoi returning 0 if a string if inputted
                } else if (strcmp(token, "0") == 0){
                    lastNoOfLines = 0;
                }
                token = strtok(NULL, "¬");
            }            
        }
        return lastNoOfLines;
            
    }
}

// changes the filetype from a .txt to a .log
void changeFileType(char *fileName){
    const char *newFileType = ".log";
    int found = 0, i = 0;
    for (i; i < strlen(fileName); i++){
        if (fileName[i] == '.'){
            found = i;
        }
        if (found){
            fileName[i] = newFileType[i - found];
        }
    }
}


// Line structure ==> command used // what happened (description total line number 
// updates change log with parameter information ==> returns 1 if successful, else returns 0
int handleChangeLog(char *fileName, char *command, char *msg, int lineNo){
    changeFileType(fileName);
    FILE *fp;
    fp = fopen(fileName, "a+");
    if (fp) {
        // adds line to file
        fprintf(fp, "%s¬%s¬%d¬ ", command, msg, lineNo);
        fclose(fp);
        return 1;
    } else {
        printf("Error - change log can not be accessed");
    }
    return 0;
}