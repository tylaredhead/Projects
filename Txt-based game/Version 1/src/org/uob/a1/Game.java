package org.uob.a1;


import java.util.Scanner;  

public class Game {
    private static Room[][] Rooms = new Room[10][10];
    private static String[] commands = new String[2];
    private static Map map = new Map(10, 10);
    private static Score score = new Score(0);
    private static Inventory inventory = new Inventory();
    private static Player player;
    private static Room currentRoom;
    private static Item[] items = new Item[10];

    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        Position currentPos = new Position(5, 0);
        player = new Player(currentPos);
        String directionNeeded = "";
        
        createRooms();
        addFeatures();
        setAllAccess();
        createAllItems();
        initalRoomSetUp();
        
        do{
            System.out.print(">> ");
            commands = scanner.nextLine().trim().split(" ", 2);
            
            if (inventory.hasItem("a lamp") != -1 && currentRoom.hasAltDescription()){
                currentRoom.setDark();
                currentRoom.changeRoomDescription();
                score.solvePuzzle();
            }

            // changes command to be invalid if in dark other than if moving out of room or look
            boolean isCommandMove = !commands[0].equalsIgnoreCase("move");
            boolean isDirectionCorrect = commands.length == 2 && !commands[1].equalsIgnoreCase(directionNeeded);
            boolean canLook = commands[0].equalsIgnoreCase("look") && commands.length == 1;
            if ((currentRoom.isDark()) && !canLook && (isCommandMove || isDirectionCorrect)){
                commands[0] = "";
                System.out.println("You can not see anything, therefore ...");
            }
            
            switch (commands[0]){
                case "move": 
                    if (commands.length == 2){
                        directionNeeded = movePlayer(commands);
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "look":
                    if (commands.length == 1){
                        System.out.println(currentRoom.getDescription());
                    } else if (commands.length == 2){
                        descriptionForObjects(commands);
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "inventory":
                    if (commands.length == 1){
                        String inventoryStr = inventory.displayInventory();
                        if (inventoryStr.length() == 0){
                            System.out.println("You have nothing in your inventory");
                        } else {
                            System.out.println("Your inventory is: " + inventoryStr);
                        }
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "score":
                    if (commands.length == 1){
                        System.out.println("Your score is " + score.getScore());
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "map":
                    if (commands.length == 1){
                        System.out.println(map.display());
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "help":
                    if (commands.length == 1){
                        dispHelpMessage();
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "search":
                    if (commands.length == 2){
                        handleSearch(commands);
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "wear":
                    if (commands.length == 2){
                        handleWearingItem(commands);
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "open":
                    if (commands.length == 2){
                        handleOpenFeature(commands);
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "hint":
                    if (commands.length == 1){
                        System.out.println(currentRoom.giveHintForRoom());
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "cut":
                    if (commands.length == 2){
                        cutFeature(commands);
                    } else {
                        dispErrArgs();
                    }
                    break;
                case "quit":
                    System.out.println("Thank you for playing. Your score is: " + score.getScore());
                    break;
                default:
                    System.out.println("Invalid command entered");
            }

            // checks win conditions 
            if (inventory.hasItem("a medallion") != -1 && Rooms[8][3] == currentRoom){
                System.out.println("Well done, you solved all the puzzles and reunited all the medallions. Your score is " + score.getScore());
                commands[0] = "quit";
            }
        } while (!commands[0].equals("quit"));
    }

    public static void createRooms(){
        Rooms[0][5] = new Room("Grassland", "An empty grassland area. You are surrounded by cliffs on all sides except from a small path leading south", 'G', new Position(5, 0));
        Rooms[1][5] = new Room("Grassland", "A small path leads north surrounded by cliffs. To the north, there is an empty grassland area. The south leads to a crossroads.", 'G', new Position(5, 1));
        Rooms[2][5] = new Room("Grassland", "You reach a crossroads. To the north, there is a small path that leads through a grassland area. To the east, you can hear flowing water. To the west, the path leads onto some more grassland", 'G', new Position(5, 2));
        Rooms[2][6] = new Room("River bank", "You approach a river bank. To the south, the river bank continues adjacent to the river. To the north, a waterfall flows directly into the river below. However, the path to the waterfall, has long since eroded away.", 'R', new Position(6, 2)); 
        Rooms[3][6] = new Room("River bank", "The river bank continously leads south. A bush lies directly in front of you. The river to the east appears shallow but very slippery", 'R', new Position(6,3)); 
        Rooms[3][7] = new Room("Shoal", "You start to cross the river. To the north and south, the river is very deep, with the west having a river bank. To the east, there lies a river bank", 'S', new Position(7, 3));
        Rooms[3][8] = new Room("River bank", "You approach a river bank with all direction being surrounded by cliffs barring the west, which lies the river. There is some bushes to the east with a locked chest beside it.", 'R', new Position(8, 3));
        Rooms[2][4] = new Room("Grassland", "The path leads you west towards more grassland. To the east, lies the crossroads. Both the north and south are blocked by cliffs.", 'G', new Position(4, 2));
        Rooms[2][3] = new Room("Grassland", "The path ends by leading you to a forest, which is both to the south and west. The path continues to the east", 'G', new Position(3, 2));
        Rooms[2][2] = new Room("Forest", "You enter a forest with more forest to the south. The north and west are blocked by a dense forest and the east, there is the beginning of a path", 'F', new Position(2, 2)); 
        Rooms[3][3] = new Room("Forest", "The forest lies to the west and north of you. There appears to be a cabin in front of you but the door is locked. There is a wooden statue just to the left of the door", 'F', new Position(3, 3)); 
        Rooms[3][2] = new Room("Forest", "The forest lies to the north and east of you. The south and west are blocked by a dense forest. There lies some rocks by your feet", 'F', new Position(2, 3)); 
        Rooms[4][3] = new Room("Cabin - Kitchen", "You enter a cabin but it is too dark to see anything", 'K', new Position(3, 4)); 
        Rooms[6][3] = new Room("Garden", "The garden is fairly empty. To the north, there is the cabin. To the south, there is some castle ruins.", 'Y', new Position(3, 6)); 
        Rooms[5][3] = new Room("Cabin - Bedroom", "You stand in a bedroom that is fairly empty barring a bed and cupboard to the east. A door lies to the north, west and south.", 'B', new Position(3, 5)); 
        Rooms[7][3] = new Room("Castle Ruins", "You arrive at some castle ruins scattered around you. To the north, the garden lies. To the south, you hear waves behind a gate covered with vines.", 'C', new Position(3, 7)); 
        Rooms[5][2] = new Room("Bathroom/Toilet", "The bathroom is quite run down, with the only access being from the east. There is some pieces of paper on the floor.", 'T', new Position(2, 5));
        Rooms[8][3] = new Room("Beach", "You stand on the beach, with gold coins across the shore. To the north, there lies the castle ruins", 'W', new Position(3, 8));    

        Rooms[4][3].addAltDescription("The room before you is illuminated, a table lies in the centre along with a bottle on the floor. To the south and north, there lies a door, with wall to the east and west");
        Rooms[4][3].setDark();
    }
   
    public static void addFeatures(){
        final String[] EMPTYARR = {""};
        Rooms[2][6].addFeature("Waterfall", "The waterfall, although it appears to have a cave just behind where the water falls, this is not possible to get to", EMPTYARR, "", "O", "___");
        Rooms[3][6].addFeature("Bush", "The green bush lies directly infront of you with some brown shades towards the center", EMPTYARR, "boots", "O", "_S_");
        Rooms[3][3].addFeature("Door", "The locked door looks slightly overgrown but still functional", new String[]{"an old skeleton key"}, "", "LS", "OS_");
        Rooms[4][3].addFeature("Door", "The door looks worn with a fairly rough surface", EMPTYARR, "", "O", "OS_");
        Rooms[3][3].addFeature("Statue", "The wooden statue is covered in vines and vegetation, but it appears to be holding something that is glowing", EMPTYARR, "a lamp", "O", "_S_");
        Rooms[3][8].addFeature("Bushes", "The bushes lie to the east, growing adjacent and almost covering the chest", EMPTYARR, "a rusty key", "O", "_S_");
        Rooms[3][8].addFeature("Chest", "The locked chest sits adjacent to the bush with the iron rusting on all seeable components", new String[]{"a rusty key"}, "a medallion", "L", "OS_");
        Rooms[3][2].addFeature("Rocks", "The rocks are covered in moss to your feet, with small crevices along them", EMPTYARR, "an old skeleton key", "O", "_S_");
        Rooms[4][3].addFeature("Bottle", "A murky bottle which appears to have a piece of paper in it with some writing", EMPTYARR, "__45", "O", "_S_");
        Rooms[4][3].addFeature("Table", "A wooden table that lives in the middle of the room with a piece of paper underneath one table leg", EMPTYARR, "9___", "O", "_S_");
        Rooms[5][3].addFeature("Door", "Each door is worn with one door having a number pad on the door handle and currently being locked", new String[]{"9___", "_6__", "__45"}, "", "LS", "OS_");
        Rooms[6][3].addFeature("Door", "The door looks worn with a fairly rough surface", EMPTYARR, "", "O", "OS_");
        Rooms[5][2].addFeature("Door", "The door lies open with nothing of significance on it", EMPTYARR, "", "O", "OS_");
        Rooms[5][3].addFeature("Bed", "The bed lies in the centre of the room unmade, with something peeking out from under the bed", EMPTYARR, "a pair of scissors", "O", "_S_");
        Rooms[5][3].addFeature("Cupboard", "The cupboard lies in the east, missing all drawers", EMPTYARR, "", "O", "_S_");
        Rooms[5][2].addFeature("Floor", "The floor is fairly empty barring the piece of paper scattered around", EMPTYARR, "_6__", "O", "_S_");
        Rooms[7][3].addFeature("Vines", "The vines surround the gate from all angles, preventing it from being opened ", new String[]{"a pair of scissors"}, "", "LS", "_SC");
        Rooms[7][3].addFeature("Gate", "The gate is largely overgrown with vines locking the gate shut", EMPTYARR, "", "LS", "_S_");
        Rooms[8][3].addFeature("Gate", "The gate has vines covering its surface without hindering its function", EMPTYARR, "", "O", "OS_");
        Rooms[3][6].addFeature("Cliff", getDefaultDescription("cliff"), EMPTYARR, "", "LW", "___");
        Rooms[3][6].addFeature("Cliff", getDefaultDescription("cliff"), EMPTYARR, "", "LS", "___");
        Rooms[3][8].addFeature("Cliff", getDefaultDescription("cliff"), EMPTYARR, "", "LN", "___");
        Rooms[3][8].addFeature("Cliff", getDefaultDescription("cliff"), EMPTYARR, "", "LS", "___");
        Rooms[3][8].addFeature("Cliff", getDefaultDescription("cliff"), EMPTYARR, "", "LE", "___");
    }

    // setting all access, adding a default block for access prohibited
    public static void setAllAccess(){
        for (int y = 0; y < Rooms.length; y++){
            for (int x = 0; x < Rooms[0].length; x++){
                if (Rooms[y][x] != null){
                    if (y != 0 && Rooms[y-1][x] != null){
                        Rooms[y][x].setAccess('N');
                    } 
                    if (y != Rooms.length && Rooms[y+1][x] != null){
                        Rooms[y][x].setAccess('S');
                    } 
                    if (x != 0 && Rooms[y][x-1] != null){
                        Rooms[y][x].setAccess('W');
                    } 
                    if (x != Rooms[0].length && Rooms[y][x+1] != null){
                        Rooms[y][x].setAccess('E');
                    }
                    String roomName = Rooms[y][x].getName();
                    String defaultBlockName = getDefaultBlock(roomName);
                    Rooms[y][x].addDefaultBlock(defaultBlockName, getDefaultDescription(defaultBlockName));
                }
            }
        }
    }

    public static String getDefaultDescription(String defaultName){
        return "The " + defaultName + " has no prominant features";
    }

    // default block is dependent on the area
    public static String getDefaultBlock(String roomName){
        switch (roomName){
            case "Grassland": return "cliff";
            case "River bank": return "river";
            case "Shoal": return "river";
            case "Forest": return "dense forest";
            case "Cabin - Kitchen": return "wall";
            case "Garden": return "fence";
            case "Cabin - Bedroom": return "wall";
            case "Castle Ruins": return "remnant of a castle wall";
            case "Bathroom/Toilet": return "wall";
            case "Beach": return "body of water";
            default: return "";
        }
    }

    public static void createAllItems(){
        items[0] = new Item("boots", "A rather rugged boot that appears to be your size", true);
        items[1] = new Item("an old skeleton key", "A key which is slightly larger than ususal", false);
        items[2] = new Item("a lamp", "A brass lamp that illuminates enclosed areas", false);
        items[3] = new Item("a rusty key", "A key which is slightly smaller than ususal and mostly green", false);
        items[4] = new Item("a medallion", "A shiny medallion that is rather precious and valuable", false);
        items[5] = new Item("__45", "A piece of paper with __45 written on it", false);
        items[6] = new Item("9___", "A piece of paper with 9___ written on it", false);
        items[7] = new Item("_6__", "A piece of paper with _6__ written on it", false);
        items[8] = new Item("a pair of scissors", "A particularly long and sharp pair of scissors", false);
    }

    public static void initalRoomSetUp(){
        System.out.println("Your goal: find the medallion and bring it to the beach of gold coins");
        System.out.println("The help command details all possible commands \n");
        currentRoom = Rooms[player.getPos().y][player.getPos().x];
        System.out.println(currentRoom.getDescription());
        currentRoom.setVisited();
        map.placeRoom(player.getPos(), '@');
    }

    public static String movePlayer(String[] commands){
        commands[1] = commands[1].toLowerCase();
        switch (commands[1]){
            case "north": move('N', 0, -1); break;
            case "east": move('E', 1, 0); break;
            case "south": move('S', 0, 1); break;
            case "west": move('W', -1, 0); break;
            default: 
                System.out.println("Invalid direction entered for player to move");
        }
        if (currentRoom.isDark()){ // gets opposite direction to be only valid movement if dark
            return getOppositeDirection(commands[1]);
        }
        return "";
    }

    // checks if move is possible and updates all objects as required
    public static void move(char direction, int incX, int incY){
        if (!currentRoom.checkAccess(direction)) {
            System.out.println("You try and move " + commands[1].toLowerCase() + ", however you find a " + currentRoom.getBlockingFeature(direction) + " is blocking the way");
        } else if (Rooms[player.getPos().y + incY][player.getPos().x + incX].getName().equals("Shoal") && !player.ifWearing("Boots")){
            System.out.println("You do not have the right atire, try finding some more suitable for the terrain");
        } else {
            System.out.println("You moved " + commands[1]);
            map.placeRoom(player.getPos(), currentRoom.getSymbol());
            player.getPos().updateX(incX);
            player.getPos().updateY(incY);
            map.placeRoom(player.getPos(), '@');
            currentRoom = Rooms[player.getPos().y][player.getPos().x];
            
            if (!currentRoom.getVisited()){
                currentRoom.setVisited();
                score.visitRoom();
            }
        }
    }

    public static String getOppositeDirection(String direction){
        switch (direction.toLowerCase()){
            case "north": return "south";
            case "east": return "west";
            case "south": return "north";
            case "west": return "east";
            default: return "";
        }
    }

    // check if commands[1] is an item in inventory, else check room features and get description if poss
    public static void descriptionForObjects(String[] commands){
        int inventoryIdx = inventory.hasItem(commands[1]);
        if (inventoryIdx != -1){
            for (Item item: items){
                if (item != null && commands[1].equalsIgnoreCase(item.getName())){
                    System.out.println(item.getDescription());
                }
            }
        } else {
            int idxOfFeature = currentRoom.getIdx(commands[1]);
            if (idxOfFeature != -1 || currentRoom.getDefaultName().equalsIgnoreCase(commands[1])){
                System.out.println(currentRoom.getFeatureDescription(commands[1]));
            } else {
                dispErrUnknownObject();
            }
        }
    }

    // checks if not searchable and not locked and gets items, setting the feature as empty
    public static void handleSearch(String[] commands){
        int idxOfFeature = currentRoom.getIdx(commands[1]);
        if (idxOfFeature != -1){
            boolean canGetItems = currentRoom.canGetItemsInside(idxOfFeature);
            
            if (!canGetItems){
                System.out.println("The " + commands[1].toLowerCase() + " is still locked");
            } else if (!currentRoom.checkIfSearchable(idxOfFeature)){
                System.out.println("The item can't be searched");
            } else if (!inventory.hasSpaces()){
                System.out.println("You have too many items in your inventory");
            } else if (inventory.hasSpaces() && currentRoom.checkIfSearchable(idxOfFeature)){
                String itemName = currentRoom.getItems(idxOfFeature);
                
                if (itemName.equals("")){
                    System.out.println("You find no items within the " + commands[1].toLowerCase());
                } else {
                    System.out.println("You find " + itemName.toLowerCase() + " within the " + commands[1].toLowerCase());
                    inventory.addItem(itemName);
                }
            }
        } else if (currentRoom.getDefaultName().equalsIgnoreCase(commands[1])){
            System.out.println("You find nothing");
        } else {
            dispErrUnknownObject();
        }
    }

    public static void handleWearingItem(String[] commands){
        int idx = inventory.hasItem(commands[1]);
        if (idx == -1){
            System.out.println("This item does not exist in your inventory");
        } else {
            for (Item item: items){
                if (item != null && commands[1].equalsIgnoreCase(item.getName())){
                    if (item.isWearable()){
                        System.out.println(player.wearItem(commands[1]));
                        if (player.ifWearing(commands[1])){
                            inventory.removeItem(commands[1]);
                            score.solvePuzzle();
                        }
                    } else {
                        System.out.println("This item is not wearable");
                    }
                }
            }
        }
    }

    // checks if the item is openable and to unlock is in inventory and updates feature to open
    public static void handleOpenFeature(String[] commands){
        int idxOfFeature = currentRoom.getIdx(commands[1]);
        String[] itemToUnlock = currentRoom.getItemToUnlockFeature(commands[1]);
        if (itemToUnlock[0].equals("Invalid") && !(currentRoom.getDefaultName().equalsIgnoreCase(commands[1]))){
            dispErrUnknownObject();
        } else if (currentRoom.getDefaultName().equalsIgnoreCase(commands[1])){
            System.out.println("This is not openable");
        } else if (itemToUnlock[0].equals("") && currentRoom.checkIfOpenable(idxOfFeature)){
            System.out.println("The " + commands[1].toLowerCase() + " is already open");
        } else if (currentRoom.checkIfOpenable(idxOfFeature)){
            boolean hasItemToUnlock = true;
            for (String item: itemToUnlock){
                if (inventory.hasItem(item) == -1){
                    hasItemToUnlock = false;
                }
            }
            
            if (hasItemToUnlock){
                for (String item: itemToUnlock){
                    inventory.removeItem(item);
                }
                score.solvePuzzle();
            }
            System.out.println(currentRoom.openFeature(idxOfFeature, hasItemToUnlock));
        } else {
            System.out.println("This feature is not openable");
        }
    }
    
    public static void dispHelpMessage(){
        System.out.println(" Command ==> " +
                           "\n   move <direction> - shifts player in direction specified (north, east, south, west)" +
                           "\n   look             - describes the room " + 
                           "\n   look <feature>   - describes a particular feature within a room e.g chest" +
                           "\n   look <item>      - describes a specific item in inventory " + 
                           "\n   inventory        - displays your inventory" +
                           "\n   score            - displays your current score " + 
                           "\n   map              - displays the current map with symbols " +
                           "\n   search <feature> - searches a specific feature for an item " + 
                           "\n   wear <item>      - wear an item to allow access to area with specific conditions " +
                           "\n   open <feature>   - opens a feature to allow access to a room that was previously locked " + 
                           "\n   hint             - gives a hint based on the room " +
                           "\n   cut              - cuts an object to enable access to an area or feature " +
                           "\n   quit             - ends the game");
                           
    }

    // if the feature is cuttable, updates the feature and feature behind if conjoined, setting it as open
    public static void cutFeature(String[] commands){
        int idx = currentRoom.getIdx(commands[1]);
        if (idx != -1 || (currentRoom.getDefaultName().equalsIgnoreCase(commands[1]))){
            if (currentRoom.getDefaultName().equalsIgnoreCase(commands[1]) || !currentRoom.checkIfCuttable(idx)){
                System.out.println("This is not cuttable");
            } else if (inventory.hasItem("a pair of scissors") == -1){
                System.out.println("You have no items that can cut");
            } else {
                char featureLockedDirection = currentRoom.getFeatureLockedDirection(idx);
                currentRoom.setFeatureNotCuttable(idx);
                currentRoom.handleAffectedFeatures(idx);
                
                currentRoom.setAccess(featureLockedDirection);
                score.solvePuzzle();
                System.out.println("The " + commands[1] + " have mostly been cut");
                System.out.println("The gate is now open");
            }
        } else {
            System.out.println("This feature does not exist within this room");
        }
    }

    public static void dispErrArgs(){
        System.out.println("Invalid number of arguments for command");
    }

    public static void dispErrUnknownObject(){
        System.out.println("This does not exist within this room");
    }
}