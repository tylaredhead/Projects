package org.uob.a1;

public class Player{
    private String[] wearing = new String[4];
    private Position currentPos; 

    public Player(Position currentPos){
        this.currentPos = currentPos;
    }

    public String wearItem(String item){
        for (int i = 0; i < wearing.length; i++){
            if (wearing[i] == null){
                wearing[i] = item;
                return "You are now wearing the " + item;
            }
        }
        return "There is no space left on your body to wear this";
    }

    public boolean ifWearing(String item){
        for (String wornItem: wearing){
            if (wornItem != null && wornItem.equalsIgnoreCase(item)){
                return true;
            }
        }
        return false;
    }

    public Position getPos(){
        return currentPos;
    }
}