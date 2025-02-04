package org.uob.a1;

public class Position{
    public int x;
    public int y;
     
    public Position(int x, int y){
        this.x = x;
        this.y = y;
    }

    public void updateY(int increment){
        y += increment;
    }

    public void updateX(int increment){
        x += increment; 
    }

    
}