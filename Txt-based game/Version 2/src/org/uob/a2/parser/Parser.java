package org.uob.a2.parser;

import java.util.ArrayList;

import org.uob.a2.commands.*;

/**
 * The {@code Parser} class processes a list of tokens and converts them into {@code Command} objects
 * that can be executed by the game.
 * 
 * <p>
 * The parser identifies the type of command from the tokens and creates the appropriate command object.
 * If the command is invalid or incomplete, a {@code CommandErrorException} is thrown.
 * </p>
 */

public class Parser {
    private Command command;

    public Parser(){
        this.command = null;
    }
    
    public Command parse(ArrayList<Token> tokens) throws CommandErrorException{
        command = null;

        // condenses token so multiple var token type can be seen as a single token as allows user to 
        // enter names with more than one word
        tokens = condenseTokens(tokens);

        // accounts for inconsistency with EOL token
        int tokenNo = tokens.size();
        if (tokens.get(tokens.size() - 1).getTokenType() != TokenType.EOL){
            tokenNo++;
        }

        // checks conditions for each command for expected tokens
        // mult cases for use depending on if item wants to be used on a room or on a feature
        // as well as help for general and specific help for individual top
        if (tokenNo == 5){
            if (tokens.get(0).getTokenType() == TokenType.USE 
                && tokens.get(1).getTokenType() == tokens.get(3).getTokenType() 
                && tokens.get(1).getTokenType() == TokenType.VAR 
                && tokens.get(2).getValue().equals("on")){
                command = new Use(tokens.get(1).getValue(), tokens.get(3).getValue());
                command.commandType = CommandType.USE;
            } else if (tokens.get(0).getTokenType() == TokenType.COMBINE
                       && tokens.get(1).getTokenType() == tokens.get(3).getTokenType() 
                       && tokens.get(1).getTokenType() == TokenType.VAR
                       && tokens.get(2).getValue().equals("with")){
                command = new Combine(tokens.get(1).getValue(), tokens.get(3).getValue());
                command.commandType = CommandType.COMBINE;
            }
        } else if (tokenNo == 3){
            if (tokens.get(1).getTokenType() == TokenType.VAR){
                switch (tokens.get(0).getTokenType()){
                    case MOVE:
                        command = new Move(tokens.get(1).getValue());
                        command.commandType = CommandType.MOVE;
                        break;
                    case DROP:
                        command = new Drop(tokens.get(1).getValue());
                        command.commandType = CommandType.DROP;
                        break;
                    case GET:
                        command = new Get(tokens.get(1).getValue());
                        command.commandType = CommandType.GET;
                        break;
                    case LOOK:
                        command = new Look(tokens.get(1).getValue());
                        command.commandType = CommandType.LOOK;
                        break;
                    case STATUS:
                        command = new Status(tokens.get(1).getValue());
                        command.commandType = CommandType.STATUS;
                        break;
                    case USE:
                        command = new Use(tokens.get(1).getValue(), null);
                        command.commandType = CommandType.USE;
                        break;
                }
            } else if (tokens.get(0).getTokenType() == TokenType.HELP){
                    command = new Help(tokens.get(1).getValue());
                    command.commandType = CommandType.HELP;
            }
        } else if (tokenNo == 2){
            if (tokens.get(0).getTokenType() == TokenType.HELP){
                command = new Help(null);
                command.commandType = CommandType.HELP;
            } else if (tokens.get(0).getTokenType() == TokenType.QUIT){
                command = new Quit();
                command.commandType = CommandType.QUIT;
            }
        } 

        if (command == null){
            throw new CommandErrorException("Invalid command");
        } else {
            return command;
        }
    }

    public ArrayList<Token> condenseTokens(ArrayList<Token> tokens){
        TokenType prev = null;
        int i = 0;
        while (i < tokens.size()){
            if (prev == tokens.get(i).getTokenType()){
                tokens.get(i - 1).appendValue(" " + tokens.get(i).getValue());
                tokens.remove(i);
            } else {
                prev = tokens.get(i).getTokenType();
                i++;
            }
        }

        return tokens;
    }
}
