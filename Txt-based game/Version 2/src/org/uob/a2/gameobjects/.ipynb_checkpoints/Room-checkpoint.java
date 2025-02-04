package org.uob.a2.gameobjects;

import java.util.ArrayList;

/**
 * Represents a room in the game, which is a type of {@code GameObject}.
 * 
 * <p>
 * Rooms can have items, equipment, features, and exits. They also manage navigation
 * and interactions within the game world.
 * </p>
 */
public class Room extends GameObject {
    private ArrayList<Item> items = new ArrayList<Item>();
    private ArrayList<Equipment> equipment = new ArrayList<Equipment>();
    private ArrayList<Feature> features = new ArrayList<Feature>();
    private ArrayList<Exit> exits = new ArrayList<Exit>();
    private char displaySymbol; // for display map
    
    public Room(String id, String name, String description, boolean hidden){
        super(id, name, description, hidden);
        // default symbol is first character of the name
        this.displaySymbol = name.charAt(0);
    }

    @Override
    public void setName(String name){
        this.name = name;
    }

    @Override
    public void setDescription(String description){
        this.description = description;
    }

    @Override
    public String getName(){
        return name;
    }

    @Override
    public String getDescription(){
        return description;
    }

    public void addDispSymbol(char character){
        this.displaySymbol = character;
    }

    public char getDispSymbol(){
        return displaySymbol;
    }

    public ArrayList<Exit> getExits(){
        return exits;
    }

    public void addExit(Exit exit){
        exits.add(exit);
    }

    public ArrayList<Item> getItems(){
        return items;
    }

    // get item by the id
    public Item getItem(String id){
        for (Item item: items){
            if (item.getId().equals(id)){
                return item;
            }
        }
        return null;
    }

    public void removeItem(Item item){
        items.remove(item);
    }

    public Item getItemByName(String name){
        for (Item item: items){
            if (item.getName().equals(name)){
                return item;
            }
        }
        return null;
    }

    public Feature getFeatureByName(String name){
        for (Feature feature: features){
            if (feature.getName().equals(name)){
                return feature;
            }
        }
        return null;
    }

    public void removeFeature(Feature feature){
        features.remove(feature);
    }

    public ArrayList<Equipment> getEquipments(){
        return equipment;
    }
    
    public Equipment getEquipmentByName(String name){
        for (Equipment e: equipment){
            if (e.getName().equals(name)){
                return e;
            }
        }
        return null;
    }

    // gets equipment by id
    public Equipment getEquipment(String id){
        for (Equipment e: equipment){
            if (e.getId().equals(id)){
                return e;
            }
        }
        return null;
    }

    public void removeEquipment(Equipment e){
        equipment.remove(e);
    }

    // gets exits by id
    public Exit getExit(String id){
        for (Exit exit: exits){
            if (exit.getId().equals(id)){
                return exit;
            }
        }
        return null;
    }

    public Exit getExitByName(String name){
        for (Exit exit: exits){
            if (exit.getName().equals(name)){
                return exit;
            }
        }
        return null;
    }

    public void addEquipment(Equipment e){
        equipment.add(e);
    }

    // gets feature by id
    public Feature getFeature(String id){
        for (Feature feature: features){
            if (feature.getId().equals(id)){
                return feature;
            }
        }
        return null;
    }

    public void addItem(Item item){
        items.add(item);
    }

    public ArrayList<Feature> getFeatures(){
        return features;
    }

    // returns all objects
    public ArrayList<GameObject> getAll(){
        ArrayList<GameObject> temp = new ArrayList<GameObject>();
        temp.addAll(items);
        temp.addAll(equipment);
        temp.addAll(features);
        temp.addAll(exits);
        return temp;
    }

    public void addFeature(Feature feature){
        features.add(feature);
    }

    public boolean hasItem(String itemName){
        for (Item item: items){
            if (item.getName().equals(itemName)){
                return true;
            }
        }
        return false;
    }

    public boolean hasEquipment(String name){
        for (Equipment e: equipment){
            if (e.getName().equals(name)){
                return true;
            }
        }
        return false;
    } 

    public boolean hasFeature(String name){
        for (Feature feature: features){
            if (feature.getName().equals(name)){
                return true;
            }
        }
        return false;
    } 

    public boolean hasExit(String name){
        for (Exit exit: exits){
            if (exit.getName().equals(name)){
                return true;
            }
        }
        return false;
    } 

    // Gets inventory name and description, prepending , if another element that follows
    public String getInventoryInfo(){
        String inventoryInfo = "";
        boolean first = true;
        
        for (int i = 0; i<items.size(); i++){
            Item item = items.get(i);
            if (!item.getHidden()){
                if (first){
                    inventoryInfo += item.getName() + ": " + item.getDescription();
                    first = false;
                } else {
                    inventoryInfo += ", " + item.getName() + ": " + item.getDescription();
                }
            }
        }

        return inventoryInfo;
    }

    // Gets equipment name and description, prepending , if another element that follows
    public String getEquipmentInfo(){
        String equipmentInfo = "";
        boolean first = true;
        
        for (int i = 0; i<equipment.size(); i++){
            Equipment e = equipment.get(i);
            if (!e.getHidden()){
                if (first){
                    equipmentInfo += e.getName() + ": " + e.getDescription();
                    first = false;
                } else {
                    equipmentInfo += ", " + e.getName() + ": " + e.getDescription();
                }
            }
        }

        return equipmentInfo;
    }

    // Gets features name and description, prepending , if another element that follows
    public String getFeatureInfo(){
        String featureInfo = "";
        boolean first = true;
        
        for (int i = 0; i<features.size(); i++){
            Feature feature = features.get(i);
            if (!feature.getHidden()){
                if (first){
                    featureInfo += feature.getName() + ": " + feature.getDescription();
                    first = false;
                } else {
                    featureInfo += ", " + feature.getName() + ": " + feature.getDescription();
                }
            }
        }

        return featureInfo;
    }

    // Gets exit name and description, prepending , if another element that follows
    public String getExitInfo(){
        String exitInfo = "";
        boolean first = true;
            
        for (int i = 0; i<exits.size(); i++){
            Exit exit = exits.get(i);
            if (!exit.getHidden()){
                if (first){
                    exitInfo += exit.getName() + ": " + exit.getDescription();
                    first = false;
                } else {
                    exitInfo += ", " + exit.getName() + ": " + exit.getDescription();
                }
            }
        }

        return exitInfo;
    }
        
    /**
     * Returns a string representation of the room, including its contents and description.
     *
     * @return a string describing the room
     */
    @Override
    public String toString() {
        String out = "[" + id + "] Room: " + name + "\nDescription: " + description + "\nIn the room there is: ";
        for (Item i : this.items) {
            out += i + "\n";
        }
        for (Equipment e : this.equipment) {
            out += e + "\n";
        }
        for (Feature f : this.features) {
            out += f + "\n";
        }
        for (Exit e : this.exits) {
            out += e + "\n";
        }
        return out + "\n";
    }
}
