package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the get command, allowing the player to pick up an item from the current room and add it to their inventory.
 * 
 * <p>
 * This command checks if the specified item is present in the current room. If the item exists and the player
 * does not already have it, the item is added to the player's inventory and removed from the room. Otherwise,
 * an appropriate message is returned.
 * </p>
 */
public class Get extends Command {
    public CommandType commandType = CommandType.GET;
    private String itemName;

    public Get(String item){
        this.itemName = item;
    }

    public String execute(GameState gameState){
        Room currentRoom = gameState.getMap().getCurrentRoom();
        Player player = gameState.getPlayer();

        // checks if player already has object
        if (player.hasItem(itemName)){
            return "You already have " + itemName;
        } else if (player.hasEquipment(itemName)){
            return "You already have " + itemName;
        // if the room is not hidden and the room has object, adds object to player and remove from current room
        } else if (currentRoom.hasItem(itemName) && !currentRoom.getHidden()){
            Item item = currentRoom.getItemByName(itemName);
            currentRoom.removeItem(item);
            player.addItem(item);
            return "You pick up: " + itemName;
        } else if (currentRoom.hasEquipment(itemName) && !currentRoom.getHidden()){
            Equipment e = currentRoom.getEquipmentByName(itemName);
            currentRoom.removeEquipment(e);
            player.addEquipment(e);
            return "You pick up: " + itemName;
        } else {
            return "No " + itemName + " to get.";
        }
    }

    public String toString(){
        return "Get command: Item name ==> " +  itemName;
    }
   
}
