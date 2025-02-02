#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//For compiling use "gcc showTotalLineNo.c ValidateFileName.c handleChangeLog.c -o showTotalLineNo"
//input (./showTotalLineNo fileName)

int validateFileName(char* a, int n, const char *fileType);
int getLastNoOfLines(char *fileName);
void changeFileType(char *fileName);

// prevents overwriting of files if one already exists ==> returns 1 if file can be read else 0
int checkFileAlreadyExists(char *fileName)
{
    FILE *fp;
    fp = fopen(fileName, "r");
    if (fp) 
    {
        fclose(fp);
        return 1;
    }
    return 0;
}

int main(int argc, char *argv[]) 
{
    const char *fileType = ".txt";
    int extraChar;
    
    if (argc != 2) 
    {
        printf("Usage: ./showTotalNoOfLines fileName\n");
        return -1;
    }
    else if ((extraChar = validateFileName(argv[1], strlen(argv[1]), fileType)) == -1)
    {
        printf("Invalid file name \n");
        return -1;
    }
    
    // allocates memory to account for file type extension if needed to be added
    char *fileName = (char *) malloc(sizeof(char)*(strlen(argv[1]) + extraChar));
    if (fileName == NULL) 
    {
        printf("Error with memory allocation \n");
    } 
    else 
    {
        // copies the fileName with the file type to the allocated memory
        strcpy(fileName, argv[1]);
        if (extraChar > 0)
        {
            fileName = strcat(fileName, fileType);
        }

        // check if the file exists
        if (!checkFileAlreadyExists(fileName))
        {
            printf("File does not exist.\n");
        } 
        else 
        {
            // changes fileType to .log to get total line no
            changeFileType(fileName);
            int totalLineNo = getLastNoOfLines(fileName);
            printf("Total line number is %d \n", totalLineNo);
        }
    }
    free(fileName);
    return 0;
}