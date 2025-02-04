package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the drop command, allowing the player to drop an item from their inventory into the current room.
 * 
 * <p>
 * This command checks if the player possesses the specified item and, if so, removes it from their inventory
 * and adds it to the current room. If the player does not have the item, an error message is returned.
 * </p>
 */
public class Drop extends Command {
    public CommandType commandType = CommandType.DROP;
    private String name;
    
    public Drop(String itemName){
        this.name = itemName;
    }

    public String execute(GameState gameState){
        Room currentRoom = gameState.getMap().getCurrentRoom();
        Player player = gameState.getPlayer();

        // check if player owns the object and add it to the room, removing it from player
        if (player.hasItem(name)){
            Item item = player.getItem(name);
            player.removeItem(item);
            currentRoom.addItem(item);
            return "You drop: " + name;
        } else if (player.hasEquipment(name)){
            Equipment equipment = player.getEquipment(name);
            player.removeEquipment(equipment);
            currentRoom.addEquipment(equipment);
            return "You drop: " + name;
        } else {
            return "You cannot drop " + name;
        }
    }

    public String toString(){
        return "Drop command: Item name ==> " +  name;
    }
   
}
