from bot1 import start_bot1
from bot2 import start_bot2
from bot4 import start_bot4
from bot5 import start_bot5
import threading

def run_bot1():
	start_bot1()

def run_bot2():
	start_bot2()
	
def run_bot4():
	start_bot4()

def run_bot5():
	start_bot5()

thread1 = threading.Thread(target=run_bot1)
thread2 = threading.Thread(target=run_bot2)
#thread3 = threading.Thread(target=run_bot3)
thread4 = threading.Thread(target=run_bot4)
thread5 = threading.Thread(target=run_bot5)

thread1.start()
thread2.start()
#thread3.start()
thread4.start()
thread5.start()

thread1.join()
thread2.join()
#thread3.join()
thread4.join()
thread5.join()
