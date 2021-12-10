/******************************************************************************
 *  Compilation:  javac BruteCollinearPoints.java
 *  Execution:    java BruteCollinearPoints
 *  Dependencies: Point, LineSegment
 *
 *  An immutable data type for points in the plane.
 *  For use on Coursera, Algorithms Part I programming assignment.
 *
 ******************************************************************************/

import edu.princeton.cs.algs4.Bag;
import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Stack;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

import java.util.Arrays;

public class FastCollinearPoints {

    private LineSegment[] segments = null;
    private int segmentSize = 0;

    public FastCollinearPoints(Point[] points) {

        if (points == null) {
            throw new IllegalArgumentException("Input array cannot be null");
        }
        for (Point p : points) {
            if (p == null) {
                throw new IllegalArgumentException("Null point specified in array");
            }
        }

        Arrays.sort(points); // sort based on y, lowest first, then x, lowest first

        Point prev = null;
        for (Point p : points) {
            // StdOut.println(p);
            if (prev != null) {
                if (p.compareTo(prev) == 0) {
                    throw new IllegalArgumentException("Input has redundant points");
                }
            }
            prev = p;
        }


        // Bag<LineSegment> lsBag = new Bag<LineSegment>();
        Bag<CollinearLine> clBag = new Bag<CollinearLine>();
        for (int i = 0; i < points.length; i++) {
            Point[] otherPoints = new Point[points.length - i - 1];
            // System.arraycopy(points, 0, otherPoints, 0, i);
            // System.arraycopy(points, i + 1, otherPoints, i, points.length - i - 1);
            // Only need to check for remaining points in the array because we've already
            //    checked this point wrt the earler ones
            System.arraycopy(points, i + 1, otherPoints, 0, points.length - i - 1);
            Arrays.sort(otherPoints, points[i].slopeOrder());
            double curslope = Double.NEGATIVE_INFINITY;
            Stack<Point> pStack = new Stack<Point>();
            for (Point p : otherPoints) {
                double newslope = points[i].slopeTo(p);
                /* StdOut.println();
                StdOut.println(points[i]);
                StdOut.println(p); */
                if (Double.compare(newslope, curslope) == 0) {
                    // StdOut.println("slopes are equal");
                    pStack.push(p);
                } else {
                    // 4 or more in the pBag, then the top is the end of the line segment
                    // since we are ordered on increasing y
                    /* StdOut.println("slopes are not equal");
                    StdOut.printf("stack size %d", pStack.size()); */
                    if (pStack.size() >= 2) {
                        /* StdOut.printf("stack size %d", pStack.size());
                        StdOut.println("add to bag"); */
                        clBag.add(new CollinearLine(points[i], pStack.pop(), curslope));
                    }
                    // now empty the stack
                    while (pStack.size() > 0) {
                        pStack.pop();
                    }
                }
                // StdOut.println();
                curslope = newslope;
            }
            if (pStack.size() >= 2) {
                /* StdOut.printf("stack size %d", pStack.size());
                StdOut.println("add to bag"); */
                clBag.add(new CollinearLine(points[i], pStack.pop(), curslope));
                // now empty the stack
            }

            while (pStack.size() > 0) {
                pStack.pop();
            }
        }

        // StdOut.println(clBag.size());
        CollinearLine[] collinearLines = new CollinearLine[clBag.size()];
        int index = 0;
        for (CollinearLine cline : clBag) {
            // StdOut.println(cline.segment());
            collinearLines[index++] = cline;
        }
        Arrays.sort(collinearLines);

        LineSegment[] segs = null;
        int segSize = 0;
        CollinearLine curline = null;

        if (collinearLines.length > 0) {
            segs = new LineSegment[collinearLines.length];
            segs[0] = new LineSegment(collinearLines[0].start(), collinearLines[0].finish());
            segSize = 1;
            curline = collinearLines[0];
            for (int i = 1; i < collinearLines.length; i++) {
                if (!collinearLines[i].sameLine(curline)) {
                    segs[segSize++] = new LineSegment(collinearLines[i].start(), collinearLines[i].finish());
                    curline = collinearLines[i];
                }
            }
        }
        if (segs != null) {
            segmentSize = segSize;
            segments = new LineSegment[segmentSize];
            System.arraycopy(segs, 0, segments, 0, segmentSize);
        }
    }

    private class CollinearLine implements Comparable<CollinearLine> {
        private final Point start;
        private final Point finish;
        private final double slope;
        private final LineSegment segment;

        public CollinearLine(Point st, Point fn, double sl) {
            start = st;
            finish = fn;
            slope = sl;
            segment = new LineSegment(start, finish);
        }

        public LineSegment segment() {
            return segment;
        }

        public Point start() {
            return start;
        }

        public Point finish() {
            return finish;
        }

        public int compareTo(CollinearLine that) {
            // sort on slope first
            int dc = Double.compare(this.slope, that.slope);
            if (dc != 0) {
                return dc;
            }

            // sort on endpoint, so we have all same slope,
            // endpoint after each other
            int fincmp = this.finish.compareTo(that.finish);
            if (fincmp != 0) {
                return fincmp;
            } else {
                // sort on begin point, so lowest y will always
                // be first, so "duplicate" segments come after
                // if match slope and finish
                return (this.start.compareTo(that.start));
            }
        }

        public boolean sameLine(CollinearLine that) {
            if (Double.compare(this.slope, that.slope) == 0 && this.finish.compareTo(that.finish) == 0) {
                return true;
            }
            return false;
        }

    }

    public int numberOfSegments() {
        return (segmentSize);
    }

    public LineSegment[] segments() {
        LineSegment[] retsegs = new LineSegment[segmentSize];
        System.arraycopy(segments, 0, retsegs, 0, segmentSize);
        return (retsegs);
    }

    public static void main(String[] args) {

        // read the n points from a file
        In in = new In(args[0]);
        int n = in.readInt();
        Point[] points = new Point[n];
        for (int i = 0; i < n; i++) {
            int x = in.readInt();
            int y = in.readInt();
            points[i] = new Point(x, y);
        }

        // draw the points
        StdDraw.enableDoubleBuffering();
        StdDraw.setXscale(0, 32768);
        StdDraw.setYscale(0, 32768);
        for (Point p : points) {
            p.draw();
        }
        StdDraw.show();

        // print and draw the line segments
        FastCollinearPoints collinear = new FastCollinearPoints(points);
        if (collinear.segments() != null) {
            for (LineSegment segment : collinear.segments()) {
                StdOut.println(segment);
                segment.draw();
            }
            StdDraw.show();
        }
    }
}
