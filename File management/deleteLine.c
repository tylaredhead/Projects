#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//For compiling  use "gcc DeleteLine.c ValidateFileName.c CheckFileExists.c -o deleteline"
//input (./deleteline fileName lineNumber)

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
int getLastNoOfLines(char *fileName);
void changeFileType(char *fileName);
int handleChangeLog(char *fileName, char *command, char *msg, int lineNo);

//deletes a specific line
int deleteLine(char* fileName, int lineNo, int fileLen) 
{
    FILE* fp = fopen(fileName, "r");
    if (!fp) 
    {
        printf("Error: File does not exist.\n");
        return 0;
    }

    //temporary file to store updates
    FILE* temp = fopen("temp.txt", "w");
    if (!temp) 
    {
        printf("Error: Cannot create a temporary file.\n");
        fclose(fp);
        return 0;
    }

    char buffer[1024];
    int currentLine = 1;

    // Copys lines to temp file (skips the line that is going to be deleted)
    while (fgets(buffer, sizeof(buffer), fp))
    {
        // if deleting last line, removes the new line so no new empty line beneath
        if (lineNo == fileLen && currentLine == lineNo -1)
        {
            buffer[strlen(buffer) - 1] = '\0';
        }
            
        if (currentLine != lineNo)
        {
            fprintf(temp, "%s", buffer); //writes the original line
        }
        currentLine++;
    }

    fclose(fp);
    fclose(temp);

    //replaces original file with the updated one
    remove(fileName);
    rename("temp.txt", fileName);

    printf("Line %d deleted.\n", lineNo);
    return 1;
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

int main(int argc, char* argv[]) 
{
    // Specifies fileType
    const char *fileType = ".txt";
    int extraChar;
    
    if (argc != 3)
    {
        printf("Usage: ./deleteline fileName lineNumber\n");
        return -1;
    }
    
    if ((extraChar = validateFileName(argv[1], strlen(argv[1]), fileType)) == -1)
    {
        printf("Invalid file name \n");
        return -1;
    }
    
    char *fileName = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
    char *fileNameLog = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
    // converts lineNo from string to int 
    int lineNo = atoi(argv[2]);

    if (fileName == NULL || fileNameLog == NULL) 
    {
        printf("Error with memory allocation \n");
    } 
    else 
    {
        // updates file type and copies to allocated memory
        strcpy(fileName, argv[1]);
        if (extraChar > 0)
        {
            fileName = strcat(fileName, fileType);
        }
        // gets the change log file by copying over the file entered and replacing file type
        strcpy(fileNameLog, fileName);
        changeFileType(fileNameLog);

        // check if file exists so line can be deleted
        if (!checkFileAlreadyExists(fileName))
        {
            printf("File does not exist.\n");
        } 
        else if (lineNo < 1 || lineNo > getLastNoOfLines(fileNameLog)) 
        {
            printf("Invalid line number. Line numbers start at 1.\n");
        } 
        else if (deleteLine(fileName, lineNo, getLastNoOfLines(fileNameLog)))
        {
            // converts to a log file type
            changeFileType(fileName);
            // gets the starting prompt adding the lineNo before concat the line added
            char msg[128];
            sprintf(msg, "Line deleted on line %d.", lineNo);
            handleChangeLog(fileName, "\nDelete line", msg, getLastNoOfLines(fileName) - 1);
        }
        free(fileName);
    }
    return 0;
}