public class PrintQueue {
    private final int capacity;
    private int count = 0;

    public PrintQueue(int capacity) {
        this.capacity = capacity;
    }

    // SYNCHRONIZED: Only one thread can enter at a time
    public synchronized void addDocument() throws InterruptedException {
        // WAIT if queue is FULL → NO OVERWRITE!
            while (count >= capacity) {
            wait();
        }
        count++;
        System.out.println("Machine added document | Queue size: " + count);
        notifyAll(); // Wake waiting printers
    }