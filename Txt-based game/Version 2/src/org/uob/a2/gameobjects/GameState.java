package org.uob.a2.gameobjects;

import java.util.ArrayList;
import java.util.HashMap;
/**
 * Represents the current state of the game, including the map and the player.
 * 
 * <p>
 * The game state contains all necessary information about the game's progress, such as
 * the player's status and the state of the game map.
 * </p>
 */
public class GameState {
    private Map map;
    private Player player;
    private Score score;
    private ArrayList<Condition> conditions;
    private HashMap<String, Integer> bonusScore;

    public GameState(Map map, Player player){
        this.map = map;
        this.player = player;
        this.score = new Score();
        this.conditions = new ArrayList<Condition>();
        this.bonusScore = new HashMap<String, Integer>();
    }

    // default constructor
    public GameState(){
        this.map = null;
        this.player = null;
        this.score = new Score();
        this.conditions = new ArrayList<Condition>();
        this.bonusScore = new HashMap<String, Integer>();
    }

    // Sets obj score to track changes
    public void addScore(Score score){
        this.score = score;
    }

    public Map getMap(){
        return map;
    }

    public Player getPlayer(){
        return player;
    }

    public Score getScore(){
        return score;
    }

    // Adds object condition, to be checked
    public void addCondition(Condition condition){
        conditions.add(condition);
    }

    // every time the player moves as only time decrement of score, check if any condition is valid and gets the message
    public String checkConditions(){
        int i = 0;
        while (i < conditions.size()){
            Condition condition = conditions.get(i);
            // checks condition first if score possibility and then checks room possibility
            if (Integer.toString(score.getScore()).equals(condition.getTarget())){
                return condition.getMsg();
            } else if (map.getCurrentRoom() != null && condition.getTarget().equals(map.getCurrentRoom().getId())){
                return condition.getMsg();
            }
            i++;
        }
        return "";
    }

    // sets conditions to not be diplayed to prevent same msg being displayed
    public void updateConditionDisp(){
        for (Condition condition: conditions){
            condition.setNotDisp();
        }
    }

    // if msg has been returned from checkCommands method, this is called to return the command from condition
    public String getConditionCommand(){
        int i = 0;
        while (i < conditions.size()){
            Condition condition = conditions.get(i);
            if (Integer.toString(score.getScore()).equals(condition.getTarget())){
                return condition.getCommand();
            } else if (map.getCurrentRoom() != null && condition.getTarget().equals(map.getCurrentRoom().getId())){
                return condition.getCommand();
            }
            i++;
        }
        return "";
    }

    // at end of game, check if any items give bonus points and update score
    public String updateScoreWithBonuses(){
        int result;
        String output = "";
        for (Item item: player.getInventory()){
            if ((result = bonusScore.getOrDefault(item.getId(), -1)) != -1){
                output += "Bonus: You have " + item.getName() + ", you get a bonus score of " + result + "\n";
                score.addBonus(result);
            }
        }
        return output;
    }

    // add items that can give bonuses
    public void addBonusPoss(HashMap<String, Integer> bonusPoss){
        bonusScore.putAll(bonusPoss);
    }
        
        
    /**
     * Returns a string representation of the game state, including the map and player details.
     *
     * @return a string describing the game state
     */
    @Override
    public String toString() {
        return "GameState {" +
               "map=" + (map != null ? map.toString() : "null") + ", " +
               "player=" + (player != null ? player.toString() : "null") +
               '}';
    }
}
