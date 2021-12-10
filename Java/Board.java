/******************************************************************************
 *  Compilation:  javac Board.java
 *  Execution:    java Board
 *  Dependencies: In, Queue, StdOut
 *
 *  An immutable data type for a 3puzzle, 8puzzle, 15puzzle, etc. tile game board.
 *  For use on Coursera, Algorithms Part I programming assignment.
 *
 ******************************************************************************/

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.StdOut;

public class Board {

    private final int size;
    private final int numSlots; // includes 0 as a tile
    private final int[][] board;
    private final int[] row;
    private final int[] col;
    private int hamming;
    private int manhattan;

    // create a board from an n-by-n array of tiles,
    // where tiles[row][col] = tile at (row, col)
    public Board(int[][] tiles) {
        if (tiles == null) {
            throw new IllegalArgumentException();
        }
        this.size = tiles.length;
        this.numSlots = this.size * this.size;
        this.row = new int[numSlots];
        this.col = new int[numSlots];
        this.board = new int[this.size][this.size];
        int[] goalRow = new int[numSlots];
        int[] goalCol = new int[numSlots];
        int goalTileID = 0;

        for (int i = 0; i < this.size; i++) {
            if (tiles[i].length != this.size) {
                throw new IllegalArgumentException();
            }
            //         this.board[i] = new int[this.size];
            for (int j = 0; j < this.size; j++) {
                goalTileID++;
                if (goalTileID == numSlots) {
                    goalTileID = 0;
                }
                int tileID = tiles[i][j];
                this.board[i][j] = tileID;
                this.row[tileID] = i;
                this.col[tileID] = j;
                goalRow[goalTileID] = i;
                goalCol[goalTileID] = j;
            }
        }
        this.hamming = 0;
        this.manhattan = 0;
        for (int i = 1; i < this.numSlots; i++) {
            this.manhattan += Math.abs(this.row[i] - goalRow[i]);
            this.manhattan += Math.abs(this.col[i] - goalCol[i]);
            if (this.row[i] != goalRow[i] || this.col[i] != goalCol[i])
                this.hamming++;
        }
    }

    // string representation of this board
    public String toString() {
        StringBuilder s = new StringBuilder();
        s.append(this.size + "\n");
        for (int i = 0; i < this.size; i++) {
            for (int j = 0; j < this.size; j++) {
                s.append(String.format("%2d ", this.board[i][j]));
            }
            s.append("\n");
        }
        return s.toString();
    }

    // board dimension n
    public int dimension() {
        return this.size;
    }

    // number of tiles out of place
    public int hamming() {
        return this.hamming;
    }

    // sum of Manhattan distances between tiles and goal
    public int manhattan() {
        return this.manhattan;
    }

    // is this board the goal board?
    public boolean isGoal() {
        return (this.hamming == 0);
    }

    // does this board equal y?
    public boolean equals(Object y) {
        if (this == y) {
            return true;
        }
        if (y == null) {
            return false;
        }
        if (this.getClass() != y.getClass()) {
            return false;
        }
        Board that = (Board) y;
        if (that == null || this.size != that.size) {
            return false;
        }
        for (int i = 1; i < this.numSlots; i++) {
            if (this.row[i] != that.row[i] || this.col[i] != that.col[i]) {
                return false;
            }
        }
        return true;
    }

    private Board leftNeighbor() {
        if (this.col[0] != 0) {
            int emptyCol = this.col[0];
            int emptyRow = this.row[0];
            int leftTileNum = this.board[emptyRow][emptyCol - 1];
            return swap(0, leftTileNum);
        }
        return null;
    }

    private Board rightNeighbor() {
        if (this.col[0] != (this.size - 1)) {
            int emptyCol = this.col[0];
            int emptyRow = this.row[0];
            int rightTileNum = this.board[emptyRow][emptyCol + 1];
            return swap(0, rightTileNum);
        }
        return null;
    }

    private Board upNeighbor() {
        if (this.row[0] != 0) {
            int emptyCol = this.col[0];
            int emptyRow = this.row[0];
            int upTileNum = this.board[emptyRow - 1][emptyCol];
            return swap(0, upTileNum);
        }
        return null;
    }

    private Board downNeighbor() {
        if (this.row[0] != (this.size - 1)) {
            int emptyCol = this.col[0];
            int emptyRow = this.row[0];
            int downTileNum = this.board[emptyRow + 1][emptyCol];
            return swap(0, downTileNum);
        }
        return null;
    }

    // all neighboring boards
    public Iterable<Board> neighbors() {
        Queue<Board> nbs = new Queue<Board>();
        Board left = this.leftNeighbor();
        if (left != null) {
            nbs.enqueue(left);
        }
        Board right = this.rightNeighbor();
        if (right != null) {
            nbs.enqueue(right);
        }
        Board up = this.upNeighbor();
        if (up != null) {
            nbs.enqueue(up);
        }
        Board down = this.downNeighbor();
        if (down != null) {
            nbs.enqueue(down);
        }

        return nbs;
    }

    // a board that is obtained by exchanging any pair of tiles
    private Board swap(int n, int m) {
        int rown = this.row[n];
        int coln = this.col[n];
        int rowm = this.row[m];
        int colm = this.col[m];
        int[][] swapBoard = new int[this.size][this.size];
        for (int i = 0; i < this.size; i++) {
            for (int j = 0; j < this.size; j++) {
                swapBoard[i][j] = this.board[i][j];
            }
        }
        swapBoard[rown][coln] = this.board[rowm][colm];
        swapBoard[rowm][colm] = this.board[rown][coln];
        return new Board(swapBoard);
    }

    // a board that is obtained by exchanging any pair of tiles
    public Board twin() {
        return swap(1, 2);
    }

    // unit testing (not graded)
    public static void main(String[] args) {
        // create initial board from file
        In in = new In(args[0]);
        int n = in.readInt();
        int[][] tiles = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                tiles[i][j] = in.readInt();
        Board initial = new Board(tiles);
        Board twin = initial.twin();

        // create a goal board
        int[][] goalTiles = new int[n][n];
        int numTile = 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                goalTiles[i][j] = numTile;
                numTile++;
            }
        }
        goalTiles[n - 1][n - 1] = 0;
        Board goal = new Board(goalTiles);

        StdOut.printf("initial board dimension is %d\n", initial.dimension());
        StdOut.print(initial.toString());
        StdOut.printf("Hamming distance of initial board is %d\n", initial.hamming());
        StdOut.printf("Manhattan distance of initial board is %d\n", initial.manhattan());
        if (initial.isGoal()) {
            StdOut.println("initial board IS goal board");
        } else {
            StdOut.println("initial board is NOT goal board");
        }
        if (initial.equals(initial)) {
            StdOut.println("initial board equals itself");
        } else {
            StdOut.println("initial board does NOT equal itself");
        }
        StdOut.println();
        StdOut.printf("twin board dimension is %d\n", twin.dimension());
        StdOut.print(twin.toString());
        StdOut.printf("Hamming distance of twin board is %d\n", twin.hamming());
        StdOut.printf("Manhattan distance of twin board is %d\n", twin.manhattan());
        if (twin.isGoal()) {
            StdOut.println("twin board IS goal board");
        } else {
            StdOut.println("twin board is NOT goal board");
        }
        StdOut.println();
        StdOut.printf("goal board dimension is %d\n", goal.dimension());
        StdOut.print(goal.toString());
        StdOut.printf("Hamming distance of goal board is %d\n", goal.hamming());
        StdOut.printf("Manhattan distance of goal board is %d\n", goal.manhattan());
        if (goal.isGoal()) {
            StdOut.println("goal board IS goal board");
        } else {
            StdOut.println("goal board is NOT goal board");
        }

        if (initial.equals(initial)) {
            StdOut.println("initial board equals itself");
        } else {
            StdOut.println("initial board does NOT equal itself");
        }
        if (twin.equals(initial)) {
            StdOut.println("twin board equals initial");
        } else {
            StdOut.println("twin board does NOT equal initial");
        }
        if (goal.equals(initial)) {
            StdOut.println("goal board equals initial");
        } else {
            StdOut.println("goal board does NOT equal initial");
        }

        StdOut.println();
        StdOut.println("neighbors of initial board:\n");
        for (Board nb : initial.neighbors()) {
            StdOut.print(nb.toString());
        }

        StdOut.println();
        StdOut.println("neighbors of twin board:\n");
        for (Board nb : twin.neighbors()) {
            StdOut.print(nb.toString());
        }

        StdOut.println();
        StdOut.println("neighbors of goal board:\n");
        for (Board nb : goal.neighbors()) {
            StdOut.print(nb.toString());
        }

    }
}
