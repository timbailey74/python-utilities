#

import winsound
import threading
import time

EXITCODE = -1

def make_beep():
    winsound.Beep(500, 1000)

def threadloop(messq):
    tstart = time.clock()
    toffset = 1e9

    while True:
        if time.clock() - tstart > toffset:
            make_beep()

        if not messq: continue
        if messq[0] == EXITCODE: break

        toffset = messq[0]
        messq.remove(toffset)
        #print('Received new offset: ', toffset)
        tstart = time.clock()

    print('Exiting thread')

def do_commands():
    message_queue = list()

    t = threading.Thread(target = threadloop, args=(message_queue,))
    t.start()

    x = None
    while x != EXITCODE:
        x = int(input('Set next alarm? '))
        message_queue.append(x)

    print('Exiting main')

#
# TEST
#

do_commands()
