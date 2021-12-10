import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.RectHV;
import edu.princeton.cs.algs4.SET;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class PointSET {

    private final SET<Point2D> point2DSet;

    public PointSET() {
        point2DSet = new SET<Point2D>();
    }                              // construct an empty set of points

    public boolean isEmpty() {
        return point2DSet.isEmpty();
    }                    // is the set empty?

    public int size() {
        return point2DSet.size();
    }                        // number of points in the set

    public void insert(Point2D p) {
        point2DSet.add(p);
    }             // add the point to the set (if it is not already in the set)

    public boolean contains(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        return point2DSet.contains(p);
    }           // does the set contain point p?

    public void draw() {
        for (Point2D p : point2DSet) {
            StdDraw.setPenRadius(0.01);
            p.draw();
        }
    }                        // draw all points to standard draw

    public Iterable<Point2D> range(RectHV rect) {
        if (rect == null) throw new IllegalArgumentException();
        SET<Point2D> point2DInRange = new SET<Point2D>();
        for (Point2D p : point2DSet) {
            if (rect.contains(p)) {
                point2DInRange.add(p);
            }
        }
        return point2DInRange;
    }            // all points that are inside the rectangle (or on the boundary)

    public Point2D nearest(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        Point2D nearestPoint = null;
        double nd = Double.POSITIVE_INFINITY;
        for (Point2D p1 : point2DSet) {
            double d = p.distanceSquaredTo(p1);
            if (Double.compare(d, nd) < 0) {
                nearestPoint = p1;
                nd = d;
            }
        }
        return nearestPoint;
    }            // a nearest neighbor in the set to point p; null if the set is empty

    public static void main(String[] args) {
        // initialize the data structures from file
        if (args[0] == null) throw new IllegalArgumentException();
        String filename = args[0];
        In in = new In(filename);
        PointSET brute = new PointSET();
        while (!in.isEmpty()) {
            double x = in.readDouble();
            double y = in.readDouble();
            Point2D p = new Point2D(x, y);
            brute.insert(p);
        }
        StdOut.println(brute.size());

    } // unit testing of the methods (optional)
}
