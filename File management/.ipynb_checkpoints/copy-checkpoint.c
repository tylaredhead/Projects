#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// compile ==> gcc copy.c validateFileName.c handleChangeLog.c -o copy
// input ==> ./copy fromFile toFile 

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
int handleChangeLog(char *fileName, char *command, char *msg, int lineNo);

//Copies the contents from one file to another ==> returns line number if file successfully copied else -1
int copyFile(char *fromFile, char *toFile){
    FILE *f1p, *f2p;
    int len = 128, count = 1;
    char s[len];

    // opens both files and directly adds the string from buffer s to the second file 
    f1p = fopen(fromFile, "r");
    f2p = fopen(toFile, "w");
    if (f1p && f2p){
        int reading = 1;
        while(reading){
            if (fgets(s, len, f1p) == NULL){
                reading = 0;
            } else {
                if (s[strlen(s) - 1] == '\n'){
                    count++;
                }
                fprintf(f2p, "%s", s);
            }
            
        }
        fclose(f1p);
        fclose(f2p);
        printf("File has been copied \n");
        return count;
    } else { 
        printf("Error reading or writing to file \n");
    }
    return -1;
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
    // specifies fileType
    const char *fileType = ".txt";
    int fromFileExtraChar, toFileExtraChar;

    // checks if the user has inputted the correct number of arguments
    if (argc != 3){
        printf("Usage: ./copy fromFile toFile\n");
    } else {
        // Checks if valid file name with correct file extensions for both files
        if ((fromFileExtraChar = validateFileName(argv[1], strlen(argv[1]), fileType)) == -1){
            printf("Invalid file name \n");
        } else if ((toFileExtraChar = validateFileName(argv[2], strlen(argv[2]), fileType)) == -1){
            printf("Invalid file name \n");
        } else {
            // allocates memory to account for file type extension if needed to be added
            char *fromFile = (char *) malloc(sizeof(char) * (strlen(argv[1]) + fromFileExtraChar));
            char *toFile = (char *) malloc(sizeof(char) * (strlen(argv[2]) + toFileExtraChar));

            if (fromFile == NULL || toFile == NULL){
                printf("Error in memory allocation \n");
            } else {
                // Assigns the new memory the fileName with correct file type
                copyString(argv[1], fromFile, strlen(argv[1]));
                copyString(argv[2], toFile, strlen(argv[2]));
                
                if (fromFileExtraChar > 0){
                    fromFile = strcat(fromFile, fileType);
                }
                if (fromFileExtraChar > 0){
                    toFile = strcat(toFile, fileType);
                }

                // Checks the file to read from exists and the file being written to is not going to be overwrited
                if (checkFileAlreadyExists(toFile)){
                    printf("There already exists a file of %s \n", toFile);
                } else if (!checkFileAlreadyExists(fromFile)){
                    printf("File copying from does not exist \n");
                } else {
                    int count;
                    if ((count = copyFile(fromFile, toFile)) >= 0){
                        // gets message with the file name which has been copied from
                        const char text[] = "File been copied from ";
                        char *msg = (char *) malloc(sizeof(char)*(strlen(fromFile) + strlen(text) + 1));

                        if (msg){
                            strcpy(msg, text);
                            strcat(msg, fromFile);
                            handleChangeLog(toFile, "Copy file", msg, count);
                            
                            free(msg);
                        }
                    }
                }
            }
            free(fromFile);
            free(toFile);
        }
    }
    return 0;
}