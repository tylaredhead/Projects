package org.uob.a2.gameobjects;

import java.util.ArrayList;

/**
 * Represents the player in the game, including their name, inventory, and equipment.
 * 
 * <p>
 * The player can carry items and equipment, interact with the game world, and perform
 * actions using their inventory or equipment.
 * </p>
 */
public class Player {
    private String name;
    private ArrayList<Item> inventory = new ArrayList<Item>();
    private ArrayList<Equipment> equipment = new ArrayList<Equipment>();
    
    public Player(String name){
       this.name = name;
   }

    public Player(){
        this.name = "";
    }

    public void setPlayerName(String name){
        this.name = name;
    }

    public String getName(){
        return name;
    }

    public ArrayList<Item> getInventory(){
        return inventory;
    }

    public boolean hasItem(String itemName){
        for (Item item: inventory){
            if (item.getName().equals(itemName)){
                return true;
            }
        }
        return false;
    }

    public Item getItem(String itemName){
        for (Item item: inventory){
            if (item.getName().equals(itemName)){
                return item;
            }
        }
        return null;
    }

    public void removeItem(Item item){
        inventory.remove(item);
    }

    public void addItem(Item item){
        inventory.add(item);
    }

    // gets all obj equipments
    public ArrayList<Equipment> getEquipment(){
        return equipment;
    }

    public boolean hasEquipment(String equipmentName){
        for (Equipment e: equipment){
            if (e.getName().equals(equipmentName)){
                return true;
            }
        }
        return false;
    }

    // get a single equipment - overloaded as different no of args
    public Equipment getEquipment(String equipmentName){
        for (Equipment e: equipment){
            if (e.getName().equals(equipmentName)){
                return e;
            }
        }
        return null;
    }

    public void removeEquipment(Equipment e){
        equipment.remove(e);
    }

    public void addEquipment(Equipment equipment){
        this.equipment.add(equipment);
    }

    // gets all equipment names and only prepends a comma if another element after 
    public String getEquipmentNames(){
        String equipmentNames = "";
        boolean first = true;
        
        for (Equipment e: equipment){
            if (first){
                equipmentNames += e.getName();
                first = false;
            } else {
                equipmentNames += ", " + e.getName();
            }
        }

        return equipmentNames;
    }

    // gets all inventory names and only prepends a comma if another element after 
    public String getInventoryNames(){
        String inventoryNames = "";
        boolean first = true;

        for (Item item: inventory){
            if (first){
                inventoryNames += item.getName();
                first = false;
            } else {
                inventoryNames += ", " + item.getName();
            }     
        }

        return inventoryNames;
    }

    // gets all equipment descriptions and only prepends a comma if another element after 
    public String getEquipmentDesc(){
        String equipmentDesc = "";
        boolean first = true;
        
        for (Equipment e: equipment){
            if (first){
                equipmentDesc += e.getDescription();
                first = false;
            } else {
                equipmentDesc += ", " + e.getDescription();
            }
        }

        return equipmentDesc;
    }

    // gets all inventory descriptions and only prepends a comma if another element after 
    public String getInventoryDesc(){
        String inventoryDesc = "";
        boolean first = true;
        
        for (Item item: inventory){
            if (first){
                inventoryDesc += item.getDescription();
                first = false;
            } else {
                inventoryDesc += ", " + item.getDescription();
            }
        }

        return inventoryDesc;
    }
        

    

    /**
     * Returns a string representation of the player's current state, including their name,
     * inventory, and equipment descriptions.
     *
     * @return a string describing the player, their inventory, and equipment
     */
    @Override
    public String toString() {
        StringBuilder out = new StringBuilder("Player Name: " + this.name + "\nInventory:\n");
        for (Item i : this.inventory) {
            out.append("- ").append(i.getDescription()).append("\n");
        }
        out.append("Equipment:\n");
        for (Equipment e : this.equipment) {
            out.append("- ").append(e.getDescription()).append("\n");
        }
        return out.toString();
    }
}
