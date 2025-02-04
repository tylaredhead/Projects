package org.uob.a1;

public class Inventory{
    final int MAX_ITEMS = 10;
    private String[] inventory;
    private int currentNoOfItems;
    
    public Inventory(){
        this.inventory = new String[10];
        this.currentNoOfItems = 0;
    }

    public void addItem(String item){ 
        if (currentNoOfItems != MAX_ITEMS){
            inventory[currentNoOfItems] = item;
            currentNoOfItems++; 
        }
    }

    public int hasItem(String item){
        for (int i = 0; i < MAX_ITEMS; i++){
            if (item.equals(inventory[i])){
                return i;
            }
        }
        return -1;
    }

    public void removeItem(String item){
        boolean found = false;
        for (int i = 0; i < MAX_ITEMS; i++){
            if (item.equals(inventory[i])){
                inventory[i] = inventory[currentNoOfItems - 1];
                found = true;
            } 
        }

        if (found){
            inventory[currentNoOfItems - 1] = null;
            currentNoOfItems--;
        }
    }

    public String displayInventory(){
        String inventoryStr = "";

        for (int i = 0; i < MAX_ITEMS; i++){
            if (inventory[i] != null){
                inventoryStr += inventory[i] + " ";
            }
        }
        return inventoryStr;
    }

    public boolean hasSpaces(){
        return (!(currentNoOfItems == MAX_ITEMS));

    }
   
}