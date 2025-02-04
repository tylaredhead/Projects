package org.uob.a2;

import java.util.Scanner;
import java.nio.file.*;
import java.io.*;

import org.uob.a2.commands.*;
import org.uob.a2.gameobjects.*;
import org.uob.a2.parser.*;
import org.uob.a2.utils.*;

/**
 * Main class for the game application. Handles game setup, input parsing, and game execution.
 * 
 * <p>
 * This class initializes the game state, reads user input, processes commands, and maintains the game loop.
 * </p>
 */
public class Game {
    private static Tokeniser tokeniser;
    private static Parser parser;
    private static Scanner input;
    private static GameState gameState;

    
    public static void main(String[] args){
        setup();
        start();
    }
    
    public static void setup(){
        tokeniser = new Tokeniser();
        parser = new Parser();
        input = new Scanner(System.in);
        
        System.out.println("Enter game data file: ");
        String fileName = input.nextLine();
        
        System.out.println("\nLoading the game");
        // allows the txt file to be found within the data folder
        File file = new File("data/" + fileName);
        gameState = GameStateFileParser.parse(file.getAbsolutePath());
    }

    public static void start(){
        // check has to have not null player and map
        if (gameState != null && gameState.getMap() != null
            && gameState.getPlayer() != null && gameState.getMap().getCurrentRoom() != null){
            gameState.getMap().generateDispMap();

            String userInput;
            // if the name is input, the name is user defined
            if (gameState.getPlayer().getName().equals("input")){
                System.out.println("Please enter your player's name");
                userInput = input.nextLine();
                gameState.getPlayer().setPlayerName(userInput);
                System.out.println("");
            }
                
            String conditionResult, conditionUserInput;

            // enables inital outputs to be displayed onto the screen for the first room with the help message
            System.out.println("Use the 'help' command for any advice on commands in general or on a specific topic");
            tokeniser.tokenise(tokeniser.sanitise("look room"));
            try{
                executeCommand(gameState);
            }catch (CommandErrorException e){
                System.out.println(e.getMessage());
            }

            do{
                System.out.print(">> ");
                // gets commands from user
                userInput = input.nextLine();
                tokeniser.tokenise(tokeniser.sanitise(userInput));
                try{// check instance is move and then disp conditions 
                    executeCommand(gameState);

                    // if one of the conditions is valid, displays the result
                    if (!(conditionResult = gameState.checkConditions()).equals("")){
                        System.out.println(conditionResult + "\n");
                        conditionUserInput = gameState.getConditionCommand();
                        // runs the command if there is one for the given condition
                        if (!conditionUserInput.equals("")){
                            tokeniser.tokenise(tokeniser.sanitise(conditionUserInput));
                            executeCommand(gameState);
                            // for terminating condition of do-while
                            if (conditionUserInput.equals("quit")){
                                userInput = "quit";
                            }
                        }
                    }
                } catch (CommandErrorException e){
                    System.out.println(e.getMessage());
                }
                
            } while (!userInput.equals("quit"));

            if (gameState.getScore().getScore() != 0){
                System.out.println(gameState.updateScoreWithBonuses());
            }
            System.out.println("Your final score: " + gameState.getScore().getScore());
        }
    }
        

    public static void executeCommand(GameState gameState) throws CommandErrorException{
        Command command = parser.parse(tokeniser.getTokens());
        turn(command);
    }

    public static void turn(Command command){
        String result = command.execute(gameState);
        // adds new line if there wasnt one returned at the end of the string
        if (result.length() != 0 && result.charAt(result.length() - 1) != '\n'){
            result += "\n";
        }
        System.out.println(result);
    }
}
