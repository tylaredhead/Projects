# Project: A text based game using OOP in java

## Overall description 
An interactive text based game using object orientated programming with 2 versions:
- [Version 1](#version-1): A score based game where the aim was to get the medallion and move it to the beach filled with them with the aim to get the highest score. Access to the code is [here](/Txt-based%20game/Version%201/)
- [Version 2](#version-2): A score based game where the machine can read in any text file obeying to a certain structure and enable the user to play each game. Access to the code is [here](/Txt-based%20game/Version%202/)

### Version 1  
#### Description  
This contains a terminal based user interface where the user can enter commands to pre-determined game format and environments, with the ability to:
- Interact with all aspects within the room include features and item as well as dynamically allocating the boundary objects such as cliffs or wall depending on the room. This includes opening doors or chests and cutting vines.
- Puzzles enabling score to be updated, completed by opening features by using the items within the inventory.
- Allows movement between room with the ability to display your current position and all rooms visited on a map.
- Allows the player to wear items to prevent access or use items to light up rooms in darkness.
- Dynamically allocates access between rooms once all the rooms have been defined

### Version 2  
#### Description
In terms of functionality, this is very similiar to version 1, however the structure is more dynamic, handling the scalablity of commands and features.
- Can read in any text file with a given structure and enable the user to play, dynamically creating a viewable map using BFS as well as enabling a wide range of default and custom puzzles. In addition, it allows the user to print text or complete certain commands when certain constraints are met.



#### Other key features  
 

## How to use the project? 
For each version, run `sh run.sh` within the terminal or `./run.sh`. 

For version 2, you can both run the game and make your own text files for the game to run.


## Specific technologies
Although version1 does not use any specific technologies, version 2 uses Enums as well as text based librarie of `java.nio.file.*` and `java.io.*`


## Challenges and future features
Scalability and debugging of first one 
static 

initial time consuming to test and harder to test in isolation as more dependent on other functions 

## What did you learn
