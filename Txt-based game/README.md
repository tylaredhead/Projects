# Project: A text based game using OOP in java

## Overall description 
An interactive text based game using object orientated programming with 2 versions:
- [Version 1](#version-1): A score based game where the aim was to get the medallion and move it to the beach with the aim to get the highest score. Access to the code is [here](/Txt-based%20game/Version%201/).
- [Version 2](#version-2): A score based game where the machine can read in any text file obeying to a certain structure and enable the user to play each game. Access to the code is [here](/Txt-based%20game/Version%202/). This builds on version 1, improving the game as result of addressing the challenges as mentioned [here](#challenges).

For each version, run `sh run.sh` within the terminal or `./run.sh`. The table below depicts the available commands within each of the versions.

<table><tr>
<th>Version 1 commands</th>
<th>Version 2 commands</th>
</tr>
<tr><td>

- move &lt;direction&gt; 
- look || look &lt;feature&gt; || look &lt;item&gt; 
- inventory
- score 
- map 
- search &lt;feature&gt; 
- wear &lt;item&gt; 
- open &lt;feature&gt; 
- hint 
- cut 
- quit 

</td>
<td>

- move &lt;direction&gt;
- look room || look &lt;exit&gt; || look &lt;feature&gt; || look &lt;item&gt; || look &lt;equipment&gt; 
- status &lt;player&gt; || status &lt;inventory&gt; || status &lt;item&gt; || status &lt;equipment&gt; || status &lt;map&gt; || status score
- drop &lt;item&gt; || drop &lt;equipment&gt;
- get &lt;item&gt; || get &lt;equipment&gt;
- help || help &lt;command&gt;
- use &lt;equipment&gt; || use &lt;equipment&gt; on &lt;feature&gt;
- quit 
- combine &lt;item&gt; with &lt;item&gt; ==> creates an item or equipment

</td></tr></table>

## Version 1  
### Description  
This contains a terminal based user interface where the user can enter commands to pre-determined game format and environments, with the ability to:
- Interact with all aspects within the room including features, item and boundary objects such as cliffs and walls, (which was dynamically allocated as a feature even if not directly specified). This also includes opening doors or chests and cutting vines.
- Puzzles were added enabling score to be updated, completed by opening features by using the items within the inventory.
- Allows movement between room with the ability to display your current position and all rooms visited on a map.
- Allows the player to wear items to allow access to certain areas or use items to light up rooms in darkness, restricting commands if certain conditions were not met.
- Dynamically allocates access between rooms once all the rooms have been defined, validating through access for players movement.
- Enables the user to have hints to guide the player

### Challenges 
1. As the commands, room and features got larger, the scalability of the project was limited, particularly due to the manual update of each features to the room. 
2. Due to the limited number of classes, it was time consuming debugging as functions often had multiple purposes.

Given the challenges were due to the current implementation structure and design of the code, I started version 2 with these challenges in mind. 


## Version 2  
### Description
In terms of functionality, this is very similiar to version 1 with all features barring wearing items and cutting, however the structure is more dynamic utilising interfaces inheritance and composition, handling the scalablity of commands and features. Further functioanlity includes:
- Can read in any text file with a given structure and enable the user to play, dynamically creating a viewable map using breadth first search (BFS) as well as enabling a wide range of default and custom puzzles. In addition, it allows the user to print text or complete certain commands when certain constraints are met.
- Ability to merge items to get an item or equipment
- Handles greater sanitisation of inputs using ENUM constants for commands
- Allows the player to choose their name
- Allows points to be automatically added at the end if certain conditions are metthrough `bonus` in the txt file.

### Structure for txt files
The structure of the file is layered so the player is defined, followed by the map, before each room with everything within directly beneath it. At the bottom, the combine items are defined followed by the conditions and then the bonus. An example is:

```
player:<player name>
map:<map id>
room:<id>,<name>,<description>,<hidden>  
    equipment:<id>,<name>,<description>,<hidden>,<use action>,<use target>,<use result>,<use description>  
    container:<id>,<name>,<description>,<hidden>  
    item:<id>,<name>,<description>,<hidden>  
    exit:<id>,<name>,<description>,<next room>,<hidden>  
combine:<item id 1>,<item id 2>,<equipment id>,<equipment  name>,<equipment description>,<equipment hidden>,<equipment use action>,<equipment use target>,<equipment use result>,<equipment use description>  
combine:<item id 1>,<item id 2>,<item id 3>,<item  name>,<item description>,<item hidden>  
condition:<room id>,<command>=<display description>  
condition:<room id>,<display description>  
bonus:<score>,<item id 1>,<item id 2>, ...
```

All inputs are strings barring hidden which acts as a boolean so must be true or false, with **,** acting as delimiters.

### Specific technologies
Version 2 uses ENUM constants to allow sanitisation of commands, identifying the correct command class for the user action. This project also uses txt based libraries of `java.nio.file.*` and `java.io.*` to allow reading in the game designs.

### Challenges and future features
In terms of the challenges from version 1, due to the code being distributed into a wider range of classes, each with a single purpose, this enabled greater horizontal scalability such as adding new commands or features. Although each class is interdependent on other functions when the game is running, debugging was much more efficient, first debugging each function in isolation and then apart of the larger network of the classes.

Due to the large number of possible permutations of a `.txt` file that are valid, I initially restricted it to the specific format shown within [Structure for txt files](#structure-for-txt-files), however the game format was still restrictive. To allow more versatility of games being played, I added the feature to have an option to add conditions that would execute a command and output text, allowing greater variety.
 
## What did you learn
1. The importance of scalability initially even from the design stage, evident with the different structure implementations of the code between version 1 and 2. 
2. Time efficiency when debugging as functions are initially tested in isolation before being integrated.
2. Object orientated programming approach utilising interfaces, inheritance, composition and ENUM constants.
3. The use of libraries to read txt files.
4. Deepened own knowledge on a range of data structures and algorithms such as hash maps and BFS.
