package org.uob.a2.parser;

import java.util.ArrayList;

/**
 * The {@code Tokeniser} class is responsible for converting a string input into a list of tokens
 * that can be parsed into commands by the game.
 * 
 * <p>
 * The tokeniser identifies keywords, variables, and special symbols, assigning each a {@code TokenType}.
 * </p>
 */
public class Tokeniser {
    private ArrayList<Token> tokens;

    public Tokeniser(){
        this.tokens = new ArrayList<Token>();
    }

    public ArrayList<Token> getTokens(){
        return tokens;
    }

    // uses scrolling window algorithm to remove spaces if prev is also a space, trimming and converting to lowercase
    public String sanitise(String s){
        s = s.trim();
        int i = 0;
        while (i < s.length()){
            if (s.charAt(i) == ' ' && s.charAt(i) == s.charAt(i - 1)){
                s = s.substring(0, i) + s.substring(i + 1);
            } else {
                i++;
            }
        }

        return s.toLowerCase();
    }
    
    public void tokenise(String s){
        // resets the token list
        this.tokens = new ArrayList<Token>();
        Token token = null;
        
        String[] words = s.split(" ");
        TokenType[] values = TokenType.values();

        for (String word: words){
            token = null;
            for (TokenType value: values){
                try{
                    // checks if the word is a command and instantiates the token
                    if (TokenType.valueOf(word.toUpperCase()) == value){
                        token = new Token(value, word);
                    } 
                } catch (Exception e){
                    // word can't be converted to TokenType so checks if it can be a prepsition alternative
                    if (word.equals("on") || word.equals("with") || word.equals("using")){
                        token = new Token(TokenType.PREPOSITION, word);
                    } 
                }
            }
            // only adds if no token already created
            if (token == null){
                token = new Token(TokenType.VAR, word);
            } 
            tokens.add(token);
        }

        // adds token to signify end of tokens
        token = new Token(TokenType.EOL);
        tokens.add(token);
    }
}
