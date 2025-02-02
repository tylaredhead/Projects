package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;

/**
 * Represents the quit command, allowing the player to exit the game.
 * 
 * <p>
 * The quit command signals the end of the game session and provides a summary of the player's
 * current status before termination.
 * </p>
 */
public class Quit extends Command {
    public CommandType commandType = CommandType.QUIT;
    String gameOverMsg;
    String playerStatus;
    
    public Quit(){
        // default game over message
        gameOverMsg = "Game over: Your current status is: \n";
        playerStatus = "";
    }

    public String execute(GameState gameState){
        Player player = gameState.getPlayer();

        // gets player status and displays the current score
        playerStatus += "Player: " + player.getName() + "\n";
        playerStatus += " - Equipment: " + player.getEquipmentDesc() + "\n";
        playerStatus += " - Inventory: " + player.getInventoryDesc() + "\n";
        playerStatus += " - Final score is: " + gameState.getScore().getScore();
        return gameOverMsg + playerStatus;
    }

    public String toString(){
        return "Quit command";
    }
 
}
