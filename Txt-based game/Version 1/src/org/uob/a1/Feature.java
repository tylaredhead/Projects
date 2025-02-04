package org.uob.a1;

public class Feature{
    private String featureName;
    private String featureDescription;
    private String[] itemToUnlock;
    private String itemsInside;
    private String ifLocked; // LW, LE, O, LN, LS, L ==> L for locked, O for Open and rest is direction it prohibits
    private String properties; //[0]==>if openable, [1]- if searchable, [2] - if cuttable 
    
    public Feature(String featureName, String featureDescription, String[] itemToUnlock, String itemsInside, String ifLocked, String properties){
        this.featureName = featureName;
        this.featureDescription = featureDescription;
        this.itemToUnlock = itemToUnlock;
        this.itemsInside = itemsInside;
        this.ifLocked = ifLocked; 
        this.properties = properties; 
    }

    public void setItemsInside(String item){
        itemsInside = item;
    }

    public void setItemToUnlock(String[] items){
        itemToUnlock = items;
    }

    public void setLockStatus(String lockedStatus){
        ifLocked = lockedStatus;
    }

    public void setNotCuttable(){
        properties = properties.substring(0, 2) + "_";
    }

    public void setOpenable(){
        properties = "O" + properties.substring(1, 3);
    }

    public void changeDescription(String newDescription){
        featureDescription = newDescription;
    }

    // overrides depending on him replacing words or full description
    public void changeDescription(String origSubStr, String newSubStr){
        featureDescription = featureDescription.replace(origSubStr, newSubStr);
    }
    
    public String getFeatureName(){
        return featureName;
    }

    public String getFeatureDescription(){
        return featureDescription;
    }

    public String[] getItemToUnlock(){
        return itemToUnlock;
    }

    public String getItemsInside(){
        return itemsInside;
    }

    // only strs at len 2 if at [0] ==> L
    public char getLockedDirection(){
        if (ifLocked.length() == 2){
            return ifLocked.charAt(1);
        }
        return ' ';
    } 

    public Boolean getIfLocked(char direction){
        return (ifLocked.length() == 2 && ifLocked.charAt(1) == direction);
    }

    // gets name
    public String getFeaturePreventingAccess(char direction){
        if (getIfLocked(direction)){
            return featureName;
        }
        return "";
    }

    public boolean isOpenable(){
        return (properties.charAt(0) == 'O');
    }

    public boolean isSearchable(){
        return (properties.charAt(1) == 'S');
    }

    public boolean isCuttable(){
        return (properties.charAt(2) == 'C');
    }
}