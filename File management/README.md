# Project: File management system

## Description - mention use of sqlite3
This project once compiled through a command line interface:
- Creates a file ([create.c](./create.c))
- Deletes a file ([delete.c](./delete.c))
- Adds a line in a file ([appendLine.c](./appendLine.c))
- Deletes a line in a file ([deleteLine.c](./deleteLine.c))
- Searches for a substr in a file ([grep.c](./grep.c))
- Records the users changes to the file, making it immutable to the user ([handleChangeLog.c](./handleChangeLog.c))
- Show the change log of the file ([showChangeLog.c](./showChangeLog.c))
- Show line(s) and total line number of the file ([showLine.c](./showLine), [showLines.c](./showLines.c), [showTotalLineNo.c](./showTotalLineNo.c))
- Validates the file name added to ensure a .txt ([validateFileName](./validateFileName.c))

## Getting started
Download a gcc compiler and use the command 'gcc fileName.c validateFileName.c checkFileExists.c -o alias' where the fileName.c is replaced by all file name excluding ones mentioned and alias is what compiled files name.

For example, 'gcc create.c validateFileName.c checkFileExists.c -o create'.

To run the individual commands once compiled, use './alias txtFileName'. For example, if there is a txt file of **hi.txt**, then './appendLine hi.txt' or './appendLine hi'.

## Challenges
- Design of the database - Initially, the plan was for more of a normalised database, however there was little data duplicity within the records. Therefore, by simplifying it, it reduced the complexity.

## What did i learn
1. The scalability and more efficient debugging long term with a more modular approach, breaking down the original main file
2. Databases - using sqlite3 to create a relational database, although the database was a single table, this taught me through research about normalisation as well as the framework, utilising SQL queries where appropiate, handling SQL injections.