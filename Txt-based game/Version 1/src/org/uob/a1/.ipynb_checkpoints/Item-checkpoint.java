package org.uob.a1;

public class Item{
    private String name;
    private String description;
    private boolean isWearable;
    
    public Item(String name, String description, boolean isWearable){
        this.name = name;
        this.description = description;
        this.isWearable = isWearable; 
    }

    public String getName(){
        return name;
    }

    public String getDescription(){
        return description;
    }

    public boolean isWearable(){
        return isWearable;
    } 
}