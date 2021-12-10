/******************************************************************************
 *  Compilation:  javac-algs4 Percolation.java
 *  Execution:    java-algs4 Percolation n
 *
 *  Implements Percolation problem
 *
 ******************************************************************************/

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.WeightedQuickUnionUF;

/* import edu.princeton.cs.algs4.StdStats; */

public class Percolation {

    private final WeightedQuickUnionUF uF;
    private boolean[][] open;
    private final int size;
    private int numOpenSites;

    public Percolation(int n) {
        if (n <= 0) {
            throw new IllegalArgumentException("Percolation:Percolation input out of range");
        }
        size = n;
        open = new boolean[n][n]; /* open already initialized to false */
        /* numOpenSites alrady initialized to 0 */
        uF = new WeightedQuickUnionUF((n * n) + 2);
        /* node 0 and node (n*n)+1 are phantom top and bottom, respectively */
        /* node number is n*row + col + 1 */
    }

    private boolean validateRowCol(int row, int col) {
        if (row <= size && row > 0 && col <= size && col > 0) {
            return true;
        }
        return false;
    }

    // opens the site (row, col) if it is not open already
    public void open(int row, int col) {

        if (!validateRowCol(row, col)) {
            throw new IllegalArgumentException("Percolation:open input out of range");
        }
        int rowidx = row - 1;
        int colidx = col - 1;
        if (open[rowidx][colidx]) return;
        open[rowidx][colidx] = true;
        numOpenSites++;
        int thisnodenum = (size * rowidx) + colidx + 1;
        int thatnodenum;
        /* if at top row, connect to phantom top node, else connect to higher node if open */
        if (rowidx == 0) {
            thatnodenum = 0; /* phantom top node */
            uF.union(thisnodenum, thatnodenum);
        } else if (isOpen(row - 1, col)) {
            thatnodenum = (size * (rowidx - 1)) + colidx + 1;
            uF.union(thisnodenum, thatnodenum);
        }
        /* if at bottom row, connect to phantom bottom node, else connect to lower node if open */
        if (rowidx == (size - 1)) {
            thatnodenum = (size * size) + 1; /* phantom bottom node */
            uF.union(thisnodenum, thatnodenum);
        } else if (isOpen(row + 1, col)) {
            thatnodenum = (size * (rowidx + 1)) + colidx + 1;
            uF.union(thisnodenum, thatnodenum);
        }
        /* connect to next left node if not leftmost */
        if (colidx != 0 && isOpen(row, col - 1)) {
            thatnodenum = (size * rowidx) + colidx;
            uF.union(thisnodenum, thatnodenum);
        }
        /* connect to next right node if not rightmmost */
        if (colidx != (size - 1) && isOpen(row, col + 1)) {
            thatnodenum = (size * rowidx) + colidx + 2;
            uF.union(thisnodenum, thatnodenum);
        }

    }

    // creates n-by-n grid, with all sites initially blocked
    // is the site (row, col) open?
    public boolean isOpen(int row, int col) {
        if (!validateRowCol(row, col)) {
            throw new IllegalArgumentException("Percolation:isOpen input out of range");
        }
        int rowidx = row - 1;
        int colidx = col - 1;
        return (open[rowidx][colidx]);
    }

    // is the site (row, col) full?
    public boolean isFull(int row, int col) {
        if (!validateRowCol(row, col)) {
            throw new IllegalArgumentException("Percolation:isFull input out of range");
        }
        int rowidx = row - 1;
        int colidx = col - 1;
        int thisnodenum = (size * rowidx) + colidx + 1;
        return (uF.find(thisnodenum) == uF.find(0)); /* 0 is top */
    }

    // returns the number of open sites
    public int numberOfOpenSites() {
        return numOpenSites;
    }

    // does the system percolate?
    public boolean percolates() {
        return uF.find(0) == uF.find((size * size) + 1);
    }

    // test client (optional)
    public static void main(String[] args) {
        int size = Integer.parseInt(args[0]);
        Percolation perc = new Percolation(size);
        while (!perc.percolates()) {
            int row = StdRandom.uniform(size) + 1;
            int col = StdRandom.uniform(size) + 1;
            if (perc.isOpen(row, col)) {
                StdOut.println("Site " + row + "," + col + " already opened");
            } else {
                perc.open(row, col);
            }
        }
        StdOut.println("percolated matrix of size " + size + " with " + perc.numberOfOpenSites() + " open sites");
    }
}
