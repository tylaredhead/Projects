package org.uob.a1;

public class Room { 
    private String name;
    private String description;
    private char symbol;
    private Position position;
    private Feature defaultBlock;

    private int noOfFeatures = 0;
    private String altDescription = "";
    private boolean visited = false;
    private Feature[] features = new Feature[10];
    private boolean[] access = {false, false, false, false}; //0 ==> north, 1 ==> East, 2 = South, 3 = West
    private boolean isDark = false; // for darkness to limit commands
    
    public Room(String name, String description, char symbol, Position position){
        this.name = name;
        this.description = description;
        this.symbol = symbol;
        this.position = position;        
    }

    public void addFeature(String featureName, String featureDescription, String[] itemToUnlock, String itemsInside, String ifLocked, String properties){
        this.features[noOfFeatures] = (new Feature(featureName, featureDescription, itemToUnlock, itemsInside, ifLocked, properties));
        noOfFeatures++;
    }

    // for if no room in direction that player wants to go
    public void addDefaultBlock(String name, String description){
        this.defaultBlock = new Feature(name, description, new String[]{""}, "", "L", "___");
    }

    // restricts/enables movement in certain directions
    public void setAccess(char direction){
        boolean change = false;
        int idx = getIndexForAccess(direction);
        
        for (int i = 0; i < noOfFeatures; i++){
            boolean ifLocked = features[i].getIfLocked(direction);
            if (ifLocked && idx != -1){
                access[idx] = false;
                change = true;
            } 
        }
        
        if (!change){
            access[idx] = true;
        }
    }

    public String openFeature(int i, boolean hasItemToUnlock){
        if (hasItemToUnlock){
            char lockedDirection = features[i].getLockedDirection();
            features[i].setItemToUnlock(new String[]{""});
            features[i].setLockStatus("O");
            features[i].changeDescription("locked", "opened");
            if (lockedDirection != ' '){
                setAccess(lockedDirection);
            }
            return features[i].getFeatureName() + " is now open";
        } else {
            return features[i].getFeatureName() + " is still locked";
        }
    }

    public void changeFeatureDescription(int i, String description){
        features[i].changeDescription(description);
    }

    public String giveHintForRoom(){
        if (isDark){
            return "Maybe try and find a light";
        }
        
        for (int i = 0; i < noOfFeatures; i++){
            String[] itemsToUnlock = features[i].getItemToUnlock();
            if (!(itemsToUnlock[0].equals("") && itemsToUnlock.length == 1)){
                return "There may be more features to unlock";
            } else if (!features[i].getItemsInside().equals("")){
                return "There may be items lying around";
            }
        }
        return "Maybe try another room";
    }

    public boolean canGetItemsInside(int i){
        String[] itemsToUnlock = features[i].getItemToUnlock();
        return (itemsToUnlock[0].equals("") && itemsToUnlock.length == 1);
    }

    public Boolean checkAccess(char direction){
        int idx = getIndexForAccess(direction);
        if (idx == -1){
            return false;
        } else {
            return access[idx];
        }
    }

    // Changes properties of features if been cut, both the object being cut and the object directly behind if there is one
    public void handleAffectedFeatures(int origIdx){
        for (int i = 0; i < noOfFeatures; i++){
            if (origIdx != i && getFeatureLockedDirection(origIdx) == getFeatureLockedDirection(i)){
                features[i].setOpenable();
                features[i].changeDescription("The " + features[origIdx].getFeatureName() + " still has " + features[i].getFeatureName() + " covering it, however there are not many left");
                features[origIdx].changeDescription("The " + features[origIdx].getFeatureName() + " has mostly been cut away");
                features[origIdx].setLockStatus("O");
                features[i].setLockStatus("O");
                features[origIdx].setItemToUnlock(new String[]{""});
            }
        }
    }

    public void addAltDescription(String altDescription){
        this.altDescription = altDescription;
    }

    public boolean hasAltDescription(){
        return (!altDescription.equals(""));
    }

    public void changeRoomDescription(){
        description = altDescription;
        altDescription = "";
    }

    public boolean checkIfOpenable(int i){
        return features[i].isOpenable();
    }

    public boolean checkIfSearchable(int i){
        return features[i].isSearchable();
    }

    public boolean checkIfCuttable(int i){
        return features[i].isSearchable();
    }

    public void setVisited(){
        visited = true;
    }

    public void setFeatureNotCuttable(int i){
        features[i].setNotCuttable();
    }

    public void setDark(){
        isDark = !isDark;
    }
    
    public String getName(){
        return name;
    }

    public String getDescription(){
        return description;
    }

    public char getSymbol(){
        return symbol;
    }

    public Position getPosition(){
        return position;
    }

    public String getFeatureDescription(String featureName){
        int i = getIdx(featureName);
        if (i != -1){
            return features[i].getFeatureDescription();
        } else if (defaultBlock.getFeatureName().equalsIgnoreCase(featureName) && !fullyAccessible()){
            return defaultBlock.getFeatureDescription();
        } else {
            return "There is no " + features[i].getFeatureName() + " within this area";
        }
    }

    public char getFeatureLockedDirection(int i){
        char result = (i != -1) ? features[i].getLockedDirection(): ' ';
        return result;
    }

    // for the access array
    public int getIndexForAccess(char direction){
        switch (direction){
            case 'N': return 0;
            case 'E': return 1;
            case 'S': return 2;
            case 'W': return 3;
            default: return -1;
        }
    }

    // gets idx of feature from the list of features
    public int getIdx(String featureName){
        for (int i = 0; i < noOfFeatures; i++){
            if (features[i].getFeatureName().equalsIgnoreCase(featureName)){
                return i;
            }
        }
        return -1;
    }

    public String getItems(int i){
        String itemName = features[i].getItemsInside();
        features[i].setItemsInside("");
        return itemName;
    }
            
    public String[] getItemToUnlockFeature(String featureName){
        for (int i = 0; i < noOfFeatures; i++){
            if (features[i].getFeatureName().equalsIgnoreCase(featureName)){
                return features[i].getItemToUnlock();
            }
        }
        String[] invalidArr = {"Invalid"};
        return invalidArr;
    }

    // checks if any feature block direction before using default block and returns name
    public String getBlockingFeature(char direction){
        for (int i = 0; i < noOfFeatures; i++){
            String featureName = features[i].getFeaturePreventingAccess(direction);
            if (!featureName.equals("")){
                return featureName.toLowerCase();
            }
        }
        if (!fullyAccessible()){
            return defaultBlock.getFeatureName().toLowerCase();
        }
        return "";
    }

    public boolean fullyAccessible(){
        for (boolean val: access){
            if (!val){
                return false;
            }
        }
        return true;
    }

    public String getDefaultName(){
        return defaultBlock.getFeatureName();
    }
    
    public boolean getVisited(){
        return visited;
    }       

    public boolean isDark(){
        return isDark;
    }
}