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
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

import java.util.Arrays;

public class BruteCollinearPoints {

    private final LineSegment[] segments;
    private final int segmentSize;

    public BruteCollinearPoints(Point[] points) {

        if (points == null) {
            throw new IllegalArgumentException("Input array cannot be null");
        }
        for (Point p : points) {
            if (p == null) {
                throw new IllegalArgumentException("Null point specified in array");
            }
        }

        Arrays.sort(points);

        Point prev = null;
        for (Point p : points) {
            if (prev != null) {
                if (p.compareTo(prev) == 0) {
                    throw new IllegalArgumentException("Input has redundant points");
                }
            }
            prev = p;
        }

        Bag<LineSegment> lsBag = new Bag<LineSegment>();
        for (int i = 0; i < points.length; i++) {
            for (int j = i + 1; j < points.length; j++) {
                for (int k = j + 1; k < points.length; k++) {
                    for (int l = k + 1; l < points.length; l++) {
                        Point p = points[i];
                        Point q = points[j];
                        Point r = points[k];
                        Point s = points[l];
                        if (Double.compare(p.slopeTo(q), p.slopeTo(r)) == 0 && Double.compare(p.slopeTo(r), p.slopeTo(s)) == 0) {
                            /* we have our four points */
                            /* add a line segment to our list */
                            lsBag.add(new LineSegment(p, s));
                        }
                    }
                }
            }
        }
        segmentSize = lsBag.size();
        segments = new LineSegment[segmentSize];
        int index = 0;
        for (LineSegment segment : lsBag) {
            segments[index++] = segment;
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
        BruteCollinearPoints collinear = new BruteCollinearPoints(points);
        for (LineSegment segment : collinear.segments()) {
            StdOut.println(segment);
            segment.draw();
        }
        StdDraw.show();
    }
}
