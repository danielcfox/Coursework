/******************************************************************************
 *  Compilation:  javac Solver.java
 *  Execution:    java Solver filename
 *  Dependencies: In, MinPQ, Stack, StdOut, Board
 *
 *  An algorithm solution for a 3puzzle, 8puzzle, 15puzzle, etc. tile game board.
 *  For use on Coursera, Algorithms Part I programming assignment.
 *
 ******************************************************************************/

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.Stack;
import edu.princeton.cs.algs4.StdOut;

public class Solver {

    private SearchNode solution;

    private class SearchNode implements Comparable<SearchNode> {
        public Board board; // the board for this search node
        public SearchNode prev; // prev search node that led to this one
        public int moves; // moves to reach this node from initial
        public int priority;

        public SearchNode(Board board, SearchNode prev, int moves) {
            this.board = board;
            this.prev = prev;
            this.moves = moves;
            this.priority = moves + board.manhattan();
        }

        public int compareTo(SearchNode that) {
            if (this.priority < that.priority) {
                return -1;
            } else if (this.priority > that.priority) {
                return 1;
            }
            if (this.board.manhattan() < that.board.manhattan()) {
                return -1;
            } else if (this.board.manhattan() > that.board.manhattan()) {
                return 1;
            }
            if (this.board.hamming() < that.board.hamming()) {
                return -1;
            } else if (this.board.hamming() > that.board.hamming()) {
                return 1;
            }
            if (this.moves < that.moves) {
                return -1;
            } else if (this.moves > that.moves) {
                return 1;
            }
            return -1;
        }
    }

    // find a solution to the initial board (using the A* algorithm)
    public Solver(Board initial) {
        MinPQ<SearchNode> pq = new MinPQ<SearchNode>();
        MinPQ<SearchNode> pqT = new MinPQ<SearchNode>();
        SearchNode searchNode = new SearchNode(initial, null, 0);
        SearchNode searchNodeT = new SearchNode(initial.twin(), null, 0);
        pq.insert(searchNode);
        pqT.insert(searchNodeT);

        for (searchNode = pq.delMin(), searchNodeT = pqT.delMin();
             (searchNode != null && searchNodeT != null &&
                     !searchNode.board.isGoal() && !searchNodeT.board.isGoal());
             searchNode = pq.delMin(), searchNodeT = pqT.delMin()) {
            for (Board b : searchNode.board.neighbors()) {
                if (searchNode.prev == null || !b.equals(searchNode.prev.board)) {
                    SearchNode s = new SearchNode(b, searchNode, searchNode.moves + 1);
                    pq.insert(s);
                }
            }
            for (Board b : searchNodeT.board.neighbors()) {
                if (searchNodeT.prev == null || !b.equals(searchNodeT.prev.board)) {
                    SearchNode s = new SearchNode(b, searchNodeT, searchNodeT.moves + 1);
                    pqT.insert(s);
                }
            }
        }
        if (searchNode != null && searchNode.board.isGoal()) {
            this.solution = searchNode;
        } else {
            this.solution = null; // here just to make it clear solution is null if not solvable
        }
    }

    // is the initial board solvable? (see below)
    public boolean isSolvable() {
        return (this.solution != null);
    }

    // min number of moves to solve initial board
    public int moves() {
        if (this.solution != null) {
            return (this.solution.moves);
        }
        return -1;
    }

    // sequence of boards in a shortest solution
    public Iterable<Board> solution() {
        if (this.solution == null) {
            return null;
        }
        Stack<Board> bs = new Stack<Board>();
        for (SearchNode s = this.solution; s != null; s = s.prev) {
            bs.push(s.board);
        }
        return (bs);
    }

    // test client (see below)
    public static void main(String[] args) {

        // create initial board from file
        In in = new In(args[0]);
        int n = in.readInt();
        int[][] tiles = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                tiles[i][j] = in.readInt();
        Board initial = new Board(tiles);

        // solve the puzzle
        Solver solver = new Solver(initial);

        // print solution to standard output
        if (!solver.isSolvable())
            StdOut.println("No solution possible");
        else {
            StdOut.println("Minimum number of moves = " + solver.moves());
            for (Board board : solver.solution())
                StdOut.println(board);
        }
    }

}
