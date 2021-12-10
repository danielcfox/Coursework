/******************************************************************************
 *  Compilation:  javac-algs4 RandomizedQueue.java
 *  Execution:    java-algs4 RandomizedQueue
 ******************************************************************************/

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

import java.util.Iterator;

public class RandomizedQueue<Item> implements Iterable<Item> {

    private Item[] rqlist;
    private int numItems;

    // construct an empty randomized queue
    public RandomizedQueue() {
        rqlist = (Item[]) new Object[1];
        numItems = 0;
    }

    // is the randomized queue empty?
    public boolean isEmpty() {
        return (numItems == 0);
    }

    // return the number of items on the randomized queue
    public int size() {
        return (numItems);
    }

    private void resize(int N) {
        // StdOut.printf("resizing numItems %d new size %d\n", numItems, N);
        Item[] copy = (Item[]) new Object[N];
        for (int i = 0; i < numItems; i++) {
            copy[i] = rqlist[i];
        }
        rqlist = copy;
    }

    // add the item
    public void enqueue(Item item) {
        if (item == null) {
            throw new IllegalArgumentException();
        }
        // randomize upon entry
        // put into random slot, existing entry is put at end
        if (numItems == 0) {
            rqlist[0] = item;
        } else {
            if (numItems == rqlist.length) {
                resize(2 * rqlist.length);
            }
            int slot = StdRandom.uniform(numItems);
            rqlist[numItems] = rqlist[slot];
            rqlist[slot] = item;
        }
        numItems++;
    }

    // remove and return a random item
    public Item dequeue() {
        if (isEmpty()) {
            throw new java.util.NoSuchElementException();
        }
        // we are sorted in random order, so just take from the rear
        Item item = rqlist[--numItems];
        rqlist[numItems] = null;
        if (numItems > 0 && numItems == rqlist.length / 4) {
            resize(rqlist.length / 2);
        }
        return item;
    }

    // return a random item (but do not remove it)
    public Item sample() {
        if (isEmpty()) {
            throw new java.util.NoSuchElementException();
        }
        int slot = StdRandom.uniform(numItems);
        return rqlist[slot];
    }

    private class RQIterator implements Iterator<Item> {
        private Item[] shuffle;
        private int current;

        public RQIterator() {
            shuffle = (Item[]) new Object[numItems];
            for (int i = 0; i < numItems; i++) {
                shuffle[i] = rqlist[i];
            }
            for (int i = 0; i < numItems; i++) {
                int slot = StdRandom.uniform(numItems);
                if (i != slot) {
                    Item temp = shuffle[i];
                    shuffle[i] = shuffle[slot];
                    shuffle[slot] = temp;
                }
            }
        }

        public boolean hasNext() {
            return (current < numItems);
        }

        public void remove() {
            throw new UnsupportedOperationException();
        }

        public Item next() {
            if (!hasNext()) {
                throw new java.util.NoSuchElementException();
            }
            current++;
            return (shuffle[current - 1]);
        }

    }

    // return an iterator over items in order from front to back
    public Iterator<Item> iterator() {
        return new RQIterator();
    }

    private static void printList(RandomizedQueue<Integer> rq, String expected) {
        StdOut.printf("list (num items %d, empty=%b): ", rq.size(), rq.isEmpty());
        for (int item : rq) {
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
        RandomizedQueue<Integer> rq = new RandomizedQueue<Integer>();
        int item;

        rq.enqueue(1);
        printItem(1, "enqueue");
        printList(rq, "list (num items 1, empty=false):)");
        item = rq.sample();
        printItem(item, "sample");
        printList(rq, "list (num items 1, empty=false):");
        rq.enqueue(5);
        printItem(5, "enqueue");
        printList(rq, "list (num items 2, empty=false):");
        item = rq.dequeue();
        printItem(item, "dequee");
        printList(rq, "list (num items 1, empty=false):");
        item = rq.dequeue();
        printItem(item, "dequee");
        printList(rq, "list (num items 0, empty=true):");
        rq.enqueue(2);
        rq.enqueue(3);
        rq.enqueue(4);
        rq.enqueue(6);
        rq.enqueue(7);
        for (int i = 0; i < 8; i++) {
            item = rq.sample();
            printItem(item, "sample");
        }
        printList(rq, "list (num items 5, empty=false):");
        for (int i = 0; i < 3; i++) {
            item = rq.dequeue();
            printItem(item, "dequeue");
        }
        printList(rq, "list (num items 2, empty=false):");
        rq.enqueue(8);
        rq.enqueue(9);
        rq.enqueue(10);
        rq.enqueue(11);
        printList(rq, "list (num items 6, empty=false):");
        for (int i = 0; i < 6; i++) {
            item = rq.sample();
            printItem(item, "sample");
        }
        for (int i = 0; i < 6; i++) {
            item = rq.dequeue();
            printItem(item, "dequeue");
        }
        printList(rq, "list (num items 0, empty=true):");
        /*
        for (int i = 0; i < 1000; i++) {
            rq.enqueue(i);
        }
        for (int i = 0; i < 500; i++) {
            item = rq.dequeue();
        }
        for (int i = 1000; i < 1500; i++) {
            rq.enqueue(i);
        }
        for (int i = 0; i < 500; i++) {
            item = rq.dequeue();
        }
        printList(rq, "list (num items 1000, empty=false):");
        for (int i = 0; i < 498; i++) {
            item = rq.dequeue();
        }
        printList(rq, "list (num items 2, empty=false):");
        for (int i = 0; i < 2; i++) {
            item = rq.dequeue();
        }
        printList(rq, "list (num items 0, empty=true):");
        */

    }
}
