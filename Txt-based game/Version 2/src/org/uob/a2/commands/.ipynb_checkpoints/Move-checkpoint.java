package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the move command, allowing the player to navigate to a different room in the game world.
 * 
 * <p>
 * The move command checks if the specified direction corresponds to an available exit in the current room.
 * If a matching exit is found, the player's location is updated to the connected room.
 * </p>
 */
public class Move extends Command {
    private String direction;
    
    public Move(String direction){
        super();
        this.direction = direction;
    }

    public String execute(GameState gameState){
        Room currentRoom = gameState.getMap().getCurrentRoom();

        Exit exit = currentRoom.getExitByName(direction); 
        // if the exits match up, set the current room, decrementing score and setting all condition msgs to be displayable
        if (exit != null && !exit.getHidden()){
            gameState.getMap().setCurrentRoom(exit.getNextRoom());
            gameState.getScore().visitRoom();
            gameState.updateConditionDisp();
            return "Moving towards " + direction + "\n";
        } else {
            return "No exit found in that direction.";
        }
    }

    public String toString(){
        return "Move command: Direction ==> " +  direction;
    }
  
}
