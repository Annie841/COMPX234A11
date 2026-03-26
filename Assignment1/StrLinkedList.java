import java.lang.invoke.VarHandle.VarHandleDesc;

/**
 * String Linked List Implementation for COMPX201 Assignment
 * Stores and manages a list of String values using nodes
 * Required for LottoDraw Task 2
 */
public class StrLinkedList {
    // Inner Node class
    private class Node {
        String data;
        Node next;
        public Node(String data){
            this .data = data ;
            this.next = null;
        }
        

 


    }
    private Node head;
    public StrLinkedList(){
        head =null;
    }
    /**
     * Check if the list is empty
     * @return true if empty, false otherwise
     */
    public boolean isEmpty() {
        return head == null;
    }

    /**
     * Get the number of elements in the list
     * @return length of the list
     */
    public int getLength() {
        int count = 0;
        Node current = head;
        while (current != null) {
            count++;
            current = current.next;
        }
        return count;
    }

    /**
     * Check if the list contains a specific value
     * @param value the string to search for
     * @return true if found, false otherwise
     */
    public boolean hasValue(String value) {
        Node current = head;
        while (current != null) {
            if (current.data.equals(value)) {
                return true;
            }
            current = current.next;
        }
          return false;
        }

    
        

    }
     
        
    

    
}