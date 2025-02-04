package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the status command, allowing the player to retrieve information
 * about their inventory, specific items, or their overall status.
 * 
 * <p>
 * The status command can display a list of items in the player's inventory, 
 * provide details about a specific item, or show the player's general status.
 * </p>
 */
public class Status extends Command {
    public CommandType commandType = CommandType.STATUS;
    private String topic;

    public Status(String topic){
        this.topic = topic;
    }

    public String execute(GameState gameState){
        Player player = gameState.getPlayer();

        // displays object names from inventory and equipment
        if (topic.equals("inventory")){
            String playerItems = "";
            
            playerItems += " - Equipment: " + player.getEquipmentNames() + "\n";
            playerItems += " - Inventory: " + player.getInventoryNames();
            
            return "Inventory: \n" + playerItems;
        // displays planer name and inventory status as detailed above
        } else if (topic.equals("player")){
            String playerStatus = "";
            playerStatus += "Player: " + player.getName() + "\n";
            playerStatus += " - Equipment: " + player.getEquipmentNames() + "\n";
            playerStatus += " - Inventory: " + player.getInventoryNames();
            return playerStatus;
        } else if (topic.equals("score")){
            return "Your score is : " + gameState.getScore().getScore();
        } else if (topic.equals("map")){
            return "\n" + gameState.getMap().display();
        } else {
            String desc;
            // get item or equipment description
            if (player.hasItem(topic)){
                desc = topic + ": " + player.getItem(topic).getDescription();
            } else if (player.hasEquipment(topic)){
                desc = topic + ": " + player.getEquipment(topic).getDescription();
            } else {
                desc = "";
            }
            return desc;
        }
    }

    public String toString(){
        return "Status command: Topic name ==> " +  topic;
    }
}
