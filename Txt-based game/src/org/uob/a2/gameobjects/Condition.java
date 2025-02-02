package org.uob.a2.gameobjects;

public class Condition{
    // if target is a number, it references a score condition such as game over when score is 0
    // else it is movement into a room when messages are displayed such as if you beat the game
    private String target;
    private String result;
    private String command;
    private boolean isDisp;

    
    public Condition(String target, String result){
        this.target = target;
        // prevents msg being displayed multiple times adj as score only decroments when moving
        this.isDisp = false;

        // enables command to be executed if required
        String[] input = result.split("=");
        if (input.length == 2){
            this.command = input[0];
            this.result = input[1];
        } else {
            this.result = result;
            this.command = "";
        }
    }

    public String getTarget(){
        return target;
    }

    public String getMsg(){
        // get command always called so isDisp is set there
        if (!isDisp){
            return result;
        }
        return "";
    }

    public void setNotDisp(){
        isDisp = false;
    }

    public String getCommand(){
        isDisp = true;
        return command;
    }
}
        
        

        