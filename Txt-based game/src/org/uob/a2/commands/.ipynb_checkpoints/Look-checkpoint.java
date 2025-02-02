package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the look command, allowing the player to examine various elements of the game world.
 * 
 * <p>
 * The look command can provide details about the current room, its exits, features, or specific items and equipment.
 * Hidden objects are not included in the output unless explicitly revealed.
 * </p>
 */
public class Look extends Command {
    public CommandType commandType = CommandType.LOOK;
    private String target;
    
    public Look(String target){
        this.target = target;
    }

    public String execute(GameState gameState){
        Room currentRoom = gameState.getMap().getCurrentRoom();
        String output;
        if (target.equals("room")){
            // check if you can see anything within the room
            if (currentRoom.getHidden()){
                output = "The room is in darkness, you can not see anything";
            } else {
                // displays room status as room is visible 
                output = "The " + currentRoom.getName() + ": " + currentRoom.getDescription();
                output += "\nYou can see: \n";
                output += " - Items - " + currentRoom.getInventoryInfo() + "\n";      
                output += " - Equipment - " + currentRoom.getEquipmentInfo();   
            }
        } else if (target.equals("features")){
            // check if you can see anything within the room
            if (currentRoom.getHidden()){
                output = "The room is in darkness, you can not see anything";
            } else {
                // displays feature name and description if room is visible 
                output = "You also see: " + currentRoom.getFeatureInfo();
            }
        } else if (target.equals("exits")){
            // displays exit name and description even if in darkness to exit room
            output = "The available exits are: " + currentRoom.getExitInfo();
        // gets individual descriptions of objects
        } else if (currentRoom.hasItem(target)){
            output = currentRoom.getItemByName(target).getDescription();
        } else if (currentRoom.hasFeature(target)){
            output = currentRoom.getFeatureByName(target).getDescription();
        } else if (currentRoom.hasEquipment(target)){
            output = currentRoom.getEquipmentByName(target).getDescription();
        } else if (currentRoom.hasExit(target)){
            output = currentRoom.getExitByName(target).getDescription();
        } else {
            System.out.println("Not a valid look object");
            output = "";
        }

        return output;
    }

    public String toString(){
        return "Look command: Target name ==> " +  target;
    }

}
