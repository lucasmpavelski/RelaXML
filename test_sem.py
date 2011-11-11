

from threading import Thread, RLock, currentThread
from time import sleep
from random import random

def synchronized_with_attr(lock_name, log):
    def decorator(method):
        def synced_method(self, *args, **kws):
            lock = getattr(self, lock_name)
            log_p = getattr(self, log)
            with lock:
                print "Executando " + method.__name__ + log_p
                method(self, *args, **kws)
                print "Terminou " + method.__name__ + log_p
        return synced_method
    return decorator
    
l = [0]

class Counter:
    
    def __init__(self, log):
        self.lock = RLock()
        self.total = 0
        self.log = log
		
    @synchronized_with_attr("lock", "log")
    def add_one(self):
        val = self.total
        val += 1
        self.total = val
        for i in range(10) :
            sleep(0.1)
            l.append(l[-1] + 1)
	
    @synchronized_with_attr("lock", "log")
    def add_two(self):
        val = self.total
        val += 2
        self.total = val
        for i in range(10) :
            sleep(0.1)
            l.append(l[-1] + 1)

c = Counter("my log")

class PrintMsg(object):
    def startmsg(self):
        print '%s started...' % self.__class__.__name__
    def endmsg(self):
        print '%s ended...' % self.__class__.__name__        

class BaseThread(Thread, PrintMsg):
    pass

class MyThread3(BaseThread):
    def run(self):
        self.startmsg()
        c.add_one()
        self.endmsg()        

class MyThread4(BaseThread):
    def run(self):
        self.startmsg()        
        c.add_two()
        self.endmsg()


t3 = MyThread3()
t4 = MyThread4()

t3.start(); t4.start()
t3.join(); t4.join()

# List will have elements in order
print l
