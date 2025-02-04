package org.uob.a1;

public class Score {
    private final int PUZZLE_VALUE = 10;
    private int startingScore; 
    private int currentScore;
    private int roomsVisited = 0;
    private int puzzlesSolved = 0;
    
    public Score(int startingScore){
        this.startingScore = startingScore;
        this.currentScore = startingScore;
    }

    public void visitRoom(){
        roomsVisited++;
    }

    public void solvePuzzle(){
        puzzlesSolved++;
    }

    public double getScore(){
        currentScore = startingScore - roomsVisited + puzzlesSolved*PUZZLE_VALUE;
        return currentScore;
    }
        
}