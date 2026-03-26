import java.util.Random;

/**
 * Lotto Draw Simulation for Assignment Task 2
 * Simulates a lotto game using a custom String Linked List (StrLinkedList)
 * Features: generate number pool, draw winning numbers, generate tickets, calculate prizes and profit
 */
public class LottoDraw {
    // Configurable constants (easy to modify without changing logic)
    private static final int NUM_MIN = 1;
    private static final int NUM_MAX = 40;
    private static final int WIN_NUM_COUNT = 6;
    private static final int TICKET_COUNT = 100;
    private static final double TICKET_PRICE = 10.00;
    private static final int NUM_PER_TICKET = 6;

    private static final Random random = new Random();

    public static void main(String[] args) {
        // Step 1: Generate the full number pool (1 to 40)
        StrLinkedList numberPool = generateNumberPool(NUM_MIN, NUM_MAX);
        System.out.println("Lotto Number Pool (1-" + NUM_MAX + "): ");
        numberPool.print();
        System.out.println();

        // Step 2: Randomly select 6 unique winning numbers
        StrLinkedList winningNumbers = selectWinningNumbers(numberPool, WIN_NUM_COUNT);
        System.out.println("Winning Numbers: ");
        winningNumbers.print();
        System.out.println();

        // Step 3: Generate 100 lotto tickets
        StrLinkedList[] allTickets = generateAllTickets(TICKET_COUNT, NUM_MIN, NUM_MAX, NUM_PER_TICKET);
        System.out.println("Generated " + TICKET_COUNT + " tickets. Calculating prizes...");
        System.out.println("----------------------------------------");

        // Step 4: Calculate financial results
        double totalPrize = calculateTotalPrize(allTickets, winningNumbers);
        double totalSales = calculateTotalSales(TICKET_COUNT, TICKET_PRICE);
        double profit = calculateProfit(totalSales, totalPrize);

        // Step 5: Print final results
        printFinalResult(totalSales, totalPrize, profit);
    }

    /**
     * Generates a linked list containing all numbers from min to max
     * @param min minimum number
     * @param max maximum number
     * @return filled number pool
     */
    private static StrLinkedList generateNumberPool(int min, int max) {
        StrLinkedList pool = new StrLinkedList();
        for (int i = max; i >= min; i--) {
            pool.add(String.valueOf(i));
        }
        return pool;
    }

    /**
     * Randomly selects unique winning numbers from the pool
     * @param pool number pool
     * @param count number of winning numbers to select
     * @return winning numbers list
     */
    private static StrLinkedList selectWinningNumbers(StrLinkedList pool, int count) {
        StrLinkedList winning = new StrLinkedList();
        int poolLength = pool.getLength();

        if (count > poolLength) count = poolLength;

        while (winning.getLength() < count) {
            int randomIndex = random.nextInt(poolLength);
            String num = pool.getValueAt(randomIndex);
            if (!winning.hasValue(num)) {
                winning.add(num);
            }
        }
        return winning;
    }

    /**
     * Generates all lotto tickets with unique random numbers
     * @param ticketCount total tickets to generate
     * @param min min number
     * @param max max number
     * @param numPerTicket numbers per ticket
     * @return array of lotto tickets
     */
    private static StrLinkedList[] generateAllTickets(int ticketCount, int min, int max, int numPerTicket) {
        StrLinkedList[] tickets = new StrLinkedList[ticketCount];
        for (int i = 0; i < ticketCount; i++) {
            StrLinkedList ticket = new StrLinkedList();
            while (ticket.getLength() < numPerTicket) {
                int randomNum = min + random.nextInt(max - min + 1);
                String numStr = String.valueOf(randomNum);
                if (!ticket.hasValue(numStr)) {
                    ticket.add(numStr);
                }
            }
            tickets[i] = ticket;
        }
        return tickets;
    }

    /**
     * Calculates prize for a single ticket based on matching numbers
     * @param ticket single ticket
     * @param winningNumbers winning numbers list
     * @return prize amount
     */
    private static double calculateSingleTicketPrize(StrLinkedList ticket, StrLinkedList winningNumbers) {
        int matchCount = 0;
        for (int i = 0; i < ticket.getLength(); i++) {
            String num = ticket.getValueAt(i);
            if (winningNumbers.hasValue(num)) {
                matchCount++;
            }
        }

        return switch (matchCount) {
            case 2 -> 10.00;
            case 3 -> 100.00;
            case 4 -> 1000.00;
            case 5 -> 10000.00;
            case 6 -> 100000.00;
            default -> 0.00;
        };
    }

    /**
     * Calculates total prize money for all tickets
     * @param allTickets all generated tickets
     * @param winningNumbers winning numbers
     * @return total prize
     */
    private static double calculateTotalPrize(StrLinkedList[] allTickets, StrLinkedList winningNumbers) {
        double total = 0.00;
        for (StrLinkedList ticket : allTickets) {
            total += calculateSingleTicketPrize(ticket, winningNumbers);
        }
        return total;
    }

    /**
     * Calculates total sales revenue
     * @param ticketCount number of tickets
     * @param ticketPrice price per ticket
     * @return total sales
     */
    private static double calculateTotalSales(int ticketCount, double ticketPrice) {
        return ticketCount * ticketPrice;
    }

    /**
     * Calculates profit: total sales - total prize
     * @param totalSales total sales
     * @param totalPrize total prize paid
     * @return profit
     */
    private static double calculateProfit(double totalSales, double totalPrize) {
        return totalSales - totalPrize;
    }

    /**
     * Prints formatted final results
     * @param totalSales total sales
     * @param totalPrize total prize
     * @param profit profit
     */
    private static void printFinalResult(double totalSales, double totalPrize, double profit) {
        System.out.println("========== Lotto Draw Final Results ==========");
        System.out.println("Total Tickets Sold: " + TICKET_COUNT);
        System.out.println("Price per Ticket: $" + String.format("%.2f", TICKET_PRICE));
        System.out.println("Total Sales: $" + String.format("%.2f", totalSales));
        System.out.println("Total Prize Paid: $" + String.format("%.2f", totalPrize));
        System.out.println("Total Profit: $" + String.format("%.2f", profit));
        System.out.println("=================================================");
    }
}