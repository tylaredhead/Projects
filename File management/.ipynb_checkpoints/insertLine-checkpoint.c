#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//For compiling "gcc insertLine.c validateFileName.c handleChangeLog.c -o insert"
//input (./insert fileName lineNumber "lineContent")

// enables importing of func from file validateFileName.c and handleChangeLog.c
int validateFileName(char *a, int n, const char *fileType);
int getLastNoOfLines(char *fileName);
void changeFileType(char *fileName);
int handleChangeLog(char *fileName, char *command, char *msg, int lineNo);

//inserts a line into a specific position
int insertLine(char* fileName, int lineNo, char* newLine) 
{
    FILE* fp = fopen(fileName, "r");
    if (!fp) 
    {
        printf("Error: File does not exist.\n");
        return 0;
    }

    FILE* temp = fopen("temp.txt", "w");
    if (!temp) 
    {
        printf("Error: Cannot create a temporary file.\n");
        fclose(fp);
        return 0;
    }

    char buffer[1024];
    int currentLine = 1;

    //copys the lines to temp file, inserting the new line at the specific position
    while (fgets(buffer, sizeof(buffer), fp)) 
    {
        if (currentLine == lineNo) 
        {
            //Inserts the new line
            fprintf(temp, "%s\n", newLine);
        }
        //Writes original line
        fprintf(temp, "%s", buffer);
        currentLine++;
    }

    //appends the new line if hasn't already been inserted
    if (lineNo >= currentLine) 
    {
        fprintf(temp, "\n%s", newLine);
    }

    fclose(fp);
    fclose(temp);

    //replaces the original file with the updated one
    remove(fileName);
    rename("temp.txt", fileName);

    printf("Line inserted at position %d.\n", lineNo);
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
    
    if (argc != 4) 
    {
        printf("Usage: ./insert fileName lineNumber \"content\"\n");
        return -1;
    }
    
    if ((extraChar = validateFileName(argv[1], strlen(argv[1]), fileType)) == -1)
    {
        printf("Invalid file name \n");
        return -1;
    }
    
    char *fileName = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
    char *fileNameLog = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
    int lineNo = atoi(argv[2]);
    char* newLine = argv[3];


    if (fileName == NULL || fileNameLog == NULL) 
    {
        printf("Error with memory allocation \n");
    } else 
    {
        strcpy(fileName, argv[1]);
        if (extraChar > 0)
        {
            fileName = strcat(fileName, fileType);
        }
        // gets the changelog file name by getting the .txt file type and converting 
        strcpy(fileNameLog, fileName);
        changeFileType(fileNameLog);

        if (!checkFileAlreadyExists(fileName))
        {
            printf("File does not exist.\n");
        } 
        else if (lineNo < 1 || (lineNo > getLastNoOfLines(fileNameLog) + 1)) 
        {
            printf("Invalid line number. Line numbers start at 1.\n");
        } 
        else if (insertLine(fileName, lineNo, newLine))
        {
            // converts to a log file type
            changeFileType(fileName);
            // gets the starting prompt adding the lineNo before concat the line entered by user
            char prompt[128];
            sprintf(prompt, "Line inserted on line %d. Line ==> ", lineNo);
            char *msg = (char *) malloc(sizeof(char)*(strlen(newLine) + strlen(prompt)));

            if (msg)
            {
                strcpy(msg, prompt);
                strcat(msg, newLine);
                handleChangeLog(fileName, "\nInsert line", msg, getLastNoOfLines(fileName) + 1);
                free(msg);
            }
        }
        free(fileName);
    }
    return 0;
}