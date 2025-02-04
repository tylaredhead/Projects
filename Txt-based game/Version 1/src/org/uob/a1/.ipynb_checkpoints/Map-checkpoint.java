package org.uob.a1;

public class Map {
    final private char EMPTY = '.';
    private char[][] mapArr; 
    private int width;
    private int height;
    private String displayString;
    
    public Map(int width, int height){
        this.width = width;
        this.height = height;
        this.mapArr = new char[height][width];
        
        // setting default char for each pos on map
        for (int i = 0; i < height; i++){
            for (int j = 0; j < width; j++){
                mapArr[i][j] = EMPTY;
            }
        }

        updateDisplayString();
    }

    public void placeRoom(Position pos, char symbol){
        if (pos.y < height && pos.x < width){
            mapArr[pos.y][pos.x] = symbol;
            updateDisplayString();
        }
    }

    public void updateDisplayString(){
        String tmp = "";

        for (int i = 0; i < mapArr.length; i++){
            for (int j = 0; j < mapArr.length; j++){
                tmp += mapArr[i][j];
            }
            tmp += "\n";
        }  
        displayString = tmp;
    }

    public String display(){
        return displayString;
    }
}