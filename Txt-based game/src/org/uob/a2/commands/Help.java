package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the help command, providing the player with instructions or information
 * about various topics related to the game.
 * 
 * <p>
 * The help command displays information on how to play the game, including details about 
 * available commands, their syntax, and their purpose.
 * </p>
 */
public class Help extends Command {
    private String topic;
    
    public Help(String topic){
        super();
        this.topic = topic;
    }

    public String execute(GameState gameState){
        // default if no topic
        if (topic == null){
            String msg = "Welcome to the game! The commands include: \n" + 
                " - DROP - Drops and item from your inventory e.g (drop objName)\n" + 
                " - GET - Picks up an item from a room e.g (get objName)\n" + 
                " - HELP - Displays a help message in geneneral or on a specific command e.g (help or help command)\n" + 
                " - LOOK - Allows you to inspect either the room as a whole, exits, features or individual items or objects within the room e.g (look room or look exits or look features or look objName)\n" + 
                " - MOVE - Moves the player in a specific direction e.g (move direction) \n" + 
                " - QUIT - Quits the game e.g (quit)\n" + 
                " - STATUS - Displays current status to oen of the following: player, inventory, item, equipment, map or score e.g (status player or status inventory or status itemName/equipmentName or status map or status score)\n" + 
                " - USE - Uses an item in your inventory e.g (use equipmentName or use equipmentName on target) \n" + 
                " - COMBINE - combines two items together from the players inventory to form a item or equipment e.g (combine itemName1 with itemName2) \n";
            return msg;
        } else {
            // returns the string in relation to the specific command/topic
            switch (topic){
                case "move":
                    return "MOVE Command: Use the 'move' command to move in a specfic direction between rooms e.g (move direction)";
                case "drop":
                    return "DROP Command: Use the 'drop' command to drop an item from your inventory or equipment e.g (drop objName)";
                case "get":
                    return "GET Command: Use the 'get' command to pick up an item or equipment from your current room e.g (get objName)";
                case "look":
                    return "LOOK Command: Use the 'look' command to inspect a room, exit, feature, item or equipment within either the current room or player's inventory e.g (look room or look exits or look features or look objName)";
                case "quit":
                    return "QUIT Command: Use the 'quit' command to quit the game e.g (quit)";
                case "status":
                    return "STATUS Command: Use the 'status' command to display the current status of the player, inventory, score, map or the description of an item e.g (status player or status inventory or status itemName/equipmentName or status map or status score)";
                case "use":
                    return "USE Command: Use the 'use' command to use a piece of equipment on a object within the room or on a room e.g (use equipmentName or use equipmentName on target)";
                case "combine":
                    return "COMBINE Command: Use the 'combine' command to combine 2 items to get an item or equipment e.g (combine itemName1 with itemName2)";
                default:
                    return "No help available for the topic: " + topic;
            }           
        }
    }

    public String toString(){
        if (topic == null){
            return "Help command: Topic ==> null";
        }
        return "HELP command: Topic ==> " + topic;
    }
  
}
