package org.uob.a2.gameobjects;

import java.util.ArrayList;
import java.util.Scanner;

public class Equipment extends GameObject implements Usable {
    protected UseInformation useInformation;
    protected Scanner input;

    public Equipment(String id, String name, String description, boolean hidden, UseInformation useInformation){
        super(id, name, description, hidden);
        this.useInformation = useInformation;
        // to enable password input
        this.input = new Scanner(System.in);
    }

    public UseInformation getUseInformation(){
        return useInformation;
    }

    public void setUseInformation(UseInformation useInformation){
        this.useInformation = useInformation;
    }

    public String use(GameObject target, GameState gameState){
        Room currentRoom = gameState.getMap().getCurrentRoom();

        // format of target if passcode - 'input-passcode=targetId'
        String[] targetInfo = useInformation.getTarget().split("=");
        boolean matchPasscode = false;
        // checks if input keyword for use input and checks the if correct password
        if (targetInfo.length == 2 && targetInfo[0].contains("input") && target.getId().equals(targetInfo[1])){
            System.out.print("Please enter the passcode: ");
            String userInput = input.nextLine();

            String passcode = targetInfo[0].split("-")[1];
            if (userInput.equals(passcode)){
                matchPasscode = true;
            } else {
                System.out.println("Incorrect password");
            }
            
        }

        // checks if the target specified is the correct target or is password correct from above
        if ((!useInformation.isUsed() && target.getId().equals(useInformation.getTarget()) && !currentRoom.getHidden()) || matchPasscode){
            // sets equipment to be used
            useInformation.setUsed(true);
            String result = useInformation.getResult();
            ArrayList<GameObject> allObj = currentRoom.getAll();

            // gets the result obj id and sets this to be visible
            for (GameObject obj: allObj){
                if (obj.getId().equals(result)){
                    obj.setHidden(false);
                }
            }

            // increments score and remove the equipment as already been used
            gameState.getScore().solvePuzzle();
            return useInformation.getMessage();
        } else if (currentRoom.getHidden()){
            return "You can't see anything \n";
        } else if (useInformation.isUsed()){
            return "You have already used " + name;
        }
        return "";
    }
    /**
     * Returns a string representation of this equipment, including the attributes inherited from {@code GameObject}
     * and the associated use information.
     *
     * @return a string describing the equipment
     */
    @Override
    public String toString() {
        return super.toString() + ", useInformation=" + useInformation;
    }
}
