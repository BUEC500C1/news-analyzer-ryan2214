import os
import time
from multiprocessing import Queue, Process, freeze_support


def inputQ(queue):
    info = str(os.getpid()) +"(put):"+ str(time.asctime())
    queue.put(info)


def outputQ(queue):
    info = queue.get()
    print('%s%s \033[32m%s\033[0m' %(str(os.getpid()), '(get):',info))


if __name__ == '__main__':
    freeze_support()
    record1 = [] #store input process
    record2 = [] #stroe output process
    queue = Queue(3)

    # input to queue
    for i in range(10):
        process = Process(target=inputQ, args=(queue,))
        process.start()
        record1.append(process)
    # output from queue
    for i in range(10):
        process = Process(target=outputQ, args=(queue,))
        process.start()
        record2.append(process)

    for p in record1:
        p.join()
    for p in record2:
        p.join()