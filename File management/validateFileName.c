#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// imported from other files

// checks if the file name has the correct file type ==> returns -1 if invalid else it returns the number of char that needed to be added for file type
int validateFileName(char *a, int n, const char *fileType){
    char *pt1 = strstr(a, fileType);
    char *pt2 = strchr(a, '.');

    // checks if file type is included
    if (pt1 != NULL){
        // checks the  .file type is at the end of the file name utilising contiguous memory
        if (pt1 + strlen(fileType) == a + n){
            return 0;
        }
        return -1;
    // checks if . is in the string, meaning different fileType than what required
    } else if (pt2 != NULL){
        return -1;
    } else {
        return strlen(fileType);
    }
}