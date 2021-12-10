/******************************************************************************
 *  Compilation:  javac-algs4 PercolationStats.java
 *  Execution:    java-algs4 PercolationStats n trials
 *
 *  Implements Percolation Stats problem
 *
 ******************************************************************************/

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {

    private final double[] x;
    private final int totalTrials;
    private final double conf95 = 1.96;
    private double xMean;
    private double xStddev;

    // perform independent trials on an n-by-n grid
    public PercolationStats(int n, int trials) {

        if (n < 0 || trials < 0) {
            throw new IllegalArgumentException("PercolationStats:PercolationStats input out of range");
        }
        x = new double[trials]; // fraction of open sites
        totalTrials = trials;
        int numClosed = n * n;
        int[] closedRow = new int[numClosed];
        int[] closedCol = new int[numClosed];

        for (int t = 0; t < totalTrials; t++) {
            numClosed = n * n;

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    int index = (i * n) + j;
                    closedRow[index] = i + 1;
                    closedCol[index] = j + 1;
                }
            }
            Percolation perc = new Percolation(n);
            while (!perc.percolates()) {
                // StdOut.println(numClosed);
                int site = StdRandom.uniform(numClosed);
                int row = closedRow[site];
                int col = closedCol[site];
                closedRow[site] = closedRow[numClosed - 1];
                closedCol[site] = closedCol[numClosed - 1];
                numClosed--;
                if (perc.isOpen(row, col)) {
                    throw new IllegalArgumentException("Site " + row + "," + col + " already opened");
                } else {
                    // StdOut.println("opening " + row + "," + col);
                    perc.open(row, col);
                }
            }
            x[t] = ((double) (perc.numberOfOpenSites())) / ((double) (n * n));
            // StdOut.printf("open sites %d, n squared %d, x[%d] = %.2f\n", perc.numberOfOpenSites(), n * n, t, x[t]);
        }
    }

    // sample mean of percolation threshold
    public double mean() {
        if (xMean == 0.0) {
            xMean = StdStats.mean(x);
        }
        return xMean;
    }

    // sample standard deviation of percolation threshold
    public double stddev() {
        if (xStddev == 0.0) {
            xStddev = StdStats.stddev(x);
        }
        return xStddev;
    }

    // low endpoint of 95% confidence interval
    public double confidenceLo() {
        return (mean() - ((conf95 * stddev()) / Math.sqrt(totalTrials)));
    }

    // high endpoint of 95% confidence interval
    public double confidenceHi() {
        return (mean() + ((conf95 * stddev()) / Math.sqrt(totalTrials)));
    }

    // test client (see below)
    public static void main(String[] args) {
        int size = Integer.parseInt(args[0]);
        int trials = Integer.parseInt(args[1]);
        if (size < 0 || trials < 0) {
            throw new IllegalArgumentException("PercolationStats:main input out of range");
        }

        PercolationStats percStats = new PercolationStats(size, trials);

        StdOut.println("mean                    = " + percStats.mean());
        StdOut.println("stddev                  = " + percStats.stddev());
        StdOut.println("95% confidence interval = [" + percStats.confidenceLo() + ", " + percStats.confidenceHi() + "]");

    }

}
