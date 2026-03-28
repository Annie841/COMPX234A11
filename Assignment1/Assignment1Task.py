import threading
import time
import random


class printDoc:
    def __init__(self, content, machine_id):
        self.content = content
        self.machine_id = machine_id

class printList:
    def __init__(self):
        self.queue = []
    
    def queueInsert(self, doc):
        self.queue.append(doc)
        print(f"📥 Task added to queue | Machine:{doc.machine_id} | Queue size:{len(self.queue)}")
    
    def queuePrint(self, printer_id):
        if self.queue:
            doc = self.queue.pop(0)
            print(f"🖨️  Printer {printer_id} finished printing | Machine:{doc.machine_id} | Content:{doc.content}")
        else:
            print(f"🖨️  Printer {printer_id} queue empty")

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines
    QUEUE_SIZE = 5  

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads
        self.empty = threading.Semaphore(self.QUEUE_SIZE)   # Empty slots in queue
        self.full = threading.Semaphore(0)                  # Filled slots in queue
        self.mutex = threading.Lock()                  # Mutual exclusion lock

    def start_task1(self):
        # Create Machine and Printer threads
        # Write code here
        self.sim_active = True
        self.mThreads = []
        self.pThreads = []
        self.print_list.queue.clear()
        print(f"\n===== TASK 1 START (No Synchronization | Queue Overwrite) | {self.NUM_MACHINES} Machines | {self.NUM_PRINTERS} Printers | Runtime: {self.SIMULATION_TIME}s =====")
        
        for p_id in range(1, self.NUM_PRINTERS + 1):
            printer_thread = self.printerThread(p_id, self)
            self.pThreads.append(printer_thread)
        for m_id in range(1, self.NUM_MACHINES + 1):
            machine_thread = self.machineThread(m_id, self)
            self.mThreads.append(machine_thread)
        # Start all the threads
        # Write code here
        
        for p in self.pThreads:
            p.start()
        for m in self.mThreads:
            m.start()
            # Run simulation
        time.sleep(self.SIMULATION_TIME)
        self.sim_active = False

        # Wait for threads to finish
        for p in self.pThreads:
            p.join()
        for m in self.mThreads:
            m.join()
        
        print("===== TASK 1 COMPLETED =====")
    
    # ===================== 修复：start_task2改为独立方法 =====================
    def start_task2(self):
        # ===================== Start Task 2: Synchronized Version (No Overwrite | Safe Access) =====================
        self.sim_active = True
        self.mThreads = []
        self.pThreads = []
        self.print_list.queue.clear()

        print(f"\n===== TASK 2 START (Synchronized | No Overwrite) | {self.NUM_MACHINES} Machines | {self.NUM_PRINTERS} Printers | Runtime: {self.SIMULATION_TIME}s =====")      
        # Create printer threads
        for p_id in range(1, self.NUM_PRINTERS + 1):
            thread = self.PrinterTask2(p_id, self)
            self.pThreads.append(thread)
        # Create machine threads
        for m_id in range(1, self.NUM_MACHINES + 1):
            thread = self.MachineTask2(m_id, self)
            self.mThreads.append(thread)
            # Start all threads
        for t in self.pThreads:
            t.start()
        for t in self.mThreads:
            t.start()   

            # Run simulation for specified time
        time.sleep(self.SIMULATION_TIME)
        self.sim_active = False
        # Release semaphores to avoid blocking threads
        for _ in range(self.QUEUE_SIZE * 2):
            try:
                self.empty.release()
                self.full.release()
            except ValueError:
                break

        for t in self.pThreads:
            t.join(timeout=2)
        for t in self.mThreads:
            t.join(timeout=2)
        
        print("===== TASK 2 COMPLETED =====")

    # Printer class
    class printerThread(threading.Thread):    
        def __init__(self, printerID, outer):
            super().__init__()
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                # Write code here
                self.printDox(self.printerID)

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            # Print from the queue
            self.outer.print_list.queuePrint(printerID)
            
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            super().__init__()
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                self.printRequest(self.machineID)

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)        

    # ===================== 修复：删除重复的MachineTask2定义，保留正确版本并修正方法缩进 =====================
    class MachineTask2(threading.Thread):
        def __init__(self, machine_id, outer):
            super().__init__()
            self.machine_id = machine_id
            self.outer = outer
        def run(self):
            while self.outer.sim_active:
                self.machine_sleep()
                doc = printDoc(f"Machine_{self.machine_id}", self.machine_id)
                print(f"Machine {self.machine_id} sent a print request")
                # Critical Section: Synchronized insertion
                self.outer.empty.acquire()
                self.outer.mutex.acquire()
                try:
                    self.outer.print_list.queueInsert(doc)
                finally:
                    self.outer.mutex.release()
                    self.outer.full.release()
        # ===================== 修复：将machine_sleep移出run方法，改为类的同级方法 =====================
        def machine_sleep(self):
            sleep_time = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleep_time)
                  
    # ===================== Task 2 Printer Thread (With Semaphores & Lock) =====================
    class PrinterTask2(threading.Thread):
        def __init__(self, printer_id, outer):
            super().__init__()
            self.printer_id = printer_id
            self.outer = outer

        def run(self):
            while self.outer.sim_active:
                self.printer_sleep()    
                self.outer.full.acquire()
                self.outer.mutex.acquire()
                try:
                    print(f"Printer {self.printer_id} is printing...")
                    self.outer.print_list.queuePrint(self.printer_id)
                finally:
                    self.outer.mutex.release()
                    self.outer.empty.release()

        def printer_sleep(self):
            sleep_time = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleep_time)

# Instantiate main simulation class
if __name__ == "__main__":
    sim = Assignment1()
    sim.start_task1()   # Run Task 1 first
    sim.start_task2()   # Then run Task 2