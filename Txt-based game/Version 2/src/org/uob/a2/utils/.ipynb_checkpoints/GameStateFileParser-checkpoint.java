package org.uob.a2.utils;

import java.io.*;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.HashMap;

import org.uob.a2.gameobjects.*;
import org.uob.a2.commands.Combine;

/**
 * Utility class for parsing a game state from a file.
 * 
 * <p>
 * This class reads a structured text file to create a {@code GameState} object,
 * including the player, map, rooms, items, equipment, features, and exits.
 * </p>
 */
public class GameStateFileParser {
    private static Room currentRoom = null; // current room for adding features, items, equipment and exits
    private static Player player = null;
    private static Map map = null;
    private static Score score = null;
    private static int lineNo = 1; // checking correct order of certain arguments
    private static String startingRoomName = null; // so can set current room once the room has been parsed
    private static ArrayList<Condition> conditions = new ArrayList<Condition>();
    private static HashMap<String, Integer> bonusPoss = new HashMap<String, Integer>();
    
    public GameStateFileParser(){} 

    public static GameState parse(String filename){
        // assuming filePath is already absolute, check certain outputs are correct e.g boolean, check if next room exists
        
        setValues();
        Path filePath = Paths.get(filename);

        try{
            InputStream input = new BufferedInputStream(Files.newInputStream(filePath));
            BufferedReader reader = new BufferedReader(new InputStreamReader(input));

            // line structure obj:arguments
            String line = reader.readLine();

            while(line != null){
                // handles each line for each command
                String[] lineSegments = line.trim().split(":");
                if (lineSegments.length == 2){
                    switch (lineSegments[0]){
                        case "player":
                            addPlayer(lineSegments[1]);
                            break;
                        case "map":
                            addMap(lineSegments[1]);
                            break;
                        case "room":
                            addRoom(lineSegments[1]);
                            break;
                        case "item":
                            addItem(lineSegments[1]);
                            break;
                        case "equipment":
                            addEquipment(lineSegments[1]);
                            break;
                        case "container":
                            addContainer(lineSegments[1]);
                            break;
                        case "feature":
                            addFeature(lineSegments[1]);
                            break;
                        case "exit":
                            addExit(lineSegments[1]);
                            break;
                        case "score":
                            addScore(lineSegments[1]);
                            break;
                        case "condition":
                            addCondition(lineSegments[1]);
                            break;
                        case "combine":
                            addCombinedObj(lineSegments[1]);
                            break;
                        case "bonus":
                            addBonusPoss(lineSegments[1]);
                            break;                       
                    }
                    lineNo++;
                }
                line = reader.readLine();
            }  
        } catch (Exception e){
            System.out.println("Error: Couldn't load file\n");
            return null;
        }
        // map, player represent object or null depending on whether they were instantiated
        GameState gameState = new GameState(map, player);

        if (score != null){
            gameState.addScore(score);
        }

        for (Condition condition: conditions){
            gameState.addCondition(condition);
        }

        if (!bonusPoss.isEmpty()){
            gameState.addBonusPoss(bonusPoss);
        }
        
        System.out.println("File loaded\n");
        return gameState;
    }

    // resets as attributes are static and need to be independent of each method call
    public static void setValues(){
        currentRoom = null;
        player = null;
        map = null;
        lineNo = 1;
        startingRoomName = null;
        score = null;
        conditions = new ArrayList<Condition>();
        bonusPoss = new HashMap<String, Integer>();
    }
        
    // player line must be at very start of txt
    public static void addPlayer(String lineSegments){
        if (lineNo == 1){
            player = new Player(lineSegments);
        }
    }

    // map line must be at line 2 of txt
    public static void addMap(String lineSegments){
        if (lineNo == 2){
            map = new Map();
            startingRoomName = lineSegments;
        }
    }
    
    public static void addScore(String lineSegments){
        String[] args = lineSegments.split(",");
        int[] numArgs = new int[args.length];
        if (args.length == 2){
            try{
                numArgs[0] = Integer.parseInt(args[0]);
                numArgs[1] = Integer.parseInt(args[1]);
                score = new Score(numArgs[0], numArgs[1]);
            } catch (NumberFormatException e){
                throw e;
            }
        }
    }

    public static void addRoom(String lineSegments){
        if (lineNo >= 3 && map != null){
            String[] args = lineSegments.split(",");
            boolean hidden = args[3].equals("true");

            // allows optional room symbol for display map
            if ((args.length == 4 || args.length == 5) && (hidden || args[3].equals("false"))){
                Room room = new Room(args[0], args[1], args[2], hidden);
                if (args.length == 5 && args[4].length() == 1){
                    room.addDispSymbol(args[4].charAt(0));
                }
                
                map.addRoom(room);
                if (startingRoomName != null && startingRoomName.equals(args[0])){
                    map.setCurrentRoom(room.getId());
                }
                // sets to current room so all objects are placed in this new room
                currentRoom = room;
            }
        }
    }

    public static void addItem(String lineSegments){
        if (currentRoom != null){
            String[] args = lineSegments.split(",");
            boolean hidden = args[3].equals("true");
            // checks if hidden is 'true' or 'false' as 'hi' would set hidden ==> false
            if (args.length == 4 && (hidden || args[3].equals("false"))){
                Item item = new Item(args[0], args[1], args[2], hidden);
                currentRoom.addItem(item);
            }
        }
    }
    

    public static void addEquipment(String lineSegments){
        if (currentRoom != null){
            String[] args = lineSegments.split(",");
            boolean hidden = args[3].equals("true");
            // checks if hidden is 'true' or 'false' as 'hi' would set hidden ==> false
            if (args.length == 8 && (hidden || args[3].equals("false"))){
                UseInformation useInformation = new UseInformation(false, args[4], args[5], args[6], args[7]);
                Equipment equipment = new Equipment(args[0], args[1], args[2], hidden, useInformation);
                currentRoom.addEquipment(equipment);
            }
        }
    }

    public static void addContainer(String lineSegments){
        if (currentRoom != null){
            String[] args  = lineSegments.split(",");
            boolean hidden = args[3].equals("true");
            // checks if hidden is 'true' or 'false' as 'hi' would set hidden ==> false
            if (args.length == 4 && (hidden || args[3].equals("false"))){
                Container container = new Container(args[0], args[1], args[2], hidden);
                currentRoom.addFeature(container);
            }
        }
    }

    public static void addFeature(String lineSegments){
        if (currentRoom != null){
            String[] args  = lineSegments.split(",");
            boolean hidden = args[3].equals("true");
            // checks if hidden is 'true' or 'false' as 'hi' would set hidden ==> false
            if (args.length == 4 && (hidden || args[3].equals("false"))){
                Feature feature = new Feature(args[0], args[1], args[2], hidden);
                currentRoom.addFeature(feature);
            }
        }
    }

    public static void addExit(String lineSegments){
        if (currentRoom != null){
            String[] args = lineSegments.split(",");
            boolean hidden = args[4].equals("true");
            // checks if hidden is 'true' or 'false' as 'hi' would set hidden ==> false
            if (args.length == 5 && (hidden || args[4].equals("false"))){
                Exit exit = new Exit(args[0], args[1], args[2], args[3], hidden);
                currentRoom.addExit(exit);
            }
        }
    }

    public static void addCondition(String lineSegments){
        String[] args = lineSegments.split(",");
        if (args.length == 2){
            Condition condition = new Condition(args[0], args[1]);
            conditions.add(condition);
        }
    }
    
    public static void addCombinedObj(String lineSegments){
        String[] args = lineSegments.split(",");
        boolean hidden = args[5].equals("true");
        // checks if hidden is 'true' or 'false' as 'hi' would set hidden ==> false
        // args vary on length depending on if result of combine is item or equipment
        if (args.length == 6 && (hidden || args[5].equals("false"))){
            Item item = new Item(args[2], args[3], args[4], hidden);
            // allows items in different input combinations
            Combine.addItemComb(args[0], args[1], item);
            Combine.addItemComb(args[1], args[0], item);
        } else if (args.length == 10 && (hidden || args[5].equals("false"))){
            UseInformation useInformation = new UseInformation(false, args[6], args[7], args[8], args[9]);
            Equipment equipment = new Equipment(args[2], args[3], args[4], hidden, useInformation);
            // allows items in different input combinations
            Combine.addEquipmentComb(args[0], args[1], equipment);
            Combine.addEquipmentComb(args[1], args[0], equipment);
        }
    }

    public static void addBonusPoss(String lineSegments){
        String[] args = lineSegments.split(",");
        if (args.length >= 2){
            try{
                // adds the bonus score value specified for all id after the number
                int bonusScore = Integer.parseInt(args[0]);
                for (int i = 1; i<args.length; i++){
                    bonusPoss.put(args[i], bonusScore);
                }
            } catch (NumberFormatException e){
                throw e;
            }
        }
    }
            
                    
}
