from multiprocessing import Process, Queue
import time

def p1(q):
    time.sleep(1)
    q.put('string1')
    time.sleep(1)
    q.put('string2')
    time.sleep(1)
    q.put('string3')


def p2(q):
    print(q.get())
    print(q.get())
    time.sleep(1)
    print(q.get())
    time.sleep(1)
    print(q.get())
    time.sleep(1)




if __name__ == '__main__':
    q = Queue()

    pr1 = Process(target=p1, args=(q,))
    pr2 = Process(target=p2, args=(q,))

    pr1.daemon = True
    pr2.daemon = True

    pr1.start()
    pr2.start()

    pr1.join()
    pr2.join()