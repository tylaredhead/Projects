package org.uob.a2.commands;

import org.uob.a2.gameobjects.*;
import java.util.ArrayList;
import java.util.HashMap;


public class Combine extends Command{
    // creates dictionary of all comb possibilites accessible to all objects of the class
    private static ArrayList<ArrayList<String>> combs = new ArrayList<ArrayList<String>>(); 
    private static ArrayList<Item> itemPoss = new ArrayList<Item>();
    private static ArrayList<Equipment> equipmentPoss = new ArrayList<Equipment>();
    
    private String part1;
    private String part2;
    
    public Combine(String part1, String part2){
        this.part1 = part1;
        this.part2 = part2;
    }

    // adds the combination from item + item ==> item
    public static void addItemComb(String inputItemId1, String inputItemId2, Item combinedItem){
        ArrayList<String> inputItems = new ArrayList<String>();
        inputItems.add(inputItemId1);
        inputItems.add(inputItemId2);
        inputItems.add(combinedItem.getId());
        combs.add(inputItems);
        itemPoss.add(combinedItem);
    }

    // adds the combination from item + item ==> equipment
    public static void addEquipmentComb(String inputItemId1, String inputItemId2, Equipment combinedEquipment){
        ArrayList<String> inputItems = new ArrayList<String>();
        inputItems.add(inputItemId1);
        inputItems.add(inputItemId2);
        inputItems.add(combinedEquipment.getId());
        combs.add(inputItems);
        equipmentPoss.add(combinedEquipment);
    }
        
    public String execute(GameState gameState){
        Player player = gameState.getPlayer();    

        // checks if items can be used by player
        if (player.hasItem(part1) && player.hasItem(part2)){
            Item part1Item = player.getItem(part1);
            Item part2Item = player.getItem(part2);

            for (ArrayList<String> comb: combs){
                // checks if items given from user is a valid comb
                if (comb.get(0).equals(part1Item.getId()) 
                    && comb.get(1).equals(part2Item.getId())){
                    // allows user to no longer use the existing items
                    player.removeItem(part1Item);
                    player.removeItem(part2Item);

                    // check the id to be equipment or item
                    String id = comb.get(2);
                    for (Equipment possEquipmentResult: equipmentPoss){
                        if (possEquipmentResult.getId().equals(id)){
                            player.addEquipment(possEquipmentResult);
                            return "The items have been combined ==> " + possEquipmentResult.getName();
                        }
                    }

                    for (Item possItemResult: itemPoss){
                        if (possItemResult.getId().equals(id)){
                            player.addItem(possItemResult);
                            return "The items have been combined ==> " + possItemResult.getName();
                        }
                    }
                }
            }
                    
            return "These items are not combinable";
            
        } else {
            return "You need to have the items before checking if they are combinable";
        }
    }
}