package org.uob.a2.gameobjects;

public class Score{
    private int score;
    private final int PUZZLE_VALUE;
    
    public Score(int startingScore, int PUZZLE_VALUE){
        this.score = startingScore;
        this.PUZZLE_VALUE = PUZZLE_VALUE;
    }

    // default values if not specified
    public Score(){
        this.score = 0;
        this.PUZZLE_VALUE = 10;
    }

    public void visitRoom(){
        score--;
    }

    public void solvePuzzle(){
        score += PUZZLE_VALUE;
    }

    public int getScore(){
        return score;
    }   

    public void addBonus(int bonus){
        score += bonus;
    }  
}