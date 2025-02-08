# Project: A text based game using OOP in java

## Overall description 
An interactive text based game using object orientated programming with 2 versions:
- [Version 1](#version-1): A score based game where the aim was to get the medallion and move it to the beach filled with them with the aim to get the highest score. Access to the code is [here](/Txt-based%20game/Version%201/).
- [Version 2](#version-2): A score based game where the machine can read in any text file obeying to a certain structure and enable the user to play each game. Access to the code is [here](/Txt-based%20game/Version%202/).

For each version, run `sh run.sh` within the terminal or `./run.sh`. 

<table><tr>
<th>Version 1 commands</th>
<th>Version 2 commands</th>
</tr>
<tr>
<td>
- move &lt;direction&gt; \n
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
- drop &lt;item&gt; || drop &lt;equipment&gt;
- get &lt;item&gt; || get &lt;equipment&gt;
- help || help &lt;command&gt;
- look room || look &lt;exit&gt; || look &lt;feature&gt; || look &lt;item&gt; || look &lt;equipment&gt; 
- move &lt;direction&gt;
- quit 
- status &lt;player&gt; || status &lt;inventory&gt; || status &lt;item&gt; || status &lt;equipment&gt; || status &lt;map&gt; || status score
- use &lt;equipment&gt; || use &lt;equipment&gt; on &lt;feature&gt;
- combine &lt;item&gt; with &lt;item&gt; ==&gt; creates an item or equipment
</td>
</tr></table>

### Version 1  
#### Description  
This contains a terminal based user interface where the user can enter commands to pre-determined game format and environments, with the ability to:
- Interact with all aspects within the room including features, item and boundary objects such as cliffs and walls, (which was dynamically allocated as a feature even if not directly specified). This also includes opening doors or chests and cutting vines.
- Puzzles were added enabling score to be updated, completed by opening features by using the items within the inventory.
- Allows movement between room with the ability to display your current position and all rooms visited on a map.
- Allows the player to wear items to allow access to certain areas or use items to light up rooms in darkness, restricting commands if certain conditions were not met.
- Dynamically allocates access between rooms once all the rooms have been defined, validating through access for players movement.
- Enables the user to have hints to guide the player


#### Challenges 
1. As the commands, room and features got larger, the scalability of the project was limited, particularly due to the munual update of each features to the room. 
2. Due to the limited number of classes, it was time consuming debugging as functions often had multiple purposes.

Given the challenges were due to the current implementation structure and design of the code, i started version 2 with these challenges in mind 



### Version 2  
#### Description
Focus on solving challenges form version 1
In terms of functionality, this is very similiar to version 1, however the structure is more dynamic, handling the scalablity of commands and features.
- Can read in any text file with a given structure and enable the user to play, dynamically creating a viewable map using BFS as well as enabling a wide range of default and custom puzzles. In addition, it allows the user to print text or complete certain commands when certain constraints are met.

// make own txt files

#### Other key features  
 



## Specific technologies
Although version1 does not use any specific technologies, version 2 uses Enums as well as text based librarie of `java.nio.file.*` and `java.io.*`


## Challenges and future features
Scalability and debugging of first one 
static 

initial time consuming to test and harder to test in isolation as more dependent on other functions 

## What did you learn
