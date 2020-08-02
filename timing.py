import time

def stopwatch(seconds):
    start = time.time()
    # time.clock()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        print("I am doing something")
        print("seconds count: %02d" % ( elapsed))


stopwatch(2)