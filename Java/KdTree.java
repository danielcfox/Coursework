import edu.princeton.cs.algs4.Bag;
import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.RectHV;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

public class KdTree {

    private static class Node {
        public Point2D p;
        public RectHV rect;
        public Node lb;
        public Node rt;
        public int size;

        public Node(Point2D point, RectHV r) {
            if (point == null) throw new IllegalArgumentException();
            if (r == null) throw new IllegalArgumentException();
            this.p = point;
            this.rect = new RectHV(r.xmin(), r.ymin(), r.xmax(), r.ymax());
            this.size = 1;
        }

    }

    private Node root;

    public KdTree() {
        this.root = null;
    }                              // construct an empty set of points

    public boolean isEmpty() {
        return (this.root == null);
    } // is the set empty?

    private int size(Node node) {
        if (node == null) return 0;
        else return node.size;
    }

    public int size() {
        return (size(root));
    }                        // number of points in the set

    public void insert(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        root = insert(this.root, p, null, true, true);
    }             // add the point to the set (if it is not already in the set)

    private RectHV newRectHV(Node node, boolean isLB, boolean useX) {
        double xmin = 0.0;
        double ymin = 0.0;
        double xmax = 1.0;
        double ymax = 1.0;
        if (node != null) {
            xmin = node.rect.xmin();
            ymin = node.rect.ymin();
            xmax = node.rect.xmax();
            ymax = node.rect.ymax();
            if (useX && isLB) xmax = node.p.x();
            if (useX && !isLB) xmin = node.p.x();
            if (!useX && isLB) ymax = node.p.y();
            if (!useX && !isLB) ymin = node.p.y();
        }
        return new RectHV(xmin, ymin, xmax, ymax);
    }

    private Node insert(Node node, Point2D p, Node parent, boolean isLB, boolean useX) {
        if (node != null) {
            int xcmp = Double.compare(p.x(), node.p.x());
            int ycmp = Double.compare(p.y(), node.p.y());
            if ((useX && (xcmp < 0)) ||
                    (!useX && (ycmp < 0))) {
                node.lb = insert(node.lb, p, node, true, !useX);
            } else if ((xcmp != 0) || (ycmp != 0)) {
                node.rt = insert(node.rt, p, node, false, !useX);
            } else {
                node.size = size(node.lb) + size(node.rt) + 1;
                return node;
            }
            node.size = size(node.lb) + size(node.rt) + 1;
            return node;
        } else {
            return new Node(p, newRectHV(parent, isLB, !useX));
        }
    }

    private Node get(Node node, Point2D p, boolean useX) {
        if (node != null) {
            int xcmp = Double.compare(p.x(), node.p.x());
            int ycmp = Double.compare(p.y(), node.p.y());
            if (xcmp == 0 && ycmp == 0) {
                return node;
            }
            if ((useX && (xcmp < 0)) || (!useX && (ycmp < 0))) {
                return get(node.lb, p, !useX);
            } else {
                return get(node.rt, p, !useX);
            }
        }
        return null;
    }

    private Point2D get(Point2D p) {
        Node node = get(this.root, p, true);
        if (node != null) {
            return (node.p);
        }
        return null;
    }

    public boolean contains(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        return (get(p) != null);
    }           // does the set contain point p?

    private void draw(Node node, boolean useX) {
        if (node == null) return;
        // draw the point
        StdDraw.setPenColor(StdDraw.BLACK);
        StdDraw.setPenRadius(0.01);
        node.p.draw();

        // draw the line
        if (useX) {
            StdDraw.setPenColor(StdDraw.RED);
            StdDraw.setPenRadius();
            StdDraw.line(node.p.x(), node.rect.ymin(), node.p.x(), node.rect.ymax());
        } else {
            StdDraw.setPenColor(StdDraw.BLUE);
            StdDraw.setPenRadius();
            StdDraw.line(node.rect.xmin(), node.p.y(), node.rect.xmax(), node.p.y());
        }
        draw(node.lb, !useX);
        draw(node.rt, !useX);
    }

    public void draw() {
        draw(root, true);
    } // draw all points to standard draw

    private void rangeNode(RectHV rect, Node node, Bag<Point2D> inRange) {
        if (node == null) return;
        if (!rect.intersects(node.rect)) return;
        if (rect.contains(node.p)) inRange.add(node.p);
        rangeNode(rect, node.lb, inRange);
        rangeNode(rect, node.rt, inRange);
    }

    public Iterable<Point2D> range(RectHV rect) {
        if (rect == null) throw new IllegalArgumentException();
        Bag<Point2D> point2DInRange = new Bag<Point2D>();
        rangeNode(rect, root, point2DInRange);
        return point2DInRange;
    }            // all points that are inside the rectangle (or on the boundary)

    private Node nearestNode(Node node, Point2D p, Node curNearest) {
        if (node == null) return curNearest;
        if (p == null) return null;

        double thisDist;
        double curDist;

        if (curNearest == null) {
            // we are the root, init to root
            thisDist = curDist = p.distanceSquaredTo(node.p);
            curNearest = node;
        } else {

            double recDist = node.rect.distanceSquaredTo(p);
            curDist = p.distanceSquaredTo(curNearest.p);
            if (recDist > curDist) {
                return curNearest; // no need to traverse down this node
            }
            // check if this node gets us nearer
            thisDist = p.distanceSquaredTo(node.p);
            if (thisDist < curDist) {
                curDist = thisDist;
                curNearest = node;
            }

        }

        if (node.lb != null && node.lb.rect.contains(p)) {
            curNearest = nearestNode(node.lb, p, curNearest);
            curNearest = nearestNode(node.rt, p, curNearest);
        } else {
            curNearest = nearestNode(node.rt, p, curNearest);
            curNearest = nearestNode(node.lb, p, curNearest);
        }

        return curNearest;
    }

    public Point2D nearest(Point2D p) {
        if (p == null) throw new IllegalArgumentException();
        if (root == null) return null;
        Node node = nearestNode(root, p, null);
        return node.p;
    }            // a nearest neighbor in the set to point p; null if the set is empty

    public static void main(String[] args) {
        // initialize the data structures from file
        if (args[0] == null) throw new IllegalArgumentException();
        String filename = args[0];
        In in = new In(filename);
        KdTree kdtree = new KdTree();
        int size = 0;
        while (!in.isEmpty()) {
            double x = in.readDouble();
            double y = in.readDouble();
            Point2D p = new Point2D(x, y);
            if (kdtree.contains(p)) {
                StdOut.println("Contains point=" + p.toString());
            }
            kdtree.insert(p);
            size++;
            assert (kdtree.size() == size);
            if (!kdtree.contains(p)) {
                StdOut.println("Contains false point=" + p.toString());
            }
        }
        StdOut.println(kdtree.size());

    } // unit testing of the methods (optional)
}
