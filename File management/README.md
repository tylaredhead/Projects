# Project: File management system

## Description - mention use of sqlite3
This project once compiled through a command line interface:
- Creates a file ([create.c](./create.c))
- Deletes a file ([delete.c](./delete.c))
- Adds a line in a file ([appendLine.c](./appendLine.c))
- Copies the contents of a file ([copy.c](./copy.c))
- Searches for a substr in a file ([grep.c](./grep.c))
- Records the users changes to the file, making it immutable to the user ([handleChangeLog.c](./handleChangeLog.c))
- Show the change log of the file ([showChangeLog.c](./showChangeLog.c))
- Show line(s) and total line number of the file ([showLine.c](./showLine), [showLines.c](./showLines.c), [showTotalLineNo.c](./showTotalLineNo.c))
- Validates the file name added to ensure a .txt ([validateFileName](./validateFileName.c))

## Getting started
Download a gcc compiler and use the command 'gcc fileName.c validateFileName.c checkFileExists.c -o alias' where the fileName.c is replaced by all file name excluding ones mentioned and alias is what compiled files name.

For example, 'gcc create.c validateFileName.c checkFileExists.c -o create'.

To run the individual commands once compiled, use './alias txtFileName' unless specified. For example, if there is a txt file of **hi.txt**, then './appendLine hi.txt' or './appendLine hi'. The other inforamtion is enetered after this initial command.
The exemptions are:
1. `./copy fromFileName toFileName`.
2. './grep fileName' - searches substring which is entered after inside a specific file.
3. './grep' - searches substring within the files within the current directory.

## Challenges
- Immutability of the changelog - Before the idea of using a .log, the idea was to reserve and alt name to the txt, however not only does this mean after every create command, this has to check all filenames for an existing changelog file that could contradict being time inefficient, it can also cause a reduced range of names as some will have to reserved. 


## What did i learn
1. Although a modular approach worked, there was a large amount of duplciity particularly when compiling due to 'handleChangeLog.c'. This meant although i considered the ability to directly use the command line when running, it showed the importance for simplifying the initial set up for the user.
2. The impacts of memory leaks when dealing with memory allocation, ensuring buffers can't be overloaded.