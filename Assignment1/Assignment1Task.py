import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads
        self.empty = threading.Semaphore(self.QUEUE_SIZE)   # Empty slots in queue
        self.full = threading.Semaphore(0)                  # Filled slots in queue
        self.mutex = threading.Semaphore(1)                  # Mutual exclusion lock

        
        

    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here
         self.sim_active = True
         self.machine_threads.clear()
         self.printer_threads.clear()
         print(f"\n===== TASK 1 START (No Synchronization | Queue Overwrite) | {self.NUM_MACHINES} Machines | {self.NUM_PRINTERS} Printers | Runtime: {self.SIMULATION_TIME}s =====")
        
         for p_id in range  (1,self.NUM_PRINTERS+1): 
              printer_thread = self.printerThread(p_id,self)
              self.pThreads.append(printer_thread)
         for m_id in range (1,self.NUM_MACHINES+1): 
             machine_thread = self .machineThread(m_id,self)
             self.mThreads.append (machine_thread) 
        # Start all the threads
        # Write code here
        
         for p in self.pThreads:    
              p.start()
         for m in self.mThreads:     
               m.start()
         time.sleep(self.SIMULATION_TIME)
         self.sim_active = False
         for p in self.printer_threads:
               p.join()
         for m in self.machine_threads:
               m.join()
        
         print("===== TASK 1 COMPLETED =====")
          # ===================== Start Task 2: Synchronized Version (No Overwrite | Safe Access) =====================
         def start_task2(self):
          self.sim_active = True
          self.machine_threads.clear()
          self.printer_threads.clear()

         print(f"\n===== TASK 2 START (Synchronized | No Overwrite) | {self.NUM_MACHINES} Machines | {self.NUM_PRINTERS} Printers | Runtime: {self.SIMULATION_TIME}s =====")      
         # Create printer threads
         for p_id in range(1, self.NUM_PRINTERS + 1):
            thread = self.PrinterTask2(p_id, self)
            self.printer_threads.append(thread)
          # Create machine threads
         for m_id in range(1, self.NUM_MACHINES + 1):
            thread = self.MachineTask2(m_id, self)
            self.machine_threads.append(thread)
             # Start all threads
         for t in self.printer_threads:
            t.start()
         for t in self.machine_threads:
            t.start()   

             # Run simulation for specified time
         time.sleep(self.SIMULATION_TIME)
         self.sim_active = False
         # Release semaphores to avoid blocking threads
         for _ in range(self.QUEUE_SIZE):
            self.empty.release()
            self.full.release()
            # Wait for all threads to finish
         for t in self.printer_threads:
            t.join()
         for t in self.machine_threads:
            t.join()
        
         print("===== TASK 2 COMPLETED =====")

            
         
        

         print(f"=== Task1 Simulation Started: {self.NUM_MACHINES} machines | {self.NUM_PRINTERS} printers | Running for {self.SIMULATION_TIME} seconds ===") 
        
        # Let the simulation run for some time
         time.sleep(self.SIMULATION_TIME)    

        # Finish simulation
         self.sim_active = False   

        # Wait until all printer threads finish by joining them
        # Write code here
         for p in self.Threads: 
              p.join()
    print("=== Task2 Simulation Ended ===")

              

    # Printer class
    class printerThread(threading.Thread):    
         def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
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

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                # Write code here
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
             # ===================== Task 2 Machine Thread (With Semaphores & Lock) =====================
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
                def machine_sleep(self):
                 sleep_time = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
                 time.sleep(sleep_time)    



            
   
            # Instantiate main simulation class
if __name__ == "__main__":
    sim = Assignment1()
    
    sim.startSimulation()   
 