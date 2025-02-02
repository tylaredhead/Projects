#include <stdio.h>
#include <dirent.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
// compile ==> gcc grep.c validateFileName.c -o grep
// input ==> ./grep fileName or ./grep 

// enables importing of func from file validateFileName.c
int validateFileName(char *a, int n, const char *fileType);

// updates the sting array subStr to contain the user's input
void getUserInput(char *subStr){
    printf("Please enter the substring you wish to find \n ==> ");
    fgets(subStr, sizeof(subStr), stdin);
    subStr[strlen(subStr) - 1] = '\0'; // removes \n 
    printf("\n");
}

// compares the substring with each line of the text file 
void checkForSubStr(char *fileName, char *subStr, int single){
    int lineNo = 1;
    
    FILE *fp = fopen(fileName, "r");;
    char *line;
    // for getline parameter ==> prevents potential wrap around if a len(buffer) < len(line
    long unsigned int len = 0;

    if (fp != NULL){
        // if user specified a single file 
        if (single){
            getUserInput(subStr);
        }
        
        while (1){
            // getline ==> realloc buffer to required size so memory efficient to size of line ==> auto
            if (getline(&line, &len, fp) == -1){
                break;
            } else {
                // compares the line with the subStr to display match
                if (strstr(line, subStr) != NULL){
                    printf("The %s lies within the file %s on line %d \n", subStr, fileName, lineNo);
                }

                lineNo++;
            }
        }
        fclose(fp);
        free(line);
    } else {
        printf("This file can not be read \n");
    }
}

// checks if the file type is .txt ==> returns 1 if correct else returns 0
int checkTxtFiles(char *fileName, int n){
    const char fileType[] = ".txt";
    // get pointer for pos of "." within file name
    char *pt = strchr(fileName, fileType[0]);

    if (pt != NULL){
        int i = 0;
        // checks if the file type matches up and no char after file type by comaparing memory address as contigous memory
        if (pt + strlen(fileType) == fileName + n){
            for (i; i < strlen(fileType); i++){
                if (*pt != fileType[i]){
                    return 0;
                }
                pt++;
            }
            return 1;
        }
    }
    return 0;
}

// gets all file name from the current directory
void checkAllFileNames(char *cwd, char *subStr){
    DIR *directory;
    struct dirent *file; // struct for file components
    directory = opendir(cwd); // opens directory 
    
    if (directory == NULL){
        printf("Error: the directory can not be opened");
    } else {
        int isReadingDir = 1;
        while (isReadingDir){
            // gets each file in sequence 
            file = readdir(directory);
            if (file != NULL){
                // gets name of the file from the struct
                char *fileName = file->d_name;
                if (checkTxtFiles(fileName, strlen(fileName))){
                    checkForSubStr(fileName, subStr, 0);
                }
            } else {
                // no more files to be checked
                isReadingDir = 0;
            }
        }
        closedir(directory);
    }
}

// this copies the contents of one string to another in memory
void copyString(char *from, char *to, int n){
    int i = 0;
    for (i; i < n; i++){
        to[i] = from[i];
    }
}

int main(int argc, char *argv[]) {
    char subStr[100];
    

    // checks if want to search all files or a single one for containing the substring
    if (argc == 1){
        getUserInput(subStr);
        // gets current working directory
        char cwd[1024];
        getcwd(cwd, sizeof(cwd));
        checkAllFileNames(cwd, subStr);
    } else if (argc == 2){
        const char *fileType = ".txt";
        int extraChar;

        // Checks if valid file name with correct file extensions
        if ((extraChar = validateFileName(argv[1], strlen(argv[1]), fileType)) == -1){
            printf("Invalid file name \n");
        } else {
        // add extra memory in case of extension of file type needing to be added on
            char *fileName = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
            if (fileName == NULL){
                printf("Error: memory allocation \n");
            } else {
                // Assigns the new memory the fileName with correct file type
                copyString(argv[1], fileName, strlen(argv[1]));
                if (extraChar > 0){
                    fileName = strcat(fileName, fileType);
                }
                
                checkForSubStr(fileName, subStr, 1);
            }
        }
    } else {
        printf("Usage: ./grep fileName or ./grep\n");
    }   
    return 0;
}
        
    

