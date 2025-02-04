package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the use command, allowing the player to use equipment on a specific target in the game.
 * 
 * <p>
 * The use command checks if the player has the specified equipment and whether it can interact with
 * the target. The target can be a feature, item, or the current room, depending on the game context.
 * </p>
 */
public class Use extends Command {
    public CommandType commandType = CommandType.USE;
    private String equipmentName;
    private String target;

    public Use(String equipmentName, String target){
        this.equipmentName = equipmentName;
        this.target = target;
    }

    public String execute(GameState gameState){
        Player player = gameState.getPlayer();
        Room currentRoom = gameState.getMap().getCurrentRoom();

        Equipment e = player.getEquipment(equipmentName);
        if (e == null){
            return "You do not have " + equipmentName;
        }

        // checks if wanted to be use on room or on a specific item
        UseInformation useInformation = e.getUseInformation();
        if (useInformation.getAction().equals("use") || useInformation.getAction().equals("open")){
            if (target != null){
                GameObject object;
                if (currentRoom.hasFeature(target)){
                    object = currentRoom.getFeatureByName(target);
                } else if (currentRoom.hasItem(target)){
                    object = currentRoom.getItemByName(target);
                } else {
                    // check if target id matches an exit, else returns null
                    object = currentRoom.getExit(target);
                }
                
                if (object == null){ // as not feature or exit
                    return "Invalid use target";
                } else {
                    return e.use(object, gameState);
                }
            } else {
                // only can use if current room is room specified
                if (!useInformation.isUsed() && useInformation.getTarget().equals(currentRoom.getId())){
                    currentRoom.setHidden(false);
                    useInformation.setUsed(true);
                    return "You can see everything within the room";
                } else if (useInformation.isUsed()){
                    return "You have already used " + e.getName();
                } else {
                    return "Invalid use of item";
                }
            }
        } else {
            return "Invalid command for equipment";
        }
    }  

    public String toString(){
        return "Use command: Desc ==> " +  equipmentName + " on " + target;
    }
}
