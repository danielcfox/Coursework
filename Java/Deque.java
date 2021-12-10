/******************************************************************************
 *  Compilation:  javac-algs4 Deque.java
 *  Execution:    java-algs4 Deque
 *
 *  Implements Percolation problem
 *
 ******************************************************************************/

import edu.princeton.cs.algs4.StdOut;

import java.util.Iterator;

public class Deque<Item> implements Iterable<Item> {

    private Node first;
    private Node last;
    private int numItems;

    private class Node {
        Item item;
        Node prev;
        Node next;
    }

    // construct an empty deque
    public Deque() {
        first = null;
        last = null;
        numItems = 0;
    }

    // is the deque empty?
    public boolean isEmpty() {
        return (numItems == 0);
    }

    // return the number of items on the deque
    public int size() {
        return numItems;
    }

    // add the item to the front
    public void addFirst(Item item) {
        if (item == null) {
            throw new IllegalArgumentException();
        }
        Node oldfirst = first;
        first = new Node();
        first.item = item;
        first.next = oldfirst;
        first.prev = null;
        if (oldfirst != null) {
            oldfirst.prev = first;
        } else {
            last = first;
        }
        numItems++;
    }

    // add the item to the back
    public void addLast(Item item) {
        if (item == null) {
            throw new IllegalArgumentException();
        }
        Node oldlast = last;
        last = new Node();
        last.item = item;
        last.next = null;
        last.prev = oldlast;
        if (oldlast != null) {
            oldlast.next = last;
        } else {
            first = last;
        }
        numItems++;
    }

    // remove and return the item from the front
    public Item removeFirst() {
        if (isEmpty()) {
            throw new java.util.NoSuchElementException();
        }
        Item item = first.item;
        first = first.next;
        if (first != null) {
            first.prev = null;
        } else {
            last = null;
        }
        numItems--;
        return item;
    }

    // remove and return the item from the back
    public Item removeLast() {
        if (isEmpty()) {
            throw new java.util.NoSuchElementException();
        }
        Item item = last.item;
        last = last.prev;
        if (last != null) {
            last.next = null;
        } else {
            first = null;
        }
        numItems--;
        return item;
    }

    private class DequeIterator implements Iterator<Item> {
        private Node current = first;

        public boolean hasNext() {
            return current != null;
        }

        public void remove() {
            throw new UnsupportedOperationException();
        }

        public Item next() {
            if (current == null) {
                throw new java.util.NoSuchElementException();
            }
            Item item = current.item;
            current = current.next;
            return item;
        }
    }

    // return an iterator over items in order from front to back
    public Iterator<Item> iterator() {
        return new DequeIterator();
    }

    private static void printList(Deque<Integer> dq, String expected) {
        StdOut.printf("list (size %d, empty=%b): ", dq.size(), dq.isEmpty());
        for (int item : dq) {
            StdOut.printf(" %d", item);
        }
        StdOut.printf("\n");
        StdOut.printf("expected: %s\n", expected);
    }

    private static void printItem(int item, String operation) {
        StdOut.printf("item %d, %s\n", item, operation);
    }

    // unit testing (required)
    public static void main(String[] args) {
        Deque<Integer> dq = new Deque<Integer>();
        int item;

        dq.addFirst(1);
        printItem(1, "add first");
        printList(dq, "list (size 1, empty=false): 1");
        item = dq.removeFirst();
        printItem(item, "removed first");
        printList(dq, "list (size 0, empty=true): ");
        dq.addLast(5);
        printItem(5, "add last");
        printList(dq, "list (size 1, empty=false): 5");
        item = dq.removeLast();
        printItem(item, "removed last");
        printList(dq, "list (size 0, empty=true): ");
        dq.addFirst(2);
        dq.addLast(3);
        dq.addLast(4);
        dq.addFirst(1);
        printList(dq, "list (size 4, empty=false): 1 2 3 4");
        for (int i = 0; i < 4; i++) {
            item = dq.removeFirst();
            printItem(item, "removed first");
        }
        printList(dq, "list (size 0, empty=true): ");
        dq.addFirst(2);
        dq.addLast(3);
        dq.addLast(4);
        dq.addFirst(1);
        printList(dq, "list (size 4, empty=false): 1 2 3 4");
        for (int i = 0; i < 4; i++) {
            item = dq.removeLast();
            printItem(item, "removed last");
        }
        printList(dq, "list (size 0, empty=true): ");
        dq.addFirst(2);
        dq.addLast(3);
        dq.addLast(4);
        dq.addFirst(1);
        printList(dq, "list (size 4, empty=false): 1 2 3 4");
        item = dq.removeLast();
        printItem(item, "removed last");
        printList(dq, "list (size 3, empty=false): 1 2 3");
        item = dq.removeFirst();
        printItem(item, "removed first");
        printList(dq, "list (size 2, empty=false): 2 3");
        item = dq.removeFirst();
        printItem(item, "removed first");
        printList(dq, "list (size 1, empty=false): 3");
        item = dq.removeLast();
        printItem(item, "removed last");
        printList(dq, "list (size 0, empty=true): ");
    }

}
